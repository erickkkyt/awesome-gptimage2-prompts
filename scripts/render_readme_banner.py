from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = Path("/Users/kkkk/Desktop/1.png")
OUT_PATH = ROOT / "assets" / "readme-gpt-image-2-prompts-cover.png"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            ]
        )
    candidates.extend(
        [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        ]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def add_background_pattern(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    draw.rectangle(box, fill=(8, 22, 30))
    pattern = "GPTIMAGE2PROMPTS"
    pattern_font = font(22, bold=True)
    colors = [(31, 61, 67), (45, 71, 54), (55, 45, 74)]
    for y in range(y1 + 8, y2, 30):
        offset = -((y // 30) % 9) * 18
        for x in range(x1 + offset, x2 + 160, 168):
            draw.text((x, y), pattern, fill=colors[(x // 168 + y // 30) % len(colors)], font=pattern_font)


def main() -> None:
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(SOURCE_PATH)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    base = Image.open(SOURCE_PATH).convert("RGB")

    # Shift the original brown-black background toward a cooler README-friendly tone.
    tint = Image.new("RGB", base.size, (0, 34, 48))
    base = Image.blend(base, tint, 0.26)

    draw = ImageDraw.Draw(base)
    width, height = base.size

    # Remove the original external-provider footer and model CTA area.
    add_background_pattern(draw, (0, 850, width, height))

    # Replace it with repo-native gallery messaging.
    cta = "BROWSE 255 PROMPT-IMAGE PAIRS"
    cta_font = font(64, bold=True)
    bbox = draw.textbbox((0, 0), cta, font=cta_font)
    draw.text(((width - (bbox[2] - bbox[0])) // 2, 955), cta, fill=(246, 250, 252), font=cta_font)

    # Add a compact footer that belongs to this repository, not an external platform.
    footer = "OPEN PROMPTS  -  COPY TEXT  -  REMIX WITH GPT-IMAGE-2"
    footer_font = font(42, bold=True)
    footer_bbox = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text(((width - (footer_bbox[2] - footer_bbox[0])) // 2, 1195), footer, fill=(236, 244, 242), font=footer_font)

    # Keep the source aspect ratio. GitHub scales it cleanly as a full-width README banner.
    base.save(OUT_PATH)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
