#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SITE_REPO = Path("/Users/kkkk/Desktop/gptimg")
ENV_PATH = SITE_REPO / ".env.local"
MAIN_GENERATED = SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.json"
LOCALE_FILES = [
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.zh.json",
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.fr.json",
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.ru.json",
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.pt.json",
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.ja.json",
    SITE_REPO / "src/lib/generated/awesome-gptimage2-prompts.i18n.ko.json",
]
REQUIRED_ENV_NAMES = [
    "R2_ENDPOINT",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_REGION",
    "R2_IMAGE_BUCKET_NAME",
    "R2_IMAGE_PUBLIC_URL",
]
ADDITIONS_IMPORTER = SITE_REPO / "scripts/import-awesome-gptimage2-site-additions.ts"


def load_env_names(path: Path) -> set[str]:
    names: set[str] = set()
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name = line.split("=", 1)[0].strip()
        if name:
            names.add(name)
    return names


def validate_generated_dataset(path: Path) -> tuple[int, list[str]]:
    data = json.loads(path.read_text())
    errors: list[str] = []
    if not isinstance(data, list) or not data:
        errors.append(f"generated dataset is empty or not a list: {path}")
        return 0, errors

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f"entry {index} is not an object")
            continue
        if not item.get("id"):
            errors.append(f"entry {index} missing id")
        if not item.get("prompt"):
            errors.append(f"entry {index} missing prompt")
        images = item.get("images")
        if not isinstance(images, list) or not images or not all(
            isinstance(url, str) and url for url in images
        ):
            errors.append(f"entry {index} missing images")
    return len(data), errors


def detect_unstable_additions_key(path: Path) -> bool:
    text = path.read_text()
    return bool(re.search(r"site-additions/.+sourceOrder|padStart\(3,\s*['\"]0['\"]\)", text))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SITE_REPO.exists():
        errors.append(f"site repo missing: {SITE_REPO}")
    if not ENV_PATH.exists():
        errors.append(f"env file missing: {ENV_PATH}")

    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        return 1

    env_names = load_env_names(ENV_PATH)
    missing_env = [name for name in REQUIRED_ENV_NAMES if name not in env_names]
    if missing_env:
        errors.append(f"missing env names: {', '.join(missing_env)}")

    if not MAIN_GENERATED.exists():
        errors.append(f"missing generated dataset: {MAIN_GENERATED}")
        entry_count = 0
    else:
        entry_count, dataset_errors = validate_generated_dataset(MAIN_GENERATED)
        errors.extend(dataset_errors)

    missing_locale_files = [str(path) for path in LOCALE_FILES if not path.exists()]
    if missing_locale_files:
        errors.append(f"missing locale files: {', '.join(missing_locale_files)}")

    if ADDITIONS_IMPORTER.exists() and detect_unstable_additions_key(ADDITIONS_IMPORTER):
        warnings.append(
            "site additions importer still uses a sourceOrder-based object path; main pipeline is stable-key based."
        )

    if warnings:
        for item in warnings:
            print(f"warning: {item}", file=sys.stderr)

    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        return 1

    print(
        f"ok generated_entries={entry_count} locales={len(LOCALE_FILES)} env_names={len(REQUIRED_ENV_NAMES)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
