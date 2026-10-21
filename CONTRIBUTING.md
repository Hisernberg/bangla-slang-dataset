# Contributing to Kothar Rong

## Add a slang entry (easiest way)

1. Open an issue using the title format: `[new-entry] বাংলা শব্দ (romanization)`
2. Include: term (Bengali script), romanization, meaning (EN and/or BN), category (from the 10 in TAXONOMY.md), region, register, offensiveness 0–3, and — if possible — a usage example.
3. A maintainer merges it into the gold tier in the next build.

## Improve existing entries

Comment on an entry via issue referencing its `KS-####` ID. Translation fixes for `meaning_en` on tier-3 entries are especially welcome (currently ~44% lack English glosses).

## Verify quarantined candidates

`data/candidates/web_candidates_for_annotation.csv` holds 75 auto-extracted web candidates awaiting human review. Reviewers: mark each `accept / reject / fix-category` in an issue. Accepted entries move to tier 3 or gold.

## Rebuild locally

```bash
pip install pandas openpyxl playwright && playwright install chromium
export GITHUB_TOKEN=... HF_TOKEN=... KAGGLE_API_TOKEN=... FIRECRAWL_API_KEY=... BROWSERBASE_API_KEY=...
bash scripts/03_firecrawl_search.sh        # web discovery
python scripts/02_harvest_wiktionary.py    # dictionary harvest
python scripts/10_parse_wiktionary.py
python scripts/11_parse_sources.py
python scripts/30_build_dataset.py         # -> data/final/
```

## Rules

- No API keys, ever (env vars only).
- Keep the 0–3 offensiveness ratings honest — descriptive, not euphemistic.
- New categories require a TAXONOMY.md proposal first.
- All additions must be verifiable: cite the source URL.
