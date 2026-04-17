# Awesome GPT-Image-2 Prompts

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Pairs](https://img.shields.io/badge/Pairs-46-black)
![X Posts](https://img.shields.io/badge/X%20Posts-33-black)
![Model](https://img.shields.io/badge/Model-GPT--Image--2-black)
![Mapping](https://img.shields.io/badge/Image--Prompt-1%3A1-success)
![License](https://img.shields.io/badge/License-CC0-lightgrey)

> A GPT-Image-2-only prompt library built around one rule: one local image, one visible prompt, one source record.

This repository no longer mixes models.

Current snapshot date: 2026-04-17.

The scope is now intentionally narrow:

- GPT-Image-2 prompt-image pairs from X
- GPT-Image-2 secondary web examples kept as reference only
- a flattened one-image-to-one-prompt dataset that is easier to reuse downstream

## What Is Here

- [GPT-Image-2 X Prompt Pairs](./collections/gpt-image-2-prompt/README.md): browse layer
- [Flattened X dataset](./data/gpt-image-2/x-prompt-image-pairs.json): 46 one-to-one records
- [Grouped X source records](./data/gpt-image-2/x-discussions-verified.json): 32 verified post-level records
- [Arena-likely X sample](./data/gpt-image-2/x-arena-likely.json): 1 lower-confidence pair
- [Secondary web examples](./data/gpt-image-2/web-examples-secondary.json): 16 non-X reference items

## Latest Sweep

The repository now explicitly covers the newest pull window from `2026-04-15` to `2026-04-17`:

- 20 verified X posts in that date range
- 22 prompt-image pairs in that date range
- direct prompt text in post body whenever possible
- one OCR-assisted case where the prompt appeared in an attached screenshot
- five same-thread cases where the full prompt lived in the author's reply thread

## Cover Gallery

| 1 | 2 | 3 |
| --- | --- | --- |
| [![Modern SaaS Homepage Design Boards](./assets/gpt-image-2-x-discussions/modern-saas-homepage-design-boards-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) | [![Douyin Tiktok Convenience Store Portrait](./assets/gpt-image-2-x-discussions/douyin-tiktok-convenience-store-portrait-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) | [![White Studio Tennis Editorial Portrait](./assets/gpt-image-2-x-discussions/white-studio-tennis-editorial-portrait-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) |
| [![Amalfi Coast Vintage Travel Poster](./assets/gpt-image-2-x-discussions/amalfi-coast-vintage-travel-poster-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) | [![Tim Cook Apple Park Keynote](./assets/gpt-image-2-x-discussions/tim-cook-apple-park-keynote-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) | [![Uesugi Kenshin Japanese X Profile Page](./assets/gpt-image-2-x-discussions/uesugi-kenshin-japanese-x-profile-page-1.jpg)](./collections/gpt-image-2-prompt/README.md#latest-additions-2026-04-15-to-2026-04-17) |

## Data Model

The repository now has two layers:

- browse layer: curated Markdown gallery for humans
- truth layer: flat JSON records where each entry is exactly one image and one prompt

That means multi-image X posts are normalized into multiple pair records rather than one grouped blob.

## Why This Shape

Most social prompt collections fail in one of two ways:

- they keep screenshots and lose the exact prompt mapping
- they keep the post-level thread but make downstream reuse harder

This repo keeps both:

- grouped source files for provenance
- pair-level records for production reuse

## Sourcing Rule

We only publish pairs when the prompt is visible in or confidently attributable to the original X post.

If a post contains three generated images from one prompt, it becomes three pair records.

The sourcing rule is documented inline in this README and enforced in the JSON records.

## Repository Structure

```text
awesome-gptimage2-prompts/
  README.md
  assets/
    gpt-image-2-x-discussions/
    gpt-image-2-x-arena-likely/
    gpt-image-2-web-examples/
  collections/
    gpt-image-2-prompt/
      README.md
  data/
    gpt-image-2/
      README.md
      x-prompt-image-pairs.json
      x-discussions-verified.json
      x-arena-likely.json
      web-examples-secondary.json
```

## Contributing

Contributions are welcome, but the bar is strict:

- GPT-Image-2 only
- source-first attribution
- visible or defensibly mapped prompts
- one image per final pair record

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before adding new items.
