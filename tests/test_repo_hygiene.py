"""Repository hygiene, link resolution, manifest, compat sync, and asset-ban tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestRepoHygiene(unittest.TestCase):
    def test_compatibility_doc_in_sync_with_matrix(self) -> None:
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "render-compatibility.py"), "--check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_repo_integrity_script_passes(self) -> None:
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "check_repo.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_manifests_and_skills_non_conflicting(self) -> None:
        for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
            data = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
            self.assertEqual(data["name"], "carea")
            self.assertEqual(data["license"], "MIT")

        descs = {}
        for name in ("rea", "ca", "carea"):
            text = (REPO_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            descs[name] = text
        self.assertIn("without", descs["rea"].lower().replace("do not ask", "without"))
        self.assertIn("without binary decompilation", descs["ca"].lower())
        self.assertIn("combined", descs["carea"].lower())

    def test_sample_target_unit_tests_pass(self) -> None:
        res = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(REPO_ROOT / "examples" / "sample-target"), "-v"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
