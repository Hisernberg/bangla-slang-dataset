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

## v3.0 — Multi-Modal Expansion (2026-10-21)

**3,174 entries · 16 categories · 230 audio clips · 2,900+ usage-corpus documents**

### Added
- **🎧 TTS audio layer**: 230 MP3 clips of high-popularity entries generated with Microsoft Edge-TTS Bengali neural voices (bn-BD-NabanitaNeural, bn-BD-PradeepNeural); manifest with per-clip duration, voice and schema fields (`data/audio/kothar_rong_tts/`).
- **🗣 Real-speech layer**: 100 Bangla TV-speech transcripts with speaker IDs & durations from HF `ragibhasan/bangla_speech_corpus_v1` (`data/audio/speech_samples/`).
- **📄 Usage corpus** (`data/corpus/`): 2,597 YouTube comments (30 top videos, up to 56M views) + 354-video metadata (YouTube Data API v3); 8 full Bangla drama/comedy transcripts (~40K chars, Supadata); 66 song lyrics incl. Bangla rap (LRCLIB); 37 Telegram meme-channel messages (public previews); 86 news headlines (BBC Bangla + Prothom Alo RSS).
- **+32 new entries** (KS-3143 → KS-3174): 6 Kolkata/Indian-Bengali slang (ling-app, glossed with examples), 1 Wiktionary slang-category term, 6 usage-counted Noakhali political gaalis from the 2016 viral MP audio (somewhereinblog), **14 Sylheti Nagri-script phrases** (Omniglot), 5 corpus-mined dialect verbs.
- **+400 corpus-mined candidate terms** frequency-verified across ≥2 independent sources (`data/candidates/v3_corpus_candidates.csv`).
- **v3 pipelines** added to `scripts/` (env-var-only, key-free): YouTube harvest, Supadata transcripts, Tavily discovery, Firecrawl scrape, Telegram previews, LRCLIB lyrics, Edge-TTS audio, RSS, candidate miner.

### Sources
- YouTube Data API v3, Supadata, Tavily, Firecrawl v2 (16 pages + 8 searches), Omniglot, ling-app, somewhereinblog, LRCLIB, Edge-TTS, HF datasets-server, RSS. Full manifest + blocked-source log: `data/provenance/v3_harvest_manifest.json`.

### Blocked (documented)
- yt-dlp audio download (YouTube bot-wall on datacenter IPs), HF datasets-server rows for `google/fleurs` (persistent 503) and gated `Kathbath`/`common_voice_17_0`, Telegram Bot API (api_hash provided without api_id).

## [3.1.0] — 2026-10-21 — Mega-corpus & Emotional-Tone expansion

### Added
- **💬 Comment mega-corpus**: 239,148 YouTube comments from 1,099 Bangla videos (26 search angles: roast, standup, gaming, campus, cricket reactions, street interviews, TikTok-viral) — `data/corpus/youtube/comments_bn_v31.jsonl.gz`.
- **🔎 Usage evidence**: 916 lexicon terms now carry real-usage frequency + top-liked example comments mined from the 239K corpus — `data/corpus/usage_evidence.json`.
- **❤️ Emotional-tone layer**: 672 BASER clips (CC BY 4.0) labeled ANGRY/SAD/HAPPY/FEAR/NEUTRAL with speaker metadata — `data/audio/emotion_baser/`.
- **🗣️ Real-speech layer v2**: 252 clips + transcripts (telecom customer-care BUET corpora, community ASR sets), re-encoded 48 kbps mono — `data/audio/speech_samples/`, `callcenter_bn/`.
- **🎧 TTS bank**: 230 → 1,380 neural pronunciation clips (tier-ranked coverage, 2 bn-BD voices).
- **3 NEW categories** (+105 gold entries): `meme_internet_culture` (29), `genz_trending` (19), `corporate_workplace` (19); gaming +14, campus +9, Dhaka street +5.
- **📖 Wiktionary deep-dive**: full 1,845-title Bengali slang category tree fetched + parsed → 123 slang-tagged entries (8 new tier-2), 2,529 slang-flagged lyric lines from 194 tracks.
- **🎬 Shorts layer**: 194 Bangla Shorts metadata; **😂 memes**: 50 new Telegram messages (26 channels) + 100 Imgflip templates reference.
- **🌐 Tavily wave-2**: 42 queries → 320 URLs → 88 full-text pages; candidate pool grown to 2,529 terms.

### Sources
- YouTube Data API v3 (~6K quota units), Tavily, Supadata, Firecrawl, Kaggle API (BASER, call-center), HF datasets-server (6 ungated bn speech datasets), LRCLIB, Edge-TTS, Telegram previews, Imgflip. Manifest: `data/provenance/v31_harvest_manifest.json`.

### Blocked (documented)
- youtube-transcript-api/yt-dlp (bot-wall), Supadata credits exhausted, HF `google/fleurs` rows (parquet scan limit), memegen (DNS), Telegram API (api_id still missing).
