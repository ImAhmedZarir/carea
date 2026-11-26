"""Load compatibility matrix and handoff schemas from repo or bundled package data."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any


def find_repo_root(start: Path | None = None) -> Path | None:
    cur = (start or Path(__file__)).resolve()
    if cur.is_file():
        cur = cur.parent
    for parent in (cur, *cur.parents):
        if (parent / "compat" / "matrix.json").is_file() and (parent / "schemas" / "carea-handoff.schema.json").is_file():
            return parent
    return None


def load_json_text(text: str) -> Any:
    return json.loads(text.lstrip("\ufeff"))


def load_compat_matrix() -> dict[str, Any]:
    root = find_repo_root()
    if root is not None:
        return load_json_text((root / "compat" / "matrix.json").read_text(encoding="utf-8-sig"))
    data_file = resources.files("carea").joinpath("data/matrix.json")
    return load_json_text(data_file.read_text(encoding="utf-8-sig"))


def load_handoff_schema(custom_schema: Path | None = None) -> dict[str, Any]:
    if custom_schema is not None:
        return load_json_text(custom_schema.read_text(encoding="utf-8-sig"))
    root = find_repo_root()
    if root is not None:
        return load_json_text((root / "schemas" / "carea-handoff.schema.json").read_text(encoding="utf-8-sig"))
    data_file = resources.files("carea").joinpath("data/carea-handoff.schema.json")
    return load_json_text(data_file.read_text(encoding="utf-8-sig"))
