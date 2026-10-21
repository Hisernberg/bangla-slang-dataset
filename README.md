# কথার রঙ · Kothar Rong — The Open Bangla Slang Dataset

**কথার রঙ** ("The Color of Speech") is an open, multi-source lexicon of **Bangla (Bengali) slang** — regional street dialects, internet meme culture, campus slang, profanity, cinema catchphrases, street-and-bazaar language, sports & gaming banter, idioms, and the living register of everyday Bengal — organized into **19 style & regional categories** with romanization, bilingual glosses, registers, offensiveness ratings, era tags and popularity estimates — plus a **239K-comment usage corpus**, **2,300+ audio clips** (TTS + emotional + real speech) and per-term **usage evidence** mined from live social data.

> 🏁 Built as the flagship lexicon for the **ELITE Research Lab Dataset Competition 2026** (slang-dictionary special category · "Culture & Tone" priority track).

![Entries](https://img.shields.io/badge/entries-3%2C287%20verified-brightgreen) ![Categories](https://img.shields.io/badge/categories-19-blue) ![Gold](https://img.shields.io/badge/gold%20curated-837-gold) ![Audio](https://img.shields.io/badge/audio%20clips-2%2C303-red) ![Corpus](https://img.shields.io/badge/usage%20corpus-239K%20comments-purple) ![Examples](https://img.shields.io/badge/usage%20examples-1%2C049-success) ![License](https://img.shields.io/badge/data%20license-CC%20BY--SA%204.0-lightgrey) ![Code](https://img.shields.io/badge/code%20license-MIT-informational) ![Romanization](https://img.shields.io/badge/romanization-100%25-success)

---

## 📊 Dataset at a glance

| | |
|---|---|
| **Verified entries** | **3,287** (+12,500+ auto-extracted candidates quarantined for human annotation) |
| **Categories** | 19 (4 regional + 15 style/usage-based) |
| **Gold-curated entries** | 837 with full schema (meaning, gloss, example, register, era, popularity) |
| **Sources** | 18+ harvested systems: Wiktionary (en+bn), GitHub, Hugging Face + datasets-server, Kaggle, Firecrawl, Browserbase, YouTube Data API, Supadata, Tavily, LRCLIB, Telegram public channels, 240+ web pages |
| **🎧 Audio layer** | **2,303 clips** — 1,380 TTS pronunciations (bn-BD neural) + 672 BASER emotional clips (ANGRY/SAD/HAPPY/FEAR/NEUTRAL) + 252 real-speech clips (telecom customer-care, ASR corpora) + 1 call-center dialogue (`data/audio/`) |
| **📄 Usage corpus** | **239,148 YouTube comments** (1,099 videos) · **916 lexicon terms with usage evidence** · 11 video transcripts · 194 lyric tracks (2,529 slang-flagged lines) · 87 Telegram meme messages · 194 Shorts metadata · 86 news headlines (`data/corpus/`) |
| **Scripts covered** | Bengali (primary) · Sylheti Nagri (reference) · Banglish Roman (documented variants) |
| **Fields per entry** | 20 — see [SCHEMA.md](SCHEMA.md) |
| **Romanization** | 100% (deterministic auto-transliteration + source-provided) |
| **English glosses** | 2,178 entries (66%) · Bengali glosses: 921 · **usage examples: 1,049** |
| **Popularity estimates** | 726 entries rated 1–5 for social-media usage frequency |
| **Quality tiers** | 3-tier provenance system — see below |

## 🗂️ The 19 categories

| # | Category | বাংলা | Entries | Example |
|---|----------|-------|--------:|---------|
| 1 | `regional_dhaka` | ঢাকাইয়া | 128 | **মামা** (*mama*) — universal friendly address; **টোকাই** (*tokai*) — Old Dhaka street urchin |
| 2 | `regional_chattogram` | চট্টগ্রামীয়া | 745 | **কেন মামা লাগব** — iconic film-origin refusal catchphrase |
| 3 | `regional_sylhet` | সিলেটি | 77 | **কিতা গরু মামা** (*kita goru mama*) — "no way!"; **বাইল** (*bail*) — rice; **ꠡꠣꠉꠔꠝ꠆** (*shagotom*, Sylheti Nagri script) — welcome |
| 4 | `colloquial_dialectal` | সাধারণ কথ্য ও আঞ্চলিক | 580 | general colloquial & minor-dialect slang incl. **287 Barishal-region dialect words** (আইজ, মোর, মনডা…) |
| 5 | `profanity_curses` | গালি ও অভিশাপ | 1,080 | **বোকাচোদা** (*bokachoda*) — "dumbass"; rated 0–3 for severity |
| 6 | `internet_social` | ইন্টারনেট ও সোশ্যাল মিডিয়া | 78 | **এয়ার মারা** (*air mara*) — leave on read; **রিয়েল মারা** — "I'm dead!"; **ফোটা দেওয়া** — expose someone |
| 7 | `campus_student` | ক্যাম্পাস ও ছাত্রজীবন | 61 | **ব্যাক খাওয়া** — fail a course; **সাপ্লাই** (*supply*), **ক্যারি খাওয়া** — carry a failed course, **প্রথম সালাম** — freshman greeting ritual |
| 8 | `entertainment_media` | সিনেমা-নাটক ও বিনোদন | 38 | **ওভার অ্যাকশন**, **মুখ ওস্তাদ** — all-talk show-off, **ফার্স্ট ডে ফার্স্ট শো** cult fan |
| 9 | `relationships_emotions` | সম্পর্ক ও আবেগ | 64 | **পাতনা** (*patna*) — make-up after a fight; **মান করা** — sulking; **মুড অফ** |
| 10 | `social_political` | সামাজিক-রাজনৈতিক | 51 | **হাওয়া খাওয়া** — vanish after political fall; **ভোট খাওয়া** — steal votes; **এক পয়েন্ট এক দাবি** |
| 11 | `banglish_codemixed` | বাংলিশ (কোড-মিক্সড) | 80 | **ভাইব** (*vibe*), **ইস্যু করা** — pick a fight, **সেটিং হওয়া** — pre-arranged fix, **লাইন মারা** — flirt |
| 12 | `exclamations_interjections` | আবেগপ্রকাশক ধ্বনি | 59 | **আব্বা মাগো!**, **বাহ্** (bravo!), **থাক গে** (forget it!), **ইসsh**, **ধুর** |
| 13 | `old_school_retro` | পুরান দিনের স্ল্যাং | 33 | **বেশ জিনিস!**, **জোস**, **ডিস্কো পোলা**, **বাহারি**, **স্টেরিও পোলা** |
| 14 | `street_transport_market` | রাস্তা-বাজার-বাহন | 51 | **জায়গা আছে!** — bus cry; **ফেরি দেওয়া** — pass the fare; **রেসের বাস** — racing bus; **দালাল পোলা** |
| 15 | `cricket_sports_gaming` | ক্রিকেট-খেলা-গেমিং | 50 | **খেলা হবে!** — game on!; **রাশ করা** — all-in rush; **ক্যাম্প মারা** — camp for kills; **ক্লাচ করা** — clutch |
| 16 | `idioms_figurative` | বাগধারা ও রূপক | 45 | **ঢোল পিটানো** — beat your own drum; **চোখে ধুলো দেওয়া** — deceive; **আগুনে ঘি ঢালা** |
| 17 | `meme_internet_culture` | মিম ও ইন্টারনেট সংস্কৃতি | 29 | **চুজ্জ** — meme-era swagger; **হাব্যো** — affectionate nerd-roast; **ভাইরাল খাওয়া** — go viral (against your will) |
| 18 | `genz_trending` | জেন-জেড ট্রেন্ডিং | 19 | **ভাইব চেক** — vibe check; **মুড অফ** — mood off; **পার্সোনাল খাওয়া** — take it personal |
| 19 | `corporate_workplace` | কর্পোরেট-অফিস | 19 | **বস প্লিজিং** — boss-pleasing; **মিটিং শেষে মিটিং** — meeting after meeting; **নোটিশ খাওয়া** — eat a termination notice |

Full details and inclusion criteria: [TAXONOMY.md](TAXONOMY.md).

## 🚀 Quickstart

```python
import pandas as pd

df = pd.read_csv("data/final/bangla_slang_master.csv")
print(df.shape)                      # (3287, 20)

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

## 🔊 v3.1 Mega-corpus & Emotional-Tone Layer (new)

v3.1 is a **100× corpus expansion** driven by the full API stack (YouTube Data API v3, Tavily, Supadata, Firecrawl, Kaggle, HF datasets-server) plus resumable keyless pipelines. New in this release:

| Layer | Contents | Path | Licenses / ToS basis |
|-------|----------|------|----------------------|
| **💬 Comment mega-corpus** | **239,148 YouTube comments** mined from **1,099 Bangla videos** (comedy, roast, standup, gaming, campus, street interviews, cricket reactions, TikTok-viral) — quota-budgeted, relevance-ordered | `data/corpus/youtube/comments_bn_v31.jsonl.gz` | YouTube Data API ToS (public data) |
| **🔎 Usage evidence** | **916 lexicon terms** matched against the 239K-comment corpus with per-term frequency + up to 4 top-liked real example comments each — turning dictionary entries into *evidenced* usage records | `data/corpus/usage_evidence.json` | derived, public data |
| **❤️ Emotional-tone audio** | **672 BASER clips** (CC BY 4.0): ANGRY / SAD / HAPPY / FEAR / NEUTRAL spoken Bangla by labeled speakers — directly serves the **"Culture & Tone"** priority track | `data/audio/emotion_baser/` + manifest | Kaggle `jabedcse/baser-dataset` (CC BY 4.0) |
| **🗣️ Real-speech audio** | 252 clips + transcripts from telecom **customer-care** dialogs (BUET), shunyalabs & community ASR corpora, re-encoded 48 kbps mono | `data/audio/speech_samples/` + `callcenter_bn/` | HF/kaggle dataset terms (attribution in manifests) |
| **🎧 TTS bank ×6** | 1,380 neural pronunciation clips (was 230): tier-ranked coverage of the lexicon, 2 bn-BD voices, rebuilt manifest | `data/audio/kothar_rong_tts/` | Generated — no copyright |
| **🎬 Shorts/reels layer** | 194 Bangla Shorts (meme/roast/comedy) metadata via `videoDuration=short` search | `data/corpus/youtube/shorts_bn_v31.csv` | YouTube Data API ToS |
| **🎵 Lyrics ×2** | 194 tracks total (128 new: Bangla hip-hop, viral songs), **2,529 slang-flagged lyric lines** | `data/corpus/lyrics/` | LRCLIB open lyrics DB |
| **😂 Memes** | 87 Telegram public meme-channel messages (26 channels probed) + 100 Imgflip template reference set | `data/corpus/telegram/` | Public t.me/s/ previews; imgflip API |
| **📖 Wiktionary deep-dive** | Full **1,845-title Bengali slang category tree** fetched and parsed → 123 slang-tagged entries (9 new tier-2 terms added; rest deduped against master) | `data/reference/wiktionary_slang_v31.json` | CC BY-SA / GFDL (Wiktionary) |
| **🌐 Web pages** | 320 Tavily-discovered Bangla slang pages (42 queries) → 88 full-text + snippets; Firecrawl pass on priority domains | `data/provenance/` manifests | per-source in SOURCES.md |
| **➕ New entries +113** | **105 gold-curated** across 3 NEW categories (`meme_internet_culture`, `genz_trending`, `corporate_workplace`) + gaming/campus/regional additions + **8 Wiktionary tier-2** | `data/final/bangla_slang_master.json` | CC BY-SA 4.0 |
| **📊 Mined candidates** | 2,529 frequency-verified Bangla/Banglish terms awaiting annotation | `data/candidates/candidates_v31.json` | — |

**Blocked & documented this wave:** YouTube transcript/caption endpoints + yt-dlp (datacenter bot-wall — transcripts sourced via Supadata where credits remained), Supadata free credits exhausted mid-run (3 transcripts), memegen.google.com (DNS-blocked in sandbox), several Telegram channels (0 preview messages), Facebook reels (no legitimate keyless path — Shorts used as proxy).

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
