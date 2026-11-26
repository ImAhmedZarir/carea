"""Tests for airlock leak fixtures, schema 1.0/1.1 fixtures, and doctor/CLI edge cases."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from carea.airlock import check_isolation, lint_airlock
from carea.commands import cmd_validate_handoff
from carea.upstream import check_mcp_config_file, run_doctor

FIXTURES = REPO_ROOT / "tests" / "fixtures"


class TestAirlockLeakFixtures(unittest.TestCase):
    def test_true_positive_code_fence(self) -> None:
        res = lint_airlock(FIXTURES / "airlock" / "tp_code_fence.md")
        self.assertEqual(res["status"], "FAIL")
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("fenced-target-code", rules)
        self.assertIn("unlabelled-code-fence", rules)

    def test_true_positive_asm_hexdump(self) -> None:
        res = lint_airlock(FIXTURES / "airlock" / "tp_asm_hexdump.md")
        self.assertEqual(res["status"], "FAIL")
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("assembly-mnemonic", rules)
        self.assertIn("hex-dump", rules)

    def test_true_positive_minified_base64(self) -> None:
        res = lint_airlock(FIXTURES / "airlock" / "tp_minified_base64.md")
        self.assertEqual(res["status"], "FAIL")
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("minified-js", rules)
        self.assertIn("base64-blob", rules)

    def test_true_positive_paths_secrets_email(self) -> None:
        res = lint_airlock(FIXTURES / "airlock" / "tp_paths_secrets.md")
        self.assertEqual(res["status"], "FAIL")
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("analyst-evidence-path", rules)
        self.assertIn("secret-github-token", rules)
        self.assertIn("cookie-header", rules)
        self.assertIn("non-example-email", rules)

    def test_true_positive_verbatim_prose_warns(self) -> None:
        res = lint_airlock(FIXTURES / "airlock" / "tp_verbatim_prose.md")
        self.assertEqual(res["status"], "WARN")
        rules = {f["rule"] for f in res["findings"]}
        self.assertIn("quoted-verbatim-prose", rules)
        self.assertIn("long-verbatim-prose", rules)

    def test_true_positive_forbidden_media_extension_dynamic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            asset = Path(td) / "icon.png"
            asset.write_bytes(b"not-a-real-png-test-payload")
            res = lint_airlock(Path(td))
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["findings"][0]["rule"], "binary-or-media-asset")

    def test_clean_negatives_pass_strictly(self) -> None:
        for name in ("clean_spec.md", "clean_feedback.md"):
            res = lint_airlock(FIXTURES / "airlock" / name)
            self.assertEqual(res["status"], "PASS", f"{name}: {res['findings']}")


class TestHandoffSchemaFixtures(unittest.TestCase):
    def test_all_positive_handoff_fixtures_valid(self) -> None:
        files = sorted((FIXTURES / "handoffs" / "positive").glob("*.json"))
        self.assertGreaterEqual(len(files), 7)
        for fp in files:
            res = cmd_validate_handoff(fp)
            self.assertTrue(res["valid"], f"{fp.name} errors: {res['errors']}")

    def test_all_negative_handoff_fixtures_rejected(self) -> None:
        files = sorted((FIXTURES / "handoffs" / "negative").glob("*.json"))
        self.assertGreaterEqual(len(files), 7)
        for fp in files:
            res = cmd_validate_handoff(fp)
            self.assertFalse(res["valid"], f"{fp.name} should have failed validation")


class TestDoctorAndIsolation(unittest.TestCase):
    def test_doctor_warns_on_full_schema_and_all_tools(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "mcp.json"
            cfg.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "rea": {
                                "command": "rea",
                                "args": ["mcp"],
                                "env": {"REA_MCP_INPUT_SCHEMA_PROFILE": "full"},
                            },
                            "craft-anything": {
                                "command": "craft-anything-cli",
                                "args": ["mcp", "--all-tools"],
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            findings = check_mcp_config_file(cfg, "6.10.1")
            severities = [f["severity"] for f in findings]
            self.assertIn("FAIL", severities)
            self.assertIn("WARN", severities)
            doc = run_doctor(client_configs=[cfg])
            self.assertGreaterEqual(len(doc["mcp_profile_findings"]), 2)

    def test_isolation_check_passes_when_permissions_present(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            for d in ("analyst-evidence", "airlock", "builder-workspace", "verification", ".claude"):
                (proj / d).mkdir(parents=True)
            (proj / ".claude" / "settings.local.json").write_text(
                json.dumps({"permissions": {"deny": ["Read(./analyst-evidence/**)"]}}),
                encoding="utf-8",
            )
            res = check_isolation(proj)
            self.assertEqual(res["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
