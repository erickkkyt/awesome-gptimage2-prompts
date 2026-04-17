# Contributing

This repository is curated, not auto-collected.

It now accepts GPT-Image-2 material only.

## What To Submit

- GPT-Image-2 examples from public X posts with visible prompts
- prompt-image pairs with clear attribution
- normalization improvements that make pair mapping cleaner
- secondary GPT-Image-2 references that are clearly marked as non-X

## What Not To Submit

- Nano Banana, Midjourney, Flux, or mixed-model content
- bulk-dumped social threads with no pair mapping
- prompt lists with no local image evidence
- images with no defendable source provenance

## Preferred Data Shape

For X-sourced material:

- keep one grouped source record in `data/gpt-image-2/x-discussions-verified.json` or `x-arena-likely.json`
- add one final pair record per image in `data/gpt-image-2/x-prompt-image-pairs.json`
- update [collections/gpt-image-2-prompt/README.md](./collections/gpt-image-2-prompt/README.md) when the example is worth featuring

## Review Standard

A good contribution is reusable without reopening the original tweet.

That means:

- exact prompt
- exact local image
- exact source URL
- explicit confidence level
