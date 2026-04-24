# Sync GPT-Image-2 Prompt Library

Use this skill when the goal is to keep the GPT-Image-2 prompt source repo and the `gptimg` site repo in sync.

This skill is an orchestrator. It has two stages:

1. `source-ingest`
   Find prompt-image pairs on X, dedupe them, download local assets, and write source-repo records.
2. `site-sync`
   Import the source repo into `gptimg`, upload images to R2, generate localized JSON, validate the generated data, and stage only user-visible outputs when raw data stays private.

## Execution Boundary

Run each stage in the correct repository. Do not mix their write scopes.

- `source-ingest`
  - execute in: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`
  - writes to: source data, local assets, generated gallery outputs
- `site-sync`
  - execute in: `/Users/kkkk/Desktop/gptimg`
  - reads from: `/Users/kkkk/Desktop/awesome-gptimage2-prompts/prompts/prompts.json`
  - writes to: `gptimg` generated prompt JSON, locale JSON, uploaded R2 objects
- `publish-visible`
  - execute in: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`
  - stages only: public README, collection README, `prompts/prompts.json`, and referenced assets

## Defaults

- source repo: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`
- site repo: `/Users/kkkk/Desktop/gptimg`
- model: `gptimage2`
- platform: `x`
- mode: `incremental`
- publish mode: visible outputs only

## Inputs To Confirm Or Infer

- search theme, keyword set, or candidate source list
- whether this run is `incremental` or `rebuild`
- whether to sync to `gptimg` immediately after ingest
- whether to localize after import
- whether to stage only visible outputs

If the user does not specify, prefer:

- incremental ingest
- sync to `gptimg`
- run localization
- stage only visible outputs

## Hard Rules

- Treat `id` as the only stable record identity.
- Treat `sourceOrder` as display ordering only.
- Never build an R2 key from sorting, batch order, or scrape order.
- Preserve multi-image records as `images[]`.
- Keep English source prompt text as the canonical base version.
- Treat translations as derived data only.
- Do not publish internal raw data unless the user explicitly asks for it.
- Do not hand-edit generated outputs if a build script exists.

## Stage 1: source-ingest

Read [references/source-ingest.md](references/source-ingest.md) before acting.

Repository:

- execute from: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`

Normal flow:

1. Gather candidates from X search, internal seed lists, or trusted discovery repos.
2. Deduplicate on `post_url` against all X data layers before download.
3. Recover prompt text from the X post first, then use a trusted secondary reference only when the X page is truncated.
4. Download every accepted image into the local asset folders.
5. Write grouped records first, then flattened pair records.
6. Rebuild public outputs with `python3 scripts/build_gallery.py`.
7. Run local verification before moving to site sync.

Useful helper:

- `python3 scripts/dedupe_seed_urls.py path/to/seeds.md`

Completion standard:

- all newly accepted records are written to the source data layer
- each accepted pair points to an existing local asset file
- `python3 scripts/build_gallery.py` completes successfully
- generated source-repo outputs are refreshed:
  - `README.md`
  - `collections/gpt-image-2-prompt/README.md`
  - `prompts/prompts.json`
- no duplicate `post_url` was introduced across X data layers

## Stage 2: site-sync

Read [references/site-sync.md](references/site-sync.md) and [references/env-and-r2.md](references/env-and-r2.md) before acting.

Repository:

- execute from: `/Users/kkkk/Desktop/gptimg`

Normal flow:

1. Confirm `/Users/kkkk/Desktop/gptimg/.env.local` has the required R2 variables.
2. In `/Users/kkkk/Desktop/gptimg`, run:
   - `pnpm prompts:import:awesome-gptimage2`
   - `pnpm prompts:localize:awesome-gptimage2`
3. Validate generated outputs and environment assumptions:
   - `python3 /Users/kkkk/Desktop/awesome-gptimage2-prompts/scripts/validate_gptimg_sync.py`
4. If raw data should stay private, stage only visible outputs from the source repo:
   - `python3 scripts/stage_visible_outputs.py`

Completion standard:

- `.env.local` contains all required R2 variable names
- import finishes and rewrites:
  - `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.json`
- localization finishes and rewrites all expected locale files
- generated dataset entries are non-empty and each entry has:
  - `id`
  - `prompt`
  - at least one image URL
- validation passes via:
  - `python3 /Users/kkkk/Desktop/awesome-gptimage2-prompts/scripts/validate_gptimg_sync.py`

## Stage 3: publish-visible

Repository:

- execute from: `/Users/kkkk/Desktop/awesome-gptimage2-prompts`

Normal flow:

1. Confirm raw data is staying private.
2. Stage only the visible outputs and their referenced local assets.
3. Do not stage ignored source data files unless the user explicitly asks.

Completion standard:

- staged files include only:
  - `README.md`
  - `collections/gpt-image-2-prompt/README.md`
  - `prompts/prompts.json`
  - referenced `assets/...` files
- no missing referenced asset remains
- the repo is ready for commit/push without broken public image links

## Output Contract

Report the run as a compact summary with:

- new candidates reviewed
- new records archived
- duplicates skipped
- images downloaded
- `gptimg` outputs generated
- locales generated
- visible files staged
- validation warnings or blockers

## Failure Handling

- If prompt recovery is ambiguous, keep the record out of verified data or mark confidence honestly.
- If an image cannot be downloaded, do not publish the record.
- If R2 env is incomplete, stop before import and report the missing variable names only.
- If generated files are missing after import, stop and report the missing paths.
- If referenced visible assets are not tracked or not present, do not claim the repo is ready to publish.

## Quick Start

For an incremental X ingest followed by a live site sync:

```bash
python3 scripts/dedupe_seed_urls.py ../gptimg2_x_posts.md
python3 scripts/build_gallery.py
(cd /Users/kkkk/Desktop/gptimg && pnpm prompts:sync:awesome-gptimage2)
python3 scripts/validate_gptimg_sync.py
python3 scripts/stage_visible_outputs.py
```
