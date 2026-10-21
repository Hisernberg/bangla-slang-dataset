# SCHEMA — `bangla_slang_master.csv`

One row = one slang term/phrase. 20 columns, UTF-8, comma-separated, quoted.

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `id` | string | Stable ID `KS-####` (assigned after final ordering; re-sorted per release) |
| 2 | `term_bn` | string | The slang term/phrase in Bengali script (canonical, NFC-normalized) |
| 3 | `romanization` | string | Latin rendering — source-provided when available, else deterministic auto-transliteration |
| 4 | `literal_meaning` | string | Word-for-word literal sense (gold tier only; empty = not available) |
| 5 | `meaning_en` | string | English gloss. Wiktionary entries: definition text. Gold: maintainer-written |
| 6 | `meaning_bn` | string | Bengali gloss (from bn-Wiktionary or gold curation) |
| 7 | `category` | enum | One of the 10 categories — see [TAXONOMY.md](TAXONOMY.md): `regional_dhaka`, `regional_chattogram`, `regional_sylhet`, `colloquial_dialectal`, `profanity_curses`, `internet_social`, `campus_student`, `entertainment_media`, `relationships_emotions`, `social_political` |
| 8 | `region` | string | Free-text region tag, e.g. `Dhaka (Old Dhaka / urban street)`, `Chattogram`, `Bengal` |
| 9 | `part_of_speech` | string | `noun`, `verb`, `adjective`, `phrase`, `interjection`, `particle`, … (from Wiktionary POS headers or gold; empty = unknown) |
| 10 | `register` | enum | `informal` · `street` · `vulgar` · `dialect` · `humorous` · `formal_slang` |
| 11 | `offensiveness` | int | **0** neutral-colloquial · **1** mildly rude · **2** offensive · **3** severe profanity/slug |
| 12 | `usage_example_bn` | string | Bengali usage example (bn-Wiktionary `usex` templates; gold entries) |
| 13 | `usage_example_en` | string | English rendering of the example |
| 14 | `era` | enum | `classic` (pre-internet) · `modern` (2000s+) — gold tier only |
| 15 | `popularity` | int 1–5 or empty | estimated usage frequency in current social-media/urban speech (gold entries only; 5 = everyday viral, 1 = niche) |
| `tags` | string | Pipe-separated free tags: sense labels (`slang`, `vulgar`, `derogatory`, `dialectal`, `colloquial`…), cross-source notes (`also:github_dataset`), topic flags |
| 16 | `confidence` | enum | `high` (gold) · `medium` (dictionary / structured lexicon) |
| 17 | `tier` | int | 1 = gold · 2 = Wiktionary · 3 = community lexicon lists (tier 4 auto-extracts live in `data/candidates/`) |
| 18 | `source_type` | string | `gold_curated` · `wiktionary_en` · `wiktionary_bn` · `nirmol_github` · `deshi_slang_github` · `hf_chittagong_vulgar` · `web_lexicon_list` |
| 19 | `source_url` | string | Canonical provenance URL for the entry |

## Conventions

- **Empty string** means "not captured", never "none".
- `meaning_en` for many tier-3 profanity entries is the literal phrase *"severe Bangla profanity / insult (moderation lexicon term)"* — these are single-word entries whose full usage nuance requires human annotation (that's what `tier` + `confidence` communicate honestly).
- Polysemous merges: when the same Bengali term came from sources with different senses (e.g. গুয়া = "betel nut" in Sylheti *and* a vulgar term in Chittagonian), fields are unioned and the lower-tier source is recorded in `tags` as `also:<source_type>`.
- Bengali-script terms are NFC-normalized; ZWJ/ZWJ conjuncts preserved.

## Files

```
data/
├── final/
│   ├── bangla_slang_master.csv          # all 2,100 verified entries
│   ├── bangla_slang_master.json         # same, JSON array
│   ├── stats.json                       # machine-readable counts
│   └── by_category/<category>.csv       # pre-split per category
├── candidates/
│   └── web_candidates_for_annotation.*  # 75 tier-4 auto-extracts, human review pending
├── provenance/                          # parsed upstream snapshots + API probe logs
└── reference/                           # raw upstream files w/ license in filename
```

## v3.2 — crosslingual_mappings schema (18 fields)

`data/final/crosslingual_mappings.csv` — the reverse-mapping layer (slang of other languages → Bangla):

| Field | Type | Description |
|---|---|---|
| `map_id` | str | `XLM-0001` … sequential |
| `source_lang` | enum | en / en-GB / en-AU / hi / ur / ar / fa / ko / ja / es |
| `source_term` | str | slang term in the source language (original script where applicable) |
| `source_gloss_en` | str | English meaning of the source slang |
| `bangla_native_equivalent` | str | native Bangla slang carrying the same meaning |
| `bangla_codemixed_form` | str | the borrowed/code-mixed form actually used in BD speech |
| `bangla_romanization` | str | romanization of the code-mixed form |
| `mapping_process` | enum | loanword_noun · loanword_adjective · loanword_verbalized_kora/mara/khaoa/deoa · semantic_equivalent · calque · cultural_adaptation |
| `register` | enum | informal · very informal · neutral |
| `offensiveness` | int 0–3 | severity rating (same scale as master) |
| `domain` | list `;`-joined | social_media, romance, gaming, campus, workplace, street, food, sports… |
| `usage_example_banglish` | str | code-mixed example sentence as written on BD social media |
| `usage_example_pure_bn` | str | the same idea in pure Bangla |
| `example_source_lang` | str | example sentence in the source language (optional) |
| `process_note` | str | why this mapping/process was chosen; contrastive notes |
| `confidence` | enum | high / medium |
| `source_evidence` | str | Urban Dictionary top definition (`UD#<defid>: …`) where available |
| `master_link` | str | KS-id of the matching entry in the master lexicon, when present |
