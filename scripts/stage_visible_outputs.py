#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


DEFAULT_VISIBLE_FILES = [
    Path("README.md"),
    Path("collections/gpt-image-2-prompt/README.md"),
    Path("prompts/prompts.json"),
]

ASSET_PATH_RE = re.compile(r"assets/[A-Za-z0-9_./-]+\.(?:png|jpg|jpeg|webp|gif)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage public prompt-library outputs and the local assets they reference."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the files that would be staged without running git add.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Visible output files to inspect. Defaults to the standard public outputs.",
    )
    return parser.parse_args()


def collect_markdown_assets(path: Path) -> set[Path]:
    return {Path(match) for match in ASSET_PATH_RE.findall(path.read_text())}


def collect_prompt_assets(path: Path) -> set[Path]:
    assets: set[Path] = set()
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        return assets
    for item in data:
        if not isinstance(item, dict):
            continue
        for key in ("image", "images"):
            value = item.get(key)
            if isinstance(value, str) and value.startswith("assets/"):
                assets.add(Path(value))
            elif isinstance(value, list):
                for part in value:
                    if isinstance(part, str) and part.startswith("assets/"):
                        assets.add(Path(part))
    return assets


def run_git_add(paths: list[Path]) -> None:
    cmd = ["git", "add", "--"] + [str(path) for path in paths]
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()
    visible_files = [Path(item) for item in args.files] if args.files else DEFAULT_VISIBLE_FILES
    missing_files = [path for path in visible_files if not path.exists()]
    if missing_files:
        for path in missing_files:
            print(f"missing visible file: {path}", file=sys.stderr)
        return 1

    staged_paths: set[Path] = set(visible_files)
    for path in visible_files:
        if path.suffix.lower() == ".json":
            staged_paths.update(collect_prompt_assets(path))
        else:
            staged_paths.update(collect_markdown_assets(path))

    missing_assets = sorted(path for path in staged_paths if not path.exists())
    if missing_assets:
        for path in missing_assets:
            print(f"missing referenced asset: {path}", file=sys.stderr)
        return 1

    ordered_paths = sorted(staged_paths)
    if args.dry_run:
        for path in ordered_paths:
            print(path)
        return 0

    run_git_add(ordered_paths)
    print(f"staged_paths={len(ordered_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
