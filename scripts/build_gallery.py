from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
PAIRS_PATH = ROOT / "data" / "gpt-image-2" / "x-prompt-image-pairs.json"
ROOT_README_PATH = ROOT / "README.md"
COLLECTION_README_PATH = ROOT / "collections" / "gpt-image-2-prompt" / "README.md"
PROMPTS_JSON_PATH = ROOT / "prompts" / "prompts.json"
IMAGE_SIZE_CACHE: dict[str, tuple[int, int]] = {}


def load_pairs() -> list[dict]:
    pairs = json.loads(PAIRS_PATH.read_text())
    pairs.sort(key=lambda item: item.get("slug", ""))
    pairs.sort(key=lambda item: item.get("published_at", ""), reverse=True)
    return pairs


def make_title(slug: str) -> str:
    base = re.sub(r"-\d+$", "", slug)
    return base.replace("-", " ").title()


def truncate_prompt(prompt: str, limit: int = 140) -> str:
    single_line = " ".join(prompt.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3].rstrip() + "..."


def format_published_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"


def relative_image_path(local_image: str, depth: int = 0) -> str:
    prefix = "../" * depth
    return f"{prefix}{local_image}"


def image_dimensions(local_image: str) -> tuple[int, int]:
    if local_image not in IMAGE_SIZE_CACHE:
        with Image.open(ROOT / local_image) as img:
            IMAGE_SIZE_CACHE[local_image] = img.size
    return IMAGE_SIZE_CACHE[local_image]


def image_aspect_ratio(local_image: str) -> float:
    width, height = image_dimensions(local_image)
    return width / height


def group_slug(slug: str) -> str:
    return re.sub(r"-\d+$", "", slug)


def aggregate_confidence(values: list[str]) -> str:
    if any(value == "medium" for value in values):
        return "medium"
    return values[0]


def detect_languages(prompt: str) -> list[str]:
    languages = []

    if re.search(r"[\u3040-\u30ff]", prompt):
        languages.append("ja")
    if re.search(r"[\uac00-\ud7af]", prompt):
        languages.append("ko")
    if re.search(r"[\u4e00-\u9fff]", prompt) and "ja" not in languages:
        languages.append("zh")
    if re.search(r"[\u0400-\u04ff]", prompt):
        languages.append("ru")
    if re.search(r"[\u0600-\u06ff]", prompt):
        languages.append("ar")

    latin_words = re.findall(r"\b[A-Za-z]{2,}\b", prompt)
    if latin_words and not languages:
        languages.append("en")
    elif latin_words and "en" not in languages:
        languages.append("en")

    return languages or ["en"]


def group_source_items(items: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    ordered_keys: list[str] = []

    for item in items:
        source_group = item["source_group"]
        if source_group not in grouped:
            grouped[source_group] = {
                "id": source_group,
                "source_group": source_group,
                "slug": group_slug(item["slug"]),
                "source_type": item["source_type"],
                "post_url": item["post_url"],
                "author_name": item["author_name"],
                "author_handle": item["author_handle"],
                "published_at": item["published_at"],
                "prompt": item["prompt"],
                "prompt_visibility": item["prompt_visibility"],
                "mapping_confidence_values": [item["mapping_confidence"]],
                "model_confidence_values": [item.get("model_confidence", "high")],
                "notes": item.get("notes", ""),
                "image_urls": [item["image_url"]],
                "local_images": [item["local_image"]],
                "pair_ids": [item["id"]],
            }
            ordered_keys.append(source_group)
            continue

        group = grouped[source_group]
        group["mapping_confidence_values"].append(item["mapping_confidence"])
        group["model_confidence_values"].append(item.get("model_confidence", "high"))
        group["image_urls"].append(item["image_url"])
        group["local_images"].append(item["local_image"])
        group["pair_ids"].append(item["id"])

    grouped_items = []
    for key in ordered_keys:
        item = grouped[key]
        item["mapping_confidence"] = aggregate_confidence(item.pop("mapping_confidence_values"))
        item["model_confidence"] = aggregate_confidence(item.pop("model_confidence_values"))
        item["image_count"] = len(item["local_images"])
        item["primary_image"] = item["local_images"][0]
        item["primary_aspect_ratio"] = image_aspect_ratio(item["primary_image"])
        item["languages"] = detect_languages(item["prompt"])
        grouped_items.append(item)

    return grouped_items


def select_cover_items(items: list[dict], limit: int = 9) -> list[dict]:
    def score(item: dict) -> tuple[float, str]:
        ratio = item["primary_aspect_ratio"]
        cover_target = 1.0
        penalty = abs(ratio - cover_target)
        if ratio < 0.7:
            penalty += 0.35
        if ratio > 1.8:
            penalty += 0.2
        return (penalty, item["slug"])

    picked = sorted(items, key=score)[:limit]
    picked.sort(key=lambda item: item["published_at"], reverse=True)
    return picked


def render_image_tag(local_image: str, alt: str, depth: int = 0, width: int | None = None) -> str:
    image = relative_image_path(local_image, depth)
    if width is None:
        return f'<img src="{image}" alt="{alt}">'
    return f'<img src="{image}" alt="{alt}" width="{width}">'


def build_cover_gallery(items: list[dict], depth: int = 0, link_prefix: str = "#") -> str:
    rows = []
    cover_items = select_cover_items(items, limit=9)
    for start in range(0, len(cover_items), 3):
        cells = []
        for item in cover_items[start : start + 3]:
            title = make_title(item["slug"])
            anchor = f"{link_prefix}{item['slug']}"
            image_tag = render_image_tag(item["primary_image"], title, depth=depth, width=280)
            cells.append(f'<a href="{anchor}">{image_tag}</a>')
        while len(cells) < 3:
            cells.append(" ")
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(
        [
            "| 1 | 2 | 3 |",
            "| --- | --- | --- |",
            *rows,
        ]
    )


def single_image_width(local_image: str) -> int:
    ratio = image_aspect_ratio(local_image)
    if ratio < 0.45:
        return 240
    if ratio < 0.7:
        return 360
    if ratio < 1.0:
        return 440
    if ratio < 1.4:
        return 540
    return 620


def build_image_gallery(local_images: list[str], title: str, depth: int = 0) -> str:
    if len(local_images) == 1:
        width = single_image_width(local_images[0])
        return render_image_tag(local_images[0], title, depth=depth, width=width)

    columns = min(3, len(local_images))
    rows = ["| " + " | ".join(f"View {index}" for index in range(1, columns + 1)) + " |"]
    rows.append("| " + " | ".join("---" for _ in range(columns)) + " |")

    for start in range(0, len(local_images), columns):
        cells = []
        for index, image_path in enumerate(local_images[start : start + columns], start=start + 1):
            cells.append(render_image_tag(image_path, f"{title} {index}", depth=depth, width=220))
        while len(cells) < columns:
            cells.append(" ")
        rows.append("| " + " | ".join(cells) + " |")

    return "\n".join(rows)


def build_prompt_blocks(items: list[dict], depth: int = 0) -> str:
    blocks = []
    for index, item in enumerate(items, start=1):
        title = make_title(item["slug"])
        image_gallery = build_image_gallery(item["local_images"], title, depth)
        author_name = item["author_name"]
        author_handle = item["author_handle"]
        author_profile = f"https://x.com/{author_handle}"
        source = item["post_url"]
        published = format_published_date(item["published_at"])
        languages = ", ".join(item["languages"])
        prompt = item["prompt"].strip()
        blocks.append(
            "\n".join(
                [
                    f"### #{index} {title}",
                    "",
                    image_gallery,
                    "",
                    f"- **Author:** [{author_name}]({author_profile})",
                    f"- **Source:** [X]({source})",
                    f"- **Published:** {published}",
                    f"- **Languages:** {languages}",
                    "",
                    "<details>",
                    "<summary>Copy Prompt</summary>",
                    "",
                    "```text",
                    prompt,
                    "```",
                    "",
                    "</details>",
                    "",
                    "---",
                ]
            )
        )
    return "\n\n".join(blocks)


def export_prompts_json(items: list[dict]) -> None:
    exported = []
    for index, item in enumerate(items, start=1):
        exported.append(
            {
                "index": index,
                "id": item["id"],
                "prompt": item["prompt"],
                "author": item["author_handle"],
                "author_name": item["author_name"],
                "image": item["primary_image"],
                "images": item["local_images"],
                "image_count": item["image_count"],
                "model": "gpt-image-2",
                "date": item["published_at"],
                "published": format_published_date(item["published_at"]),
                "languages": item["languages"],
                "source": "X",
                "source_url": item["post_url"],
                "pair_ids": item["pair_ids"],
            }
        )

    PROMPTS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPTS_JSON_PATH.write_text(json.dumps(exported, ensure_ascii=False, indent=2) + "\n")


def build_root_readme(items: list[dict]) -> str:
    generated_on = date.today().isoformat()
    total = len(items)
    grouped_items = group_source_items(items)
    source_posts = len(grouped_items)
    gallery_pairs = sum(item["image_count"] for item in grouped_items)
    latest_date = max(item["published_at"] for item in items)
    cover_gallery = build_cover_gallery(grouped_items, depth=0, link_prefix="#")
    prompt_blocks = build_prompt_blocks(grouped_items, depth=0)
    recent_titles = "\n".join(
        f"- `{make_title(item['slug'])}`: {truncate_prompt(item['prompt'])}"
        for item in grouped_items[:6]
    )
    return "\n".join(
        [
            "<!-- Generated by scripts/build_gallery.py -->",
            "# Awesome GPT-Image-2 Prompts",
            "",
            "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
            f"![Pairs](https://img.shields.io/badge/Pairs-{total}-black)",
            "![Model](https://img.shields.io/badge/Model-GPT--Image--2-black)",
            "",
            f"> Scroll through {source_posts} source-post cards and {gallery_pairs} curated GPT-Image-2 results, open any card, and copy the prompt directly into your own image workflow.",
            "",
            f"Gallery build date: {generated_on}. Latest source post date: {latest_date}.",
            "",
            "[Browse Collection](./collections/gpt-image-2-prompt/README.md) • [Download JSON](./prompts/prompts.json)",
            "",
            "## What This Repo Is For",
            "",
            "This repository is designed for one behavior: see an image effect you like, open the prompt, copy it, and run your own GPT-Image-2 generation.",
            "",
            "The homepage is intentionally long and visual so GitHub visitors can keep scrolling through real examples instead of reading a short description and bouncing.",
            "",
            "## How To Use It",
            "",
            "1. Scroll until you find an image effect you want to recreate.",
            "2. Open `Copy Prompt` under that card.",
            "3. Copy the full prompt into GPT-Image-2 and adapt the subject if needed.",
            "",
            "## Stats",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Source-post cards | {source_posts} |",
            f"| Prompt-image pairs | {total} |",
            "",
            "## Recent Highlights",
            "",
            recent_titles,
            "",
            "## Cover Gallery",
            "",
            cover_gallery,
            "",
            "## Browse Prompts",
            "",
            prompt_blocks,
            "",
        ]
    )


def build_collection_readme(items: list[dict]) -> str:
    generated_on = date.today().isoformat()
    grouped_items = group_source_items(items)
    total = len(grouped_items)
    latest_date = max(item["published_at"] for item in items)
    cover_gallery = build_cover_gallery(
        grouped_items,
        depth=2,
        link_prefix="../../README.md#",
    )
    return "\n".join(
        [
            "<!-- Generated by scripts/build_gallery.py -->",
            "# GPT-Image-2 Prompt Collection",
            "",
            f"This collection mirrors the main GitHub gallery and currently contains {total} source-post prompt cards.",
            "",
            f"Gallery build date: {generated_on}. Latest source post date: {latest_date}.",
            "",
            "[Open Homepage Gallery](../../README.md) • [Download JSON](../../prompts/prompts.json)",
            "",
            "## Cover Gallery",
            "",
            cover_gallery,
            "",
            "## Notes",
            "",
            "- The root README is the main browsing surface.",
            "- `prompts/prompts.json` is the copy-friendly export.",
            "- The raw ingest layer remains local-only and is not part of the public browsing surface.",
            "",
        ]
    )


def main() -> None:
    items = load_pairs()
    ROOT_README_PATH.write_text(build_root_readme(items) + "\n")
    COLLECTION_README_PATH.write_text(build_collection_readme(items) + "\n")
    export_prompts_json(group_source_items(items))


if __name__ == "__main__":
    main()
