# GPT-Image-2 Data

This directory contains both source-ingest files and final reuse files.

## Files

- `x-prompt-image-pairs.json`: flattened one-image-to-one-prompt X dataset
- `x-discussions-verified.json`: grouped verified X-source records
- `x-arena-likely.json`: grouped lower-confidence arena-stage X records
- `web-examples-secondary.json`: non-X secondary references

## Field Intent

Use `x-prompt-image-pairs.json` when you need a direct prompt-image mapping.

Use grouped X files when you need provenance from the original post layout.

Use `web-examples-secondary.json` only as a secondary reference layer.
