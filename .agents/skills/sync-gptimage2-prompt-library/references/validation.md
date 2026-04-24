# Validation Reference

Validation must happen at both repo boundaries.

## Repository Split

- source validation runs in: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`
- site validation runs against: `/Users/kkkk/Desktop/gptimg`
- visible publish validation returns to: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`

## Source Repo Validation

Required checks:

- X `post_url` is unique across all X datasets
- each accepted pair has a non-empty prompt
- each accepted pair has a local image file
- rebuild completes successfully
- generated gallery outputs reference only local asset paths

Useful commands:

```bash
python3 scripts/build_gallery.py
python3 scripts/dedupe_seed_urls.py path/to/seeds.md
```

## Site Repo Validation

Required checks:

- `/Users/kkkk/Desktop/gptimg/.env.local` has all required R2 variable names
- generated English dataset exists
- generated locale datasets exist
- each generated entry has an `id`, `prompt`, and at least one image URL

Helper:

```bash
python3 scripts/validate_gptimg_sync.py
```

## Publish Validation

If raw data stays private, only visible outputs should be staged from the source repo:

- `README.md`
- `collections/gpt-image-2-prompt/README.md`
- `prompts/prompts.json`
- referenced local assets used by those files

Helper:

```bash
python3 scripts/stage_visible_outputs.py --dry-run
python3 scripts/stage_visible_outputs.py
```

Done means:

- the staging set contains only public deliverables and referenced assets
- all referenced asset files exist locally
- public repo consumers can see prompt text and images without needing ignored raw data

## Blocking Conditions

Do not claim success when any of these is true:

- missing required R2 env names
- missing generated JSON in `gptimg`
- missing local assets referenced by visible outputs
- prompt/image records written with unstable ids
- main R2 object key built from ordering instead of stable `id`
