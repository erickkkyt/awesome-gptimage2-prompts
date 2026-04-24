#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


STATUS_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:x|twitter)\.com/[A-Za-z0-9_]+/status/\d+"
)

DEFAULT_DATA_FILES = [
    Path("data/gpt-image-2/x-prompt-image-pairs.json"),
    Path("data/gpt-image-2/x-discussions-verified.json"),
    Path("data/gpt-image-2/x-arena-likely.json"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print unseen X status URLs after checking current GPT-Image-2 data."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Markdown, text, or JSON files containing candidate X URLs. Reads stdin when omitted.",
    )
    parser.add_argument(
        "--json-key",
        default="post_url",
        help="JSON key to inspect when an input file is a JSON array of objects.",
    )
    return parser.parse_args()


def load_seen_urls(paths: Iterable[Path]) -> set[str]:
    seen: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            continue
        for item in data:
            if isinstance(item, dict):
                value = item.get("post_url")
                if isinstance(value, str):
                    seen.add(value)
    return seen


def extract_urls_from_text(text: str) -> list[str]:
    return STATUS_URL_RE.findall(text)


def extract_urls_from_json(path: Path, json_key: str) -> list[str]:
    data = json.loads(path.read_text())
    urls: list[str] = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                value = item.get(json_key)
                if isinstance(value, str) and STATUS_URL_RE.fullmatch(value):
                    urls.append(value)
    return urls


def load_candidate_urls(paths: list[str], json_key: str) -> list[str]:
    if not paths:
        return extract_urls_from_text(sys.stdin.read())

    urls: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        text = path.read_text()
        if path.suffix.lower() == ".json":
            urls.extend(extract_urls_from_json(path, json_key))
            continue
        urls.extend(extract_urls_from_text(text))
    return urls


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def main() -> int:
    args = parse_args()
    seen_urls = load_seen_urls(DEFAULT_DATA_FILES)
    candidate_urls = unique_preserve_order(load_candidate_urls(args.inputs, args.json_key))
    unseen_urls = [url for url in candidate_urls if url not in seen_urls]

    for url in unseen_urls:
        print(url)

    print(
        (
            f"candidate_urls={len(candidate_urls)} "
            f"seen_urls={len(seen_urls)} "
            f"unseen_urls={len(unseen_urls)}"
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
