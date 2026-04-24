# Env And R2 Reference

The site repo loads R2 configuration from:

- `/Users/kkkk/Desktop/gptimg/.env.local`

Do not print secrets back to the user. Only report whether required variable names are present.

## Required Variables

- `R2_ENDPOINT`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_REGION`
- `R2_IMAGE_BUCKET_NAME`
- `R2_IMAGE_PUBLIC_URL`

## Stable Object Key Rule

The main import path is already stable-key based.

Current object prefix:

- `prompt-libraries/awesome-gptimage2-prompts`

Current main key pattern:

- `prompt-libraries/awesome-gptimage2-prompts/{id}/{filename}`

This is correct.

Never change the main prompt-library key pattern back to one that includes:

- `sourceOrder`
- scrape batch index
- temporary import ordering

## Known Warning

The site additions importer still uses a `sourceOrder`-based object path. That branch should eventually be normalized to:

- `site-additions/{id}/{filename}`

Do not copy the old additions key design into new code.
