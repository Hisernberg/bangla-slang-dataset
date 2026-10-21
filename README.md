# কথার রঙ · Kothar Rong — The Open Bangla Slang Dataset

**কথার রঙ** ("The Color of Speech") is an open, multi-source lexicon of **Bangla (Bengali) slang** — regional street dialects, internet meme culture, campus slang, profanity, cinema catchphrases, street-and-bazaar language, sports & gaming banter, idioms, and the living register of everyday Bengal — organized into **16 style & regional categories** with romanization, bilingual glosses, registers, offensiveness ratings, era tags and popularity estimates.

> 🏁 Built as the flagship lexicon for the **ELITE Research Lab Dataset Competition 2026** (slang-dictionary special category · "Culture & Tone" priority track).

![Entries](https://img.shields.io/badge/entries-3%2C174%20verified-brightgreen) ![Categories](https://img.shields.io/badge/categories-16-blue) ![Gold](https://img.shields.io/badge/gold%20curated-742-gold) ![Audio](https://img.shields.io/badge/audio%20clips-230-red) ![Corpus](https://img.shields.io/badge/usage%20corpus-2.9K%20docs-purple) ![Examples](https://img.shields.io/badge/usage%20examples-943-success) ![License](https://img.shields.io/badge/data%20license-CC%20BY--SA%204.0-lightgrey) ![Code](https://img.shields.io/badge/code%20license-MIT-informational) ![Romanization](https://img.shields.io/badge/romanization-100%25-success)

---

## 📊 Dataset at a glance

| | |
|---|---|
| **Verified entries** | **3,174** (+10,000+ auto-extracted candidates quarantined for human annotation) |
| **Categories** | 16 (4 regional + 12 style/usage-based) |
| **Gold-curated entries** | 742 with full schema (meaning, gloss, example, register, era, popularity) |
| **Sources** | 18+ harvested systems: Wiktionary (en+bn), GitHub, Hugging Face, Kaggle, Firecrawl, Browserbase, YouTube Data API, Supadata, Tavily, LRCLIB, Telegram public channels, 240+ web pages |
| **🎧 Audio layer** | **230 Edge-TTS clips** (bn-BD Nabanita/Pradeep neural voices) of high-popularity entries + 100 real-speech transcripts (`data/audio/`) |
| **📄 Usage corpus** | 2,597 YouTube comments · 8 Bangla video transcripts · 66 song lyrics · 37 Telegram meme messages · 86 news headlines (`data/corpus/`) |
| **Scripts covered** | Bengali (primary) · Sylheti Nagri (reference) · Banglish Roman (documented variants) |
| **Fields per entry** | 20 — see [SCHEMA.md](SCHEMA.md) |
| **Romanization** | 100% (deterministic auto-transliteration + source-provided) |
| **English glosses** | 2,033 entries (65%) · Bengali glosses: 820 · **usage examples: 943** |
| **Popularity estimates** | 599 entries rated 1–5 for social-media usage frequency |
| **Quality tiers** | 3-tier provenance system — see below |

## 🗂️ The 16 categories

| # | Category | বাংলা | Entries | Example |
|---|----------|-------|--------:|---------|
| 1 | `regional_dhaka` | ঢাকাইয়া | 123 | **মামা** (*mama*) — universal friendly address; **টোকাই** (*tokai*) — Old Dhaka street urchin |
| 2 | `regional_chattogram` | চট্টগ্রামীয়া | 744 | **কেন মামা লাগব** — iconic film-origin refusal catchphrase |
| 3 | `regional_sylhet` | সিলেটি | 77 | **কিতা গরু মামা** (*kita goru mama*) — "no way!"; **বাইল** (*bail*) — rice; **ꠡꠣꠉꠔꠝ꠆** (*shagotom*, Sylheti Nagri script) — welcome |
| 4 | `colloquial_dialectal` | সাধারণ কথ্য ও আঞ্চলিক | 562 | general colloquial & minor-dialect slang incl. **287 Barishal-region dialect words** (আইজ, মোর, মনডা…) |
| 5 | `profanity_curses` | গালি ও অভিশাপ | 1,080 | **বোকাচোদা** (*bokachoda*) — "dumbass"; rated 0–3 for severity |
| 6 | `internet_social` | ইন্টারনেট ও সোশ্যাল মিডিয়া | 78 | **এয়ার মারা** (*air mara*) — leave on read; **রিয়েল মারা** — "I'm dead!"; **ফোটা দেওয়া** — expose someone |
| 7 | `campus_student` | ক্যাম্পাস ও ছাত্রজীবন | 52 | **সাপ্লাই** (*supply*), **ক্যারি খাওয়া** — carry a failed course, **প্রথম সালাম** — freshman greeting ritual |
| 8 | `entertainment_media` | সিনেমা-নাটক ও বিনোদন | 38 | **ওভার অ্যাকশন**, **মুখ ওস্তাদ** — all-talk show-off, **ফার্স্ট ডে ফার্স্ট শো** cult fan |
| 9 | `relationships_emotions` | সম্পর্ক ও আবেগ | 63 | **পাতনা** (*patna*) — make-up after a fight; **মান করা** — sulking; **মুড অফ** |
| 10 | `social_political` | সামাজিক-রাজনৈতিক | 51 | **হাওয়া খাওয়া** — vanish after political fall; **ভোট খাওয়া** — steal votes; **এক পয়েন্ট এক দাবি** |
| 11 | `banglish_codemixed` | বাংলিশ (কোড-মিক্সড) | 80 | **ভাইব** (*vibe*), **ইস্যু করা** — pick a fight, **সেটিং হওয়া** — pre-arranged fix, **লাইন মারা** — flirt |
| 12 | `exclamations_interjections` | আবেগপ্রকাশক ধ্বনি | 59 | **আব্বা মাগো!**, **বাহ্** (bravo!), **থাক গে** (forget it!), **ইসsh**, **ধুর** |
| 13 | `old_school_retro` | পুরান দিনের স্ল্যাং | 33 | **বেশ জিনিস!**, **জোস**, **ডিস্কো পোলা**, **বাহারি**, **স্টেরিও পোলা** |
| 14 | `street_transport_market` | রাস্তা-বাজার-বাহন | 51 | **জায়গা আছে!** — bus cry; **ফেরি দেওয়া** — pass the fare; **রেসের বাস** — racing bus; **দালাল পোলা** |
| 15 | `cricket_sports_gaming` | ক্রিকেট-খেলা-গেমিং | 36 | **খেলা হবে!** — game on!; **টেপা ক্রিকেট** — tape-ball cricket; **র‍্যাংক খাওয়া** — lose rank |
| 16 | `idioms_figurative` | বাগধারা ও রূপক | 45 | **ঢোল পিটানো** — beat your own drum; **চোখে ধুলো দেওয়া** — deceive; **আগুনে ঘি ঢালা** |

Full details and inclusion criteria: [TAXONOMY.md](TAXONOMY.md).

## 🚀 Quickstart

```python
import pandas as pd

df = pd.read_csv("data/final/bangla_slang_master.csv")
print(df.shape)                      # (3142, 20)

# all Dhakaiya street slang, ranked by offensiveness
dh = df[df.category == "regional_dhaka"].sort_values("offensiveness")
print(dh[["term_bn", "romanization", "meaning_en"]].head(10))

# Gen-Z internet slang with popularity ratings
genz = df[(df.category == "internet_social") & (df.popularity >= 4)]

# category files are pre-split
sylheti = pd.read_csv("data/final/by_category/regional_sylhet.csv")
barishal_dialect = df[df.region == "Barishal"]
```

```json
{
  "id": "KS-0732",
  "term_bn": "এয়ার মারা",
  "romanization": "air mara",
  "literal_meaning": "to air",
  "meaning_en": "publicly ignore someone — unread message, blank look",
  "category": "internet_social",
  "region": "Nationwide (urban, social media)",
  "register": "informal",
  "offensiveness": 0,
  "usage_example_bn": "মেসেজ দিছি তারে, পুরা এয়ার মারছে",
  "usage_example_en": "I messaged him, he totally aired me",
  "era": "2020s",
  "popularity": 5,
  "confidence": "high",
  "tier": 1,
  "source_type": "gold_curated_v2"
}
```

## 🎧 v3.0 Media & Corpus Layers (new)

v3.0 extends the lexicon with **multi-modal layers** collected via the user-provided API stack (YouTube Data API v3, Supadata, Tavily, Firecrawl) plus keyless pipelines (Edge-TTS, LRCLIB, Telegram web previews, RSS, Hugging Face):

| Layer | Contents | Path | Licenses / ToS basis |
|-------|----------|------|----------------------|
| **TTS audio** | 230 MP3 clips of high-popularity entries, 2 Bangladeshi neural voices (bn-BD-Nabanita / bn-BD-Pradeep), per-clip manifest with durations | `data/audio/kothar_rong_tts/` | Generated — no copyright |
| **Real-speech transcripts** | 100 Bangla speech segments (Banglavision TV) with speaker IDs & durations | `data/audio/speech_samples/` | HF `ragibhasan/bangla_speech_corpus_v1` (attribution) |
| **YouTube comments** | 2,597 comments from 30 top-viewed Bangla videos (up to 56M views) — live slang in the wild | `data/corpus/youtube/comments_bn.jsonl` | Public data via YouTube Data API ToS |
| **Video metadata** | 354 Bangla videos (comedy, standup, dialect, street interviews, rap, stadium chants) with views/likes/tags | `data/corpus/youtube/videos_bn.csv` | YouTube Data API ToS |
| **Transcripts** | 8 full Bangla video transcripts (drama/comedy dialogue, ~40K chars) | `data/corpus/youtube/transcripts_bn.jsonl` | Supadata API |
| **Song lyrics** | 66 Bangla tracks incl. Bangla rap (Black Zang etc.), rock, film songs (~69K chars) | `data/corpus/lyrics/lrclib_lyrics_bn.jsonl` | LRCLIB open lyrics DB |
| **Telegram memes** | 37 public messages from 7 Bangla meme channels | `data/corpus/telegram/messages_bn.jsonl` | Public t.me/s/ previews |
| **News headlines** | 86 headlines (BBC Bangla, Prothom Alo) — mainstream reference register | `data/corpus/news_rss/headlines_bn.csv` | Public RSS |
| **Mined candidates** | 400 frequency-verified corpus terms awaiting annotation | `data/candidates/v3_corpus_candidates.csv` | — |
| **Full provenance** | Per-source manifest + blocked-source log (yt-dlp bot-wall, HF viewer overload, Telegram api_id missing) | `data/provenance/v3_harvest_manifest.json` | — |

**New v3 entries (+32):** Kolkata/Indian-Bengali slang (পন্ড পাকা, ঘ্যামা, টেনশন নিও না…), Wiktionary slang-category term (ওলানচাষী), 6 usage-counted Noakhali political gaalis (2016 viral audio), 14 **Sylheti Nagri-script** phrases (ꠡꠣꠉꠔꠝ꠆, ꠀꠃꠇ꠆ꠇꠣ…), 5 corpus-mined dialect verbs (ছাইরা দিল, বেইচা কামাইছে, হেরা কতো, হাই লেভেল, পুরা ফিদা).

## 🔬 Methodology

```
 ┌───────────────────────────────────────────────────────────────────────────┐
 │  COLLECTION v2.0 — 7 parallel harvest pipelines, 130+ pages               │
 ├────────────────────┬──────────────────────┬───────────────────────────────┤
 │ Wiktionary API     │ Firecrawl v2         │ Hugging Face Hub API          │
 │ (1,830 v1 + v2     │ (24 searches → 87    │ (19 datasets sampled;         │
 │  categories)       │  markdown pages)     │  dialect-normalization mined) │
 │ GitHub API         │ Kaggle API           │ Browserbase + Playwright      │
 │ (16 slang/dialect  │ (12 corpora: hate,   │ (JS-heavy pages, CDP)         │
 │  repos surveyed)   │  dialect, sentiment) │ + WebSearch/WebFetch          │
 ├────────────────────┴──────────────────────┴───────────────────────────────┤
 │  PARSING: wikitext sense parser · markdown table/dash extractors ·        │
 │  JS-array wordlist parser · sentence-pair diff miner · junk filters       │
 ├───────────────────────────────────────────────────────────────────────────┤
 │  ENRICHMENT: auto-transliteration · 16-way category classifier ·          │
 │  offensiveness mapping · register/era normalization · popularity (1–5)    │
 ├───────────────────────────────────────────────────────────────────────────┤
 │  MERGE: NFC normalization → priority dedupe (translit-fuzzy key)          │
 │  → tier assignment → stable ID allocation (KS-####)                       │
 └───────────────────────────────────────────────────────────────────────────┘
```

### The API stack — what was used, and what happened

| API / Tool | Status | Role |
|---|---|---|
| **GitHub API** | ✅ used | v1: Nirmol (40★) + deshi-slang · v2: 14 additional slang/dialect repos surveyed (Kuntalojha slangs MIT, BanglaWordKit, Six-Dialect MIT, Dwadash Apache-2.0, Setu…); hosts this repo |
| **Hugging Face API** | ✅ used | v1: Chittagonian vulgar lexicon (Apache-2.0) · v2: 19 datasets sampled; **bangla-dialect-normalization (Apache-2.0) → 287 dialect words with region tags** |
| **Kaggle API** | ✅ used | v2: 12 corpora downloaded (hate speech, political comments, SentNoB, dialect "bleach" corpus, microblog lexicons) |
| **Firecrawl v2** | ✅ workhorse | v1: 18 searches · v2: 24 searches (Bangla+English) → 87 markdown pages mined |
| **Browserbase + Playwright** | ✅ used | CDP-driven headless Chromium for JS-heavy/blocked pages |
| **Wiktionary / Wikipedia APIs** | ✅ used (v1) | 1,830 structured entries; v2 deep-dive (idioms/Sylheti/Chittagonian) rate-limited (429) by Wikimedia — documented honestly |
| **ScrapeGraphAI** | ⛔ network-blocked | TLS handshake rejected from collection environment (7 attempts across sessions) |
| **Browse AI** | ⛔ auth-rejected | API key rejected (401/403); robots require dashboard setup |
| **CrawlForge** | ⛔ DNS-unresolvable | no such host from this network |
| **Reddit public API** | ⛔ IP-blocked | 403 for datacenter ranges; thread mining skipped in favor of web mirrors |

Every probe result is preserved in `data/provenance/` — no API was left untried.

### Quality tiers (honest provenance)

| Tier | Meaning | Count | Confidence |
|:---:|---|---:|---|
| **1** | Gold — hand-curated by maintainers, full schema, examples, popularity | 731 | `high` |
| **2** | Wiktionary (en+bn) — dictionary-verified senses with usage labels | 194 | `medium` |
| **3** | Community/lexicon lists — GitHub & HF lexicons, blog lists, dialect corpora | 2,217 | `medium` |
| — | Tier-4 web-auto-extracts | 9,628 | quarantined in `data/candidates/` for human review |

**Deduplication**: NFC normalization + transliteration-fuzzy keys (Bengali-script and Roman-script variants of the same term merge, e.g. `খানকির পোলা` = `Khankir pula`), highest-tier source wins fields; duplicate sources recorded in `tags`.

## ⚠️ Ethics & content warning

This dataset contains **profanity, slurs, and offensive language** — that is its scientific subject matter. Entries carry a 0–3 `offensiveness` rating and a `register` flag so downstream NLP systems can detect, filter, or study such language — **not** produce it. Do not use this dataset to harass anyone. Identity-referencing terms are documented in their derogatory-slang usage with a `slur_caution` tag, reflecting descriptive linguistics, not endorsement. All content was collected from public sources; see [SOURCES.md](SOURCES.md) for full attribution and the takedown policy.

## 🔗 Related work (the gap this fills)

| Resource | What it has | What it lacks |
|---|---|---|
| BAAD (Bangla Audio Abuse Dataset) | 114 abusive words, 6,100 audio clips | no lexicon metadata, no categories, no meanings |
| BanglaDial-Abuse / ONUBAD / BD-Dialect | dialect text corpora | not slang-organized, no bilingual glosses |
| BanglaToxicCommentsDB / SentNoB | classified comments | usage corpus, not a dictionary |
| BanglaWordKit / Nirmol / deshi-slang | raw word lists | no categories, no glosses, no examples |
| **Kothar Rong (this repo)** | **3,142 categorized slang entries, 20 fields, bilingual, era+popularity** | audio layer → roadmap |

## 📚 Citation

```bibtex
@dataset{nur2026kotharrong,
  author  = {Nabid Nur and contributors},
  title   = {Kothar Rong (কথার রঙ): The Open Bangla Slang Dataset},
  year    = {2026},
  url     = {https://github.com/Hisernberg/bangla-slang-dataset},
  note    = {3,142 verified entries, 16 style \& regional categories, 20 fields,
             ELITE Research Lab Dataset Competition 2026}
}
```

## 📄 License

- **Data** (`data/`): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — share-alike keeps compatibility with the Wiktionary-derived content.
- **Code** (`scripts/`): MIT.
- Upstream licenses are honored per source — MIT/Apache sources are integrated; GPL and no-license sources are kept in `data/reference/` with attribution requirements — see [SOURCES.md](SOURCES.md).

## 🗺️ Roadmap

1. ~~v1.0 — 2,100 entries, 10 categories~~ ✅
2. ~~v2.0 — 3,142 entries, 16 categories, popularity + era enrichment~~ ✅
3. **v2.1** — human-verify the top-ranked tier-4 candidates (priority: internet & campus slang)
4. **v2.2** — audio layer: 1,000 spoken pronunciations with regional accents (the "Culture & Tone" track)
5. **v2.3** — Wiktionary deep-dive (idioms, Sylheti, Chittagonian categories) once rate-limits lift
6. **v3.0** — Bengali↔English slang-to-slang translation pairs for MT evaluation

## 🙏 Acknowledgments

- [Wiktionary](https://en.wiktionary.org/) & [bn.wiktionary](https://bn.wiktionary.org/) contributors (CC BY-SA)
- [Sigmakib2/Nirmol](https://github.com/Sigmakib2/Nirmol) — community profanity lexicon
- [amirulsizan/deshi-slang](https://github.com/amirulsizan/deshi-slang) (MIT)
- [kuntalojha/slangs](https://github.com/kuntalojha/slangs) (MIT) — multi-language slang wordlists
- [TanjimKIT — Vulgar Lexicon of Chittagonian Dialect](https://huggingface.co/datasets/TanjimKIT/Vulgar_Lexicon_of_Chittagonian_Dialect_of_Bangla_or_Bengali) (Apache-2.0)
- [zmsali/bangla-dialect-normalization](https://huggingface.co/datasets/zmsali/bangla-dialect-normalization) (Apache-2.0)
- [Sadab1522/Bangla-Six-Dialect-Dataset](https://github.com/Sadab1522/Bangla-Six-Dialect-Dataset) (MIT)
- [secrakib/Dwadash-Dataset](https://github.com/secrakib/Dwadash-Dataset) (Apache-2.0)
- Kaggle community corpora (SentNoB, Bangla hate speech, political comments, dialect corpora)
- The ELITE Research Lab for organizing the 2026 dataset competition

*কথার রঙ — every street has its own palette.*
