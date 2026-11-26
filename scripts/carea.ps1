#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$RepoRoot\src;$env:PYTHONPATH" } else { "$RepoRoot\src" }

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 -m carea @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m carea @args
} else {
    throw "Python 3.10+ is required to run carea."
}
exit $LASTEXITCODE
