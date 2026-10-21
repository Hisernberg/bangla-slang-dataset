# কথার রঙ · Kothar Rong — The Open Bangla Slang Dataset

**কথার রঙ** ("The Color of Speech") is an open, multi-source lexicon of **Bangla (Bengali) slang** — regional street dialects, internet meme culture, campus slang, profanity, cinema catchphrases, and the living register of everyday Bengal — organized into **10 style & regional categories** with romanization, bilingual glosses, registers, and offensiveness ratings.

> 🏁 Built as the flagship lexicon for the **ELITE Research Lab Dataset Competition 2026** (slang-dictionary special category · "Culture & Tone" priority track).

![Entries](https://img.shields.io/badge/entries-2%2C100%20verified-brightgreen) ![Categories](https://img.shields.io/badge/categories-10-blue) ![License](https://img.shields.io/badge/data%20license-CC%20BY--SA%204.0-lightgrey) ![Code](https://img.shields.io/badge/code%20license-MIT-informational) ![Romanization](https://img.shields.io/badge/romanization-100%25-success)

---

## 📊 Dataset at a glance

| | |
|---|---|
| **Verified entries** | **2,100** (+75 auto-extracted candidates queued for human annotation) |
| **Categories** | 10 (4 regional + 6 style-based) |
| **Sources** | 8+ harvested systems: Wiktionary (en+bn), GitHub, Hugging Face, Kaggle, 40+ web pages |
| **Scripts covered** | Bengali (primary) · Sylheti Nagri (reference) · Banglish Roman (documented variants) |
| **Fields per entry** | 19 — see [SCHEMA.md](SCHEMA.md) |
| **Romanization** | 100% (deterministic auto-transliteration + source-provided) |
| **English glosses** | 1,163 entries (55%) · Bengali glosses: 235 · usage examples: 62 |
| **Quality tiers** | 3-tier provenance system — see below |

## 🗂️ The 10 categories

| # | Category | বাংলা | Entries | Example |
|---|----------|-------|--------:|---------|
| 1 | `regional_dhaka` | ঢাকাইয়া | 101 | **মামা** (*mama*) — "uncle" → universal friendly address; গোল্লাছুট (*gollachhut*) — "long gone!" |
| 2 | `regional_chattogram` | চট্টগ্রামীয়া | 744 | **কেন মামা লাগব** — iconic film-origin refusal catchphrase |
| 3 | `regional_sylhet` | সিলেটি | 14 | **কিতা গরু মামা** (*kita goru mama*) — "no way!" |
| 4 | `colloquial_dialectal` | সাধারণ কথ্য ও আঞ্চলিক | 125 | general colloquial, old-school & minor-dialect slang (Noakhali, Dinajpur, Kolkata…) |
| 5 | `profanity_curses` | গালি ও অভিশাপ | 1,048 | **বোকাচোদা** (*bokachoda*) — "dumbass"; rated 0–3 for severity |
| 6 | `internet_social` | ইন্টারনেট ও সোশ্যাল মিডিয়া | 18 | **আইডি ডিলিট** — the fake-hacker threat meme; **হাহাকার** — despair meme |
| 7 | `campus_student` | ক্যাম্পাস ও ছাত্রজীবন | 15 | **সাপ্লাই** (*supply*), **রেফার** (*refer*), **কাটিং** (*cutting* — bunking class) |
| 8 | `entertainment_media` | সিনেমা-নাটক ও বিনোদন | 9 | **সিনেমা দেখিস বেশি** — "you watch too many movies" |
| 9 | `relationships_emotions` | সম্পর্ক ও আবেগ | 13 | **মন খারাপ** (*mon kharap*) — the national sadness catch-all |
| 10 | `social_political` | সামাজিক-রাজনৈতিক | 13 | **চামচা** (*chamcha*) — sycophant; **হাওয়া** (*hawa*) — political wind |

Full details and inclusion criteria: [TAXONOMY.md](TAXONOMY.md).

## 🚀 Quickstart

```python
import pandas as pd

df = pd.read_csv("data/final/bangla_slang_master.csv")
print(df.shape)                      # (2100, 19)

# all Dhakaiya street slang, ranked by offensiveness
dh = df[df.category == "regional_dhaka"].sort_values("offensiveness")
print(dh[["term_bn", "romanization", "meaning_en"]].head(10))

# category files are pre-split
sylheti = pd.read_csv("data/final/by_category/regional_sylhet.csv")
```

```json
{
  "id": "KS-0001",
  "term_bn": "মামা",
  "romanization": "mama",
  "literal_meaning": "maternal uncle",
  "meaning_en": "universal friendly address to any male peer or elder; also self-description as the \"boss\" of a situation",
  "category": "regional_dhaka",
  "region": "Dhaka (Old Dhaka / urban street)",
  "register": "informal",
  "offensiveness": 0,
  "usage_example_bn": "কী অবস্থা মামা?",
  "usage_example_en": "What's up, mama?",
  "era": "classic",
  "confidence": "high",
  "tier": 1,
  "source_type": "gold_curated"
}
```

## 🔬 Methodology

```
 ┌────────────────────────────────────────────────────────────────────┐
 │  COLLECTION (8 API systems, 40+ pages, 2.4 MB raw markdown)        │
 ├──────────────────┬───────────────────┬─────────────────────────────┤
 │ Wiktionary API   │ Firecrawl v2      │ Hugging Face Hub API        │
 │ (1,830 entries)  │ (search+scrape)   │ (Chittagonian vulgar lex.)  │
 │ GitHub API       │ Kaggle API        │ Browserbase + Playwright    │
 │ (Nirmol, deshi-  │ (43k-row corpus,  │ (JS-heavy pages, CDP)       │
 │  slang datasets) │  referenced)      │ + WebSearch/WebFetch        │
 ├──────────────────┴───────────────────┴─────────────────────────────┤
 │  PARSING: wikitext definition parser · markdown table extractor ·  │
 │  dash/colon pattern miner · junk filters (spam, infoboxes, nav)    │
 ├────────────────────────────────────────────────────────────────────┤
 │  ENRICHMENT: auto-transliteration · category classifier ·           │
 │  offensiveness mapping · register/era normalization                │
 ├────────────────────────────────────────────────────────────────────┤
 │  MERGE: NFC normalization → priority dedupe (translit-fuzzy key)   │
 │  → tier assignment → ID allocation (KS-####)                       │
 └────────────────────────────────────────────────────────────────────┘
```

### The API stack — what was used, and what happened

| API / Tool | Status | Role |
|---|---|---|
| **GitHub API** | ✅ used | located & fetched Nirmol (40★) + deshi-slang slang datasets; hosts this repo |
| **Hugging Face API** | ✅ used | pulled the Apache-2.0 Chittagonian vulgar lexicon; surveyed 180+ Bangla datasets |
| **Kaggle API** | ✅ used | surveyed slang datasets; downloaded 43k-row suspicious-text corpus (referenced) |
| **Firecrawl v2** | ✅ workhorse | 18 search queries + 15 scrapes → 100 markdown docs / 2.4 MB |
| **Browserbase + Playwright** | ✅ used | CDP-driven headless Chromium for JS-heavy/blocked pages |
| **Wiktionary / Wikipedia APIs** | ✅ used | 1,830 structured entries with wikitext sense labels |
| **ScrapeGraphAI** | ⛔ network-blocked | TLS handshake rejected from collection environment (5 attempts incl. browser-TLS routing); integration script included (`scripts/08`) |
| **Browse AI** | ⛔ auth-rejected | API key rejected (401); robots require dashboard setup |
| **CrawlForge** | ⛔ DNS-unresolvable | no such host from this network |

Every probe result is preserved in `data/provenance/api_probe_results.json` — no API was left untried.

### Quality tiers (honest provenance)

| Tier | Meaning | Count | Confidence |
|:---:|---|---:|---|
| **1** | Gold — hand-curated by maintainers, full schema, examples | 150 | `high` |
| **2** | Wiktionary (en+bn) — dictionary-verified senses with usage labels | 194 | `medium` |
| **3** | Community/lexicon lists — GitHub & HF moderation lexicons, blog lists | 1,756 | `medium` |
| — | Tier-4 web-auto-extracts | 75 | quarantined in `data/candidates/` for human review |

**Deduplication**: NFC normalization + transliteration-fuzzy keys (Bengali-script and Roman-script variants of the same term merge, e.g. `খানকির পোলা` = `Khankir pula`), highest-tier source wins fields; duplicate sources recorded in `tags`.

## ⚠️ Ethics & content warning

This dataset contains **profanity, slurs, and offensive language** — that is its scientific subject matter. Entries carry a 0–3 `offensiveness` rating and a `register` flag so downstream NLP systems can detect, filter, or study such language — **not** produce it. Do not use this dataset to harass anyone. Identity-referencing terms (e.g. হিজরা) are documented in their derogatory-slang usage with a `slur_caution` tag, reflecting descriptive linguistics, not endorsement. All content was collected from public sources; see [SOURCES.md](SOURCES.md) for full attribution.

## 🔗 Related work (the gap this fills)

| Resource | What it has | What it lacks |
|---|---|---|
| BAAD (Bangla Audio Abuse Dataset) | 114 abusive words, 6,100 audio clips | no lexicon metadata, no categories, no meanings |
| BanglaDial-Abuse / ONUBAD / BD-Dialect | dialect text corpora | not slang-organized, no bilingual glosses |
| BanglaToxicCommentsDB | 43k classified comments | usage corpus, not a dictionary |
| **Kothar Rong (this repo)** | **2,100 categorized slang entries, 19 fields, bilingual** | audio layer → roadmap |

## 📚 Citation

```bibtex
@dataset{nur2026kotharrong,
  author  = {Nabid Nur and contributors},
  title   = {Kothar Rong (কথার রঙ): The Open Bangla Slang Dataset},
  year    = {2026},
  url     = {https://github.com/Hisernberg/bangla-slang-dataset},
  note    = {2,100 verified entries, 10 style \& regional categories,
             ELITE Research Lab Dataset Competition 2026}
}
```

## 📄 License

- **Data** (`data/`): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — share-alike keeps compatibility with the Wiktionary-derived content.
- **Code** (`scripts/`): MIT.
- Upstream licenses are honored per source — see [SOURCES.md](SOURCES.md).

## 🗺️ Roadmap

1. **v1.1** — human-verify the 75 quarantined tier-4 candidates
2. **v1.2** — audio layer: 1,000 spoken pronunciations with regional accents (the "Culture & Tone" track)
3. **v1.3** — Banglish/Roman-script parallel forms for every entry
4. **v2.0** — Bengali↔English slang-to-slang translation pairs for MT evaluation

## 🙏 Acknowledgments

- [Wiktionary](https://en.wiktionary.org/) & [bn.wiktionary](https://bn.wiktionary.org/) contributors (CC BY-SA)
- [Sigmakib2/Nirmol](https://github.com/Sigmakib2/Nirmol) — community profanity lexicon
- [amirulsizan/deshi-slang](https://github.com/amirulsizan/deshi-slang) (MIT)
- [TanjimKIT — Vulgar Lexicon of Chittagonian Dialect](https://huggingface.co/datasets/TanjimKIT/Vulgar_Lexicon_of_Chittagonian_Dialect_of_Bangla_or_Bengali) (Apache-2.0)
- The ELITE Research Lab for organizing the 2026 dataset competition

*কথার রঙ — every street has its own palette.*
