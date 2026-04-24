# Site Sync Reference

This stage syncs the source repo into the site repo at:

- `/Users/kkkk/Desktop/gptimg`

## Repository Boundary

- execute in: `/Users/kkkk/Desktop/gptimg`
- reads from:
  - `/Users/kkkk/Desktop/awesome-gptimage2-prompts/prompts/prompts.json`
  - source-repo local assets referenced by that file
- writes to:
  - `src/lib/generated/awesome-gptimage2-prompts.json`
  - `src/lib/generated/awesome-gptimage2-prompts.i18n.*.json`
  - R2 objects for imported prompt images
- do not edit source-repo raw X datasets during this stage

The current site pipeline is already implemented. This skill should call the real scripts instead of re-implementing them.

## Entry Points

- `/Users/kkkk/Desktop/gptimg/scripts/import-awesome-gptimage2-prompts.ts`
- `/Users/kkkk/Desktop/gptimg/scripts/localize-awesome-gptimage2-prompts.py`

Useful package commands:

- `pnpm prompts:import:awesome-gptimage2`
- `pnpm prompts:localize:awesome-gptimage2`
- `pnpm prompts:sync:awesome-gptimage2`

## Import Behavior

Import reads from the source repo:

- `/Users/kkkk/Desktop/awesome-gptimage2-prompts/prompts/prompts.json`

Import uploads source images to R2 and writes the English generated dataset to:

- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.json`

The import schema is normalized in:

- `/Users/kkkk/Desktop/gptimg/src/lib/awesome-gptimage2-import.ts`

Key internal fields after normalization:

- `id`
- `sourceOrder`
- `title`
- `description`
- `images`
- `prompt`
- `modelId`
- `authorName`
- `authorHandle`
- `publishedLabel`
- `sourceUrl`
- `languages`

## Localization Behavior

Localization reads:

- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.json`

And writes locale maps such as:

- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.zh.json`
- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.fr.json`
- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.ru.json`
- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.pt.json`
- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.ja.json`
- `/Users/kkkk/Desktop/gptimg/src/lib/generated/awesome-gptimage2-prompts.i18n.ko.json`

## Page Consumption

The site page consumes generated data through:

- `/Users/kkkk/Desktop/gptimg/src/lib/gpt-image-2-prompts-data.ts`
- `/Users/kkkk/Desktop/gptimg/src/lib/gpt-image-2-prompt-localizations.ts`
- `/Users/kkkk/Desktop/gptimg/src/app/[locale]/(marketing)/gpt-image-2-prompts/page.tsx`
- `/Users/kkkk/Desktop/gptimg/src/components/prompts/gpt-image-2-prompts-page.tsx`

The page layer does not ingest or normalize source records. It only consumes generated outputs.

## Recommended Execution

```bash
cd /Users/kkkk/Desktop/gptimg
pnpm prompts:sync:awesome-gptimage2
python3 /Users/kkkk/Desktop/awesome-gptimage2-prompts/scripts/validate_gptimg_sync.py
```

## Done Means

This stage is complete only when:

- import succeeds against the current source-repo `prompts/prompts.json`
- generated English prompt data exists and is non-empty
- expected locale files exist
- validation passes without missing env names or missing generated files

## Important Side Branch

There is still a manual additions branch:

- `/Users/kkkk/Desktop/gptimg/scripts/import-awesome-gptimage2-site-additions.ts`

It currently uses a key pattern that still includes `sourceOrder`. Treat that as a known warning, not as the main pipeline rule.
