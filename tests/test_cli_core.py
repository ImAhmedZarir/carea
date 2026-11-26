"""Core CLI unit tests for carea (Phase 4 baseline; expanded in Phase 6)."""

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
from carea.cli import main as cli_main
from carea.commands import (
    apply_mcp_profile,
    build_mcp_profile,
    cmd_airlock_sign,
    cmd_init,
    cmd_parity_report,
    cmd_return_feedback,
    cmd_spec_draft,
    cmd_validate_handoff,
)


class TestCareaCliCore(unittest.TestCase):
    def test_bundled_data_matches_repo_sources(self) -> None:
        self.assertEqual(
            (REPO_ROOT / "compat" / "matrix.json").read_text(encoding="utf-8"),
            (SRC_DIR / "carea" / "data" / "matrix.json").read_text(encoding="utf-8"),
        )

    def test_init_and_validate_private_deep_banner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "demo"
            res = cmd_init(proj, mode="private-deep-rebuild", target_name="own-app")
            self.assertTrue(res["deep_private"])
            spec_text = (proj / "airlock" / "clean-room-spec.md").read_text(encoding="utf-8")
            self.assertIn("NOT CLEAN-ROOM", spec_text)
            val = cmd_validate_handoff(proj / "airlock" / "carea-handoff.json")
            self.assertTrue(val["valid"], val["errors"])

            # signing deep_private=true as clean-room must refuse
            with self.assertRaises(ValueError):
                cmd_airlock_sign(
                    proj / "airlock" / "carea-handoff.json",
                    reviewer="Alice",
                    confirm_human_review=True,
                )

    def test_airlock_lint_detects_leaks_and_blocks_sign(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            cmd_init(proj, mode="two-team-process")
            leak_file = proj / "airlock" / "clean-room-spec.md"
            leak_file.write_text(
                "# Bad Spec\n\n```js\nfunction secretAlgo(x) { return x ^ 0x55; }\n```\n",
                encoding="utf-8",
            )
            lint = lint_airlock(proj / "airlock")
            self.assertEqual(lint["status"], "FAIL")
            self.assertIn("NEVER proves absence of leakage", lint["disclaimer"])
            with self.assertRaises(ValueError):
                cmd_airlock_sign(
                    proj / "airlock" / "carea-handoff.json",
                    reviewer="Reviewer",
                    confirm_human_review=True,
                )

    def test_airlock_sign_requires_explicit_confirm_flag(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            cmd_init(proj, mode="two-team-process")
            with self.assertRaises(PermissionError):
                cmd_airlock_sign(
                    proj / "airlock" / "carea-handoff.json",
                    reviewer="Reviewer",
                    confirm_human_review=False,
                )

    def test_spec_draft_copies_ids_only_no_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bundle = Path(td) / "bundle.json"
            bundle.write_text(
                json.dumps(
                    {
                        "evidence_format": 2,
                        "evidence": [
                            {"evidence_id": "ev_alpha_1", "raw_result": "SUPER_SECRET_RAW_CODE()"},
                        ],
                        "unknowns": [{"unknown_id": "unk_gap_1"}],
                        "obligations": [{"obligation_id": "obl_tick_rate"}],
                    }
                ),
                encoding="utf-8",
            )
            res = cmd_spec_draft(bundle)
            self.assertTrue(res["draft"])
            self.assertIn("DRAFT", res["markdown"])
            self.assertIn("ev_alpha_1", res["markdown"])
            self.assertIn("unk_gap_1", res["markdown"])
            self.assertIn("obl_tick_rate", res["markdown"])
            self.assertNotIn("SUPER_SECRET_RAW_CODE", res["markdown"])

    def test_parity_requires_both_axes_complete(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            cmd_init(proj, mode="two-team-process", target_name="app")
            handoff = proj / "airlock" / "carea-handoff.json"
            ca_rep = Path(td) / "ca.json"
            rea_rep = Path(td) / "rea.json"
            ca_rep.write_text(json.dumps({"obligations": {"obl_app_core": {"status": "passed"}}}), encoding="utf-8")

            # REA missing -> partial, NOT passed
            part = cmd_parity_report(handoff, ca_report_path=ca_rep)
            self.assertEqual(part["overall_status"], "partial")
            self.assertEqual(part["rows"][0]["final_status"], "partial")

            # Both passed AND clear coverage -> passed
            data = json.loads(handoff.read_text(encoding="utf-8"))
            data["obligations"][0]["coverage"] = {"scope": "complete", "notes": "All checks complete"}
            handoff.write_text(json.dumps(data), encoding="utf-8")
            rea_rep.write_text(json.dumps({"obligations": {"obl_app_core": {"status": "passed"}}}), encoding="utf-8")
            full = cmd_parity_report(handoff, ca_report_path=ca_rep, rea_report_path=rea_rep)
            self.assertEqual(full["overall_status"], "passed")

    def test_return_feedback_and_mcp_profile_apply_requires_yes_non_tty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            cmd_init(proj, mode="two-team-process", target_name="app")
            handoff = proj / "airlock" / "carea-handoff.json"
            ca_rep = Path(td) / "ca.json"
            ca_rep.write_text(
                json.dumps({"obligations": {"obl_app_core": {"status": "failed", "pixel_diff": "Button shifted 8px"}}}),
                encoding="utf-8",
            )
            fb = cmd_return_feedback(handoff, ca_report_path=ca_rep)
            self.assertEqual(fb["failing_count"], 1)
            self.assertIn("Button shifted 8px", fb["markdown"])

            snippet = build_mcp_profile("rea-hot-cold")
            self.assertEqual(snippet["mcpServers"]["rea"]["env"]["REA_MCP_TOOL_CATALOG_PROFILE"], "hot-cold")

            master = build_mcp_profile("carea-master")
            self.assertIn("rea", master["mcpServers"])
            self.assertIn("craft-anything", master["mcpServers"])
            self.assertEqual(master["mcpServers"]["rea"]["env"]["REA_ASAR_MAX_HEADER_BYTES"], "268435456")
            self.assertIn("--deep", master["mcpServers"]["craft-anything"]["args"])
            self.assertIn("--all-tools", master["mcpServers"]["craft-anything"]["args"])
            self.assertIn("uefi", build_mcp_profile("rea-all-families")["mcpServers"]["rea"]["env"]["REA_MCP_TOOL_FAMILIES"])
            self.assertEqual(build_mcp_profile("ca-deep-full")["mcpServers"]["craft-anything"]["args"], ["mcp", "--deep", "--all-tools"])

            cfg = Path(td) / "client.json"
            with self.assertRaises(PermissionError):
                apply_mcp_profile("ca-clean-room", cfg, assume_yes=False)
            res = apply_mcp_profile("ca-clean-room", cfg, assume_yes=True)
            self.assertTrue(res["applied"])
            self.assertIn("craft-anything", json.loads(cfg.read_text(encoding="utf-8"))["mcpServers"])

    def test_isolation_check_catches_missing_and_cli_version(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            (proj / "analyst-evidence").mkdir(parents=True)
            (proj / "airlock").mkdir()
            res = check_isolation(proj)
            self.assertEqual(res["status"], "WARN")
            with self.assertRaises(SystemExit) as cm:
                cli_main(["--version"])
            self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
