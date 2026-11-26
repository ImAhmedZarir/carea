#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Verify installed `rea` and `craft-anything-cli` versions against compat/matrix.json.
.DESCRIPTION
    Probes external `rea` and `craft-anything-cli` executables without vendoring or
    modifying user configs, compares detected versions to compat/matrix.json, and prints
    `supported`, `limited`, `unsupported`, `untested`, or `missing` per engine.
#>

[CmdletBinding()]
param(
    [string]$MatrixPath = "",
    [string]$ReaBin = $env:CAREA_REA_BIN,
    [string]$CraftAnythingBin = $env:CAREA_CA_BIN,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
if ([string]::IsNullOrWhiteSpace($MatrixPath)) {
    $MatrixPath = Join-Path $RepoRoot "compat\matrix.json"
}

if (-not (Test-Path -LiteralPath $MatrixPath)) {
    throw "Compatibility matrix not found: $MatrixPath"
}

$Matrix = Get-Content -LiteralPath $MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Resolve-ToolPath {
    param([string]$Override, [string[]]$Candidates)
    if (-not [string]::IsNullOrWhiteSpace($Override)) {
        if (Test-Path -LiteralPath $Override) { return $Override }
        $cmd = Get-Command $Override -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
        return $null
    }
    foreach ($c in $Candidates) {
        $cmd = Get-Command $c -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }
    return $null
}

function Parse-SemVer {
    param([string]$Text)
    if ($Text -match '(\d+)\.(\d+)\.(\d+)') {
        return [ordered]@{
            raw   = "$($Matches[1]).$($Matches[2]).$($Matches[3])"
            major = [int]$Matches[1]
            minor = [int]$Matches[2]
            patch = [int]$Matches[3]
        }
    }
    return $null
}

function Compare-SemVer {
    param($A, $B)
    if ($A.major -ne $B.major) { return $A.major.CompareTo($B.major) }
    if ($A.minor -ne $B.minor) { return $A.minor.CompareTo($B.minor) }
    return $A.patch.CompareTo($B.patch)
}

function Classify-Version {
    param([string]$VersionStr, $EngineSpec)
    $parsed = Parse-SemVer $VersionStr
    if ($null -eq $parsed) { return "untested" }
    foreach ($r in $EngineSpec.ranges) {
        $minV = Parse-SemVer $r.min
        $maxV = Parse-SemVer $r.max_exclusive
        if ((Compare-SemVer $parsed $minV) -ge 0 -and (Compare-SemVer $parsed $maxV) -lt 0) {
            return $r.status
        }
    }
    $minCompat = Parse-SemVer $EngineSpec.minimum_compatible
    if ($null -ne $minCompat -and (Compare-SemVer $parsed $minCompat) -lt 0) {
        return "unsupported"
    }
    return "untested"
}

function Invoke-Probe {
    param([string]$Exe, [string[]]$CommandArgs)
    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $Exe
        $psi.Arguments = ($CommandArgs -join ' ')
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $proc = [System.Diagnostics.Process]::Start($psi)
        $outTask = $proc.StandardOutput.ReadToEndAsync()
        $errTask = $proc.StandardError.ReadToEndAsync()
        if (-not $proc.WaitForExit(15000)) {
            try { $proc.Kill() } catch {}
            return @{ code = -1; out = ""; err = "timeout after 15s" }
        }
        return @{
            code = $proc.ExitCode
            out  = $outTask.GetAwaiter().GetResult()
            err  = $errTask.GetAwaiter().GetResult()
        }
    } catch {
        return @{ code = -1; out = ""; err = $_.Exception.Message }
    }
}

# Check Node runtime for REA
$NodePath = Resolve-ToolPath "" @("node")
$NodeVersion = $null
$NodeOk = $false
if ($NodePath) {
    $nv = Invoke-Probe $NodePath @("--version")
    if ($nv.code -eq 0) {
        $sv = Parse-SemVer $nv.out
        if ($sv) {
            $NodeVersion = $sv.raw
            # ^22.23.4 || ^24.22.1 || >=26.12.1
            $NodeOk = (
                ($sv.major -eq 22 -and ($sv.minor -gt 23 -or ($sv.minor -eq 23 -and $sv.patch -ge 4))) -or
                ($sv.major -eq 24 -and ($sv.minor -gt 22 -or ($sv.minor -eq 22 -and $sv.patch -ge 1))) -or
                ($sv.major -eq 26 -and ($sv.minor -gt 12 -or ($sv.minor -eq 12 -and $sv.patch -ge 1))) -or
                ($sv.major -gt 26)
            )
        }
    }
}

# Probe REA
$ReaResolved = Resolve-ToolPath $ReaBin @("rea", "rea-agents")
$ReaResult = [ordered]@{
    engine = "rea"
    path = $ReaResolved
    version = $null
    status = "missing"
    node_version = $NodeVersion
    node_satisfied = $NodeOk
    checks = [ordered]@{}
    notes = @()
}

if ($ReaResolved) {
    $pVer = Invoke-Probe $ReaResolved @("--version")
    $pHelp = Invoke-Probe $ReaResolved @("--help")
    $pDoc = Invoke-Probe $ReaResolved @("doctor", "--json")
    $ReaResult.checks["version"] = $pVer.code -eq 0
    $ReaResult.checks["help"] = $pHelp.code -eq 0
    $ReaResult.checks["doctor"] = $pDoc.code -eq 0
    $parsedRea = Parse-SemVer ($pVer.out + "`n" + $pVer.err)
    if ($pVer.code -eq 0 -and $parsedRea) {
        $ReaResult.version = $parsedRea.raw
        $ReaResult.status = Classify-Version $parsedRea.raw $Matrix.engines.rea
    } else {
        $ReaResult.status = "unsupported"
        $ReaResult.notes += "rea binary failed to execute --version cleanly: $($pVer.err.Trim())"
    }
} else {
    $ReaResult.notes += "rea executable not found on PATH (install via npm install -g rea-agents@$($Matrix.engines.rea.recommended))"
}

# Locate Craft Anything (PATH or default Windows portable plugin path if unset)
$CaExtra = @()
$PluginRoot = Join-Path $env:USERPROFILE ".gemini\config\plugins\craft-anything\bin"
if (Test-Path -LiteralPath $PluginRoot) {
    $CaExtra = Get-ChildItem -Path $PluginRoot -Filter "craft-anything-cli*.exe" -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}
$CaResolved = Resolve-ToolPath $CraftAnythingBin (@("craft-anything-cli") + @($CaExtra))
$CaResult = [ordered]@{
    engine = "craft_anything"
    path = $CaResolved
    version = $null
    status = "missing"
    checks = [ordered]@{}
    notes = @()
}

if ($CaResolved) {
    $cVer = Invoke-Probe $CaResolved @("--version")
    $cDoc = Invoke-Probe $CaResolved @("doctor", "--json")
    $cCmd = Invoke-Probe $CaResolved @("commands", "--json")
    $cCap = Invoke-Probe $CaResolved @("capabilities", "--json")
    $CaResult.checks["version"] = $cVer.code -eq 0
    $CaResult.checks["doctor"] = $cDoc.code -eq 0
    $CaResult.checks["commands"] = $cCmd.code -eq 0
    $CaResult.checks["capabilities"] = $cCap.code -eq 0
    $parsedCa = Parse-SemVer ($cVer.out + "`n" + $cVer.err)
    if ($cVer.code -eq 0 -and $parsedCa) {
        $CaResult.version = $parsedCa.raw
        $CaResult.status = Classify-Version $parsedCa.raw $Matrix.engines.craft_anything
    } else {
        $CaResult.status = "unsupported"
        $CaResult.notes += "craft-anything-cli failed to execute --version cleanly: $($cVer.err.Trim())"
    }
} else {
    $CaResult.notes += "craft-anything-cli not found on PATH (install release $($Matrix.engines.craft_anything.recommended) from storytold/craft-anything)"
}

$Report = [ordered]@{
    carea_version = $Matrix.carea_version
    matrix_updated_at = $Matrix.updated_at
    rea = $ReaResult
    craft_anything = $CaResult
}

if ($Json) {
    $Report | ConvertTo-Json -Depth 6
} else {
    Write-Host "carea upstream verification report (matrix $($Matrix.carea_version), updated $($Matrix.updated_at))"
    Write-Host ""
    $reaVerOut = if ($ReaResult.version) { $ReaResult.version } else { "none" }
    $reaPathOut = if ($ReaResult.path) { $ReaResult.path } else { "missing" }
    $nodeVerOut = if ($ReaResult.node_version) { $ReaResult.node_version } else { "none" }
    $caVerOut = if ($CaResult.version) { $CaResult.version } else { "none" }
    $caPathOut = if ($CaResult.path) { $CaResult.path } else { "missing" }

    Write-Host ("[REA]            status={0} version={1} path={2}" -f $ReaResult.status, $reaVerOut, $reaPathOut)
    Write-Host ("                 node={0} satisfied={1}" -f $nodeVerOut, $ReaResult.node_satisfied)
    foreach ($n in $ReaResult.notes) { Write-Host "                 note: $n" }
    Write-Host ("[Craft Anything] status={0} version={1} path={2}" -f $CaResult.status, $caVerOut, $caPathOut)
    foreach ($n in $CaResult.notes) { Write-Host "                 note: $n" }
}
