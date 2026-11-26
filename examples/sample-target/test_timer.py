"""Unit tests for the self-owned pulse-timer sample target."""

from __future__ import annotations

import unittest

from server import clamp_status


class TestPulseTimer(unittest.TestCase):
    def test_paused_midpoint(self) -> None:
        self.assertEqual(
            clamp_status(60000, 18000, state="paused"),
            {"state": "paused", "duration_ms": 60000, "remaining_ms": 42000, "warning_active": False},
        )

    def test_zero_clamp_completed(self) -> None:
        self.assertEqual(
            clamp_status(10000, 15000, state="running"),
            {"state": "completed", "duration_ms": 10000, "remaining_ms": 0, "warning_active": False},
        )

    def test_invalid_duration_rejected(self) -> None:
        self.assertEqual(clamp_status(500, 0), {"error": "invalid_duration"})


if __name__ == "__main__":
    unittest.main()
