# Changelog

## v2.0 — The Big Expansion (2026-10-21)

**3,142 verified entries (from 2,100) · 16 categories (from 10) · 20 fields (from 19)**

### Added
- **+581 gold-curated entries** (`gold_curated_v2`) across all 16 categories with full schema: bilingual glosses, usage examples (943 total examples now), era tags, and **new `popularity` field** (1–5 social-media usage estimate; 599 entries rated).
- **6 new categories**: `banglish_codemixed`, `exclamations_interjections`, `old_school_retro`, `street_transport_market`, `cricket_sports_gaming`, `idioms_figurative`.
- **+174 terms** from kuntalojha/slangs (MIT).
- **+287 Barishal-region dialect words** mined from zmsali/bangla-dialect-normalization (Apache-2.0) with a sentence-pair diff + recurrence filter.
- **v2 collection pipelines** (7 parallel harvest jobs): GitHub repo survey (14 new repos), Hugging Face hub sampling (19 datasets), Kaggle downloads (12 corpora), Firecrawl v2 (24 searches → 87 pages), API probes re-run for ScrapeGraphAI / Browse AI / CrawlForge / Reddit (all environment-blocked, documented).
- `data/reference/`: banglawordkit slang pairs (attribution-required), six-dialect corpus (MIT), dialect-normalization README, Dwadash manifest.
- `data/provenance/`: v2 API probe results, firecrawl2 manifest, Kaggle/HF manifests.

### Changed
- SCHEMA: added `popularity` (int 1–5 or empty) — now 20 fields.
- TAXONOMY: rewritten for 16 categories with inclusion criteria.
- README: updated stats, methodology diagram, API disclosure table, related-work table, roadmap.

### Notes
- Wiktionary v2 deep-dive (idioms, Sylheti, Chittagonian categories) was rate-limited (HTTP 429/403) by Wikimedia from the collection environment; scheduled for v2.3. v1 Wiktionary data remains fully integrated.
- All API keys are used via environment variables only; no secrets in scripts.

## v1.0 — Initial Release (2026-10-21)

- 2,100 verified entries, 10 categories, 19 fields.
- Sources: Wiktionary (en+bn), Nirmol (GitHub), deshi-slang (GitHub), Chittagonian vulgar lexicon (Hugging Face, Apache-2.0), 100 markdown pages via Firecrawl, Browserbase-rendered lists, Kaggle corpus references.
- 3-tier provenance system, 150 gold-curated entries, 75 quarantined candidates.
- CC BY-SA 4.0 data / MIT code.
