# SOURCES — Full Provenance & Attribution

Every entry in Kothar Rong traces to a public source. This file lists them all, with licenses and what was taken.

## Primary harvested sources

### 1. English Wiktionary — `wiktionary_en` (124 entries after filtering)
- **URL**: https://en.wiktionary.org/wiki/Category:Bengali_slang (plus vulgarities, colloquialisms, offensive terms, dialect categories)
- **Method**: MediaWiki API — category members → wikitext → sense-label parser (`{{lb|bn|slang|vulgar}}` → tags), definition cleaning
- **License**: CC BY-SA 4.0 (dual-licensed with GFDL) → this dataset adopts CC BY-SA 4.0 for compatibility
- **Take**: 1,830 Bengali-section entries scanned; 124 kept after strict colloquial-family label filtering

### 2. Bengali Wiktionary — `wiktionary_bn` (70 entries)
- **URL**: https://bn.wiktionary.org/wiki/বিষয়শ্রেণী:ঢাকাইয়া_কুট্টি_ভাষার_শব্দ
- **License**: CC BY-SA 4.0
- **Take**: Dhakaiya Kutti dialect words with Bengali glosses and `{{usex}}` usage examples (উভয়ৌষ্ঠ্য, হাইছা, অইচিল…)

### 3. Sigmakib2/Nirmol (GitHub, 40★) — `nirmol_github` (802 entries)
- **URL**: https://github.com/Sigmakib2/Nirmol
- **License**: none declared upstream → treated as **attribution-required factual word list** (single-term rows = compilation of facts); redistributed as `data/reference/nirmol_terms_attribution_required.csv` with this notice; upstream contacted-worthy — if you are the author and object, open an issue and it will be removed
- **Take**: Bengali profanity terms + Roman-script variants (Koromchod, Notimagi…)

### 4. amirulsizan/deshi-slang (GitHub) — `deshi_slang_github` (68 entries)
- **URL**: https://github.com/amirulsizan/deshi-slang
- **License**: MIT ✔ redistributed in `data/reference/deshi_slang_MIT.jsonl`
- **Take**: structured profanity entries with romanization + severity scores (spam/obfuscated rows dropped)

### 5. TanjimKIT — Vulgar Lexicon of Chittagonian Dialect (Hugging Face) — `hf_chittagong_vulgar` (731 entries)
- **URL**: https://huggingface.co/datasets/TanjimKIT/Vulgar_Lexicon_of_Chittagonian_Dialect_of_Bangla_or_Bengali
- **License**: Apache-2.0 ✔ redistributed in `data/reference/chittagonian_vulgar_Apache2.csv`
- **Take**: Chittagonian vulgar/dialect terms (single column)

### 6. Web lexicon lists — `web_lexicon_list` (155 entries)
- **175-item Bangla abusive-language list** — allzinone.blogspot.com (2014): https://allzinone.blogspot.com/2014/12/list-of-175-abusive-language-bangla.html — rendered via Browserbase + Playwright (Cloudflare-bypassing headless session); 134 numbered terms extracted
- **Dhakaiya/Chatgaiya blog & wiki word lists** — bn.wikipedia ঢাকাইয়া কুট্টি উপভাষা, en.wikipedia Dhakaiya Kutti dialect, Daily Star "Bazaira Vasha", Dhaka Tribune "Dhaka Dictionary", Ajker Patrika, Prothom Alo সোব্বাসি (all CC BY-SA for wiki pages; news articles quoted factually)
- **ling-app 10 Bengali slang words**: https://ling-app.com/blog/bengali-slang-words/ (educational list, factual extraction)
- **guruchandali.com স্ল্যাং essay** (সংসদে চুদুর-বুদুর ruling history)
- **somewhereinblog slang crowdsourcing thread**: https://www.somewhereinblog.net/blog/icarusss/29879801

### 7. Kaggle — referenced corpora (not redistributed)
- **Suspicious Bengali Text (Slang)** — https://www.kaggle.com/datasets/mizan116/suspicious-bengali-text-slang (43,389 rows, MIT license) — used as usage-context reference; download via Kaggle API
- Survey of 80+ slang/bangla Kaggle datasets confirmed: **no existing categorized Bangla slang dictionary** — the gap this dataset fills

### 8. Survey-only sources (context, no entries taken)
- Hugging Face: 180+ Bangla datasets surveyed (Nirmol-adjacent toxic sets, hate-speech sets)
- GitHub: 14 slang-related repos surveyed
- Academic papers: IJCRT Dinajpur গালি study, SSRN "Exploring Bangla Language Slang", Springer university-slang willingness study, Sylheti Project lessons, PMC Sylheti dataset paper

## The 9 API systems — full disclosure

| # | System | Key used | Result |
|---|--------|----------|--------|
| 1 | GitHub REST API | PAT | ✅ repo search, tree listing, raw file fetch, this repo's host |
| 2 | Hugging Face Hub API | token | ✅ dataset search + file download |
| 3 | Kaggle API v1 (Bearer) | KGAT token | ✅ authenticated dataset search + download |
| 4 | Firecrawl v2 (search + scrape) | fc- key | ✅ **primary web harvester** — 18 searches, 15 scrapes, 2.4 MB markdown |
| 5 | Browserbase v1 (CDP sessions) | bb_live_ key | ✅ headless Chromium sessions via `connect_over_cdp`; rendered JS-blocked pages |
| 6 | MediaWiki Action API (Wiktionary/Wikipedia) | public | ✅ 1,830 wikitext entries |
| 7 | ScrapeGraphAI smartscraper | sgai- key | ⛔ TLS handshake rejected from collection network (tried: urllib, curl, browser-fetch, context.request, same-origin navigation — logs in `data/provenance/api_probe_results.json`); integration script `scripts/08_scrapegraphai_probe.py` ships ready-to-run |
| 8 | Browse AI v2 | key | ⛔ 401 unauthorized (key rejected / robots not configured in dashboard) |
| 9 | CrawlForge | cf_live_ key | ⛔ DNS does not resolve (`api.crawlforge.dev`, `crawlforge.net`) |

No API key is committed to this repository; all collection scripts read keys from environment variables.


## v2.0 additions

### 9. kuntalojha/slangs (GitHub, MIT) — `kuntalojha_slangs_mit` (174 entries)
Multi-language slang wordlist package; the Bengali array contributed 202 raw terms (174 unique after dedupe). License: MIT (integrated). https://github.com/kuntalojha/slangs

### 10. zmsali/bangla-dialect-normalization (Hugging Face, Apache-2.0) — `hf_dialect_norm_apache2` (287 entries)
Dialect↔standard Bangla sentence pairs (Barishal and other regions). Dialect words differing from the standard were mined with a recurrence filter, giving 287 regional dialect words with region tags. License: Apache-2.0 (integrated). https://huggingface.co/datasets/zmsali/bangla-dialect-normalization

### 11. reja273/BanglaWordKit (GitHub, no license) — reference only
slang↔clean-Bangla pairs (40) and shadhu→cholito pairs (3,781). No license found → kept in `data/reference/banglawordkit_slang_pairs_attribution_required.json`, attribution required; pairs quarantined as candidates, not integrated into the master. https://github.com/reja273/BanglaWordKit

### 12. Sadab1522/Bangla-Six-Dialect-Dataset (GitHub, MIT) — reference only
Sentence-level six-dialect corpus (Chittagong, Pabna, Noakhali, …). Kept as `data/reference/`. https://github.com/Sadab1522/Bangla-Six-Dialect-Dataset

### 13. secrakib/Dwadash-Dataset (GitHub, Apache-2.0) — reference only
Twelve-source dialect compilation (Chatgaiyya Alap, BanglaDial, Vashantor, Bhasabodh, Ancholik…). Git-LFS files not retrievable from the collection environment; manifest preserved. https://github.com/secrakib/Dwadash-Dataset

### 14. Jawwad1233/Setu (GitHub, no license) — reference only
248-entry English-slang glossary built for Bangladeshi translation (user-supplied definitions). Surveyed for Banglish usage patterns; not redistributed. https://github.com/Jawwad1233/Setu

### 15. Kaggle corpora (v2) — referenced, not redistributed
12 datasets downloaded for analysis: Bangla hate speech recognition, Bangla political comments, SentNoB (noisy-text sentiment), 11.5k Bangla news, "bleach" dialect corpus (Noakhali/Chittagong sentences), microblog POS lexicons, YouTube sentiment/emotion. https://www.kaggle.com/datasets (see manifest in provenance)

### 16. Firecrawl v2 web harvest (v2) — `fc2_web_auto` candidates
24 search queries (Bangla + English: বাংলা স্ল্যাং, বাগধারা, কুট্টি ভাষা, gen-z slang, gali lists, dialect word lists…) → 87 markdown pages → 9,553 auto-extracted candidates quarantined for annotation (tier 4).

### 17. Reddit public JSON API — blocked, disclosed
r/bangladesh slang threads returned HTTP 403 (datacenter-IP block). No data taken; documented in provenance.

## Data licensing summary

| This dataset | Upstream | Terms honored |
|---|---|---|
| CC BY-SA 4.0 (data) | Wiktionary/Wikipedia (CC BY-SA 4.0) | attribution + share-alike ✔ |
| CC BY-SA 4.0 (data) | deshi-slang (MIT) | MIT text kept alongside redistribution ✔ |
| CC BY-SA 4.0 (data) | Chittagonian lexicon (Apache-2.0) | Apache text compatible; source linked ✔ |
| CC BY-SA 4.0 (data) | Nirmol (no license — factual list) | attribution + takedown offer ✔ |
| CC BY-SA 4.0 (data) | blog/wiki word lists | factual extraction + deep links ✔ |

**Takedown policy**: any source author can request removal via GitHub issues — no questions asked.

## v3.0 additions

| # | Source | What was taken | License / basis | URL |
|---|--------|----------------|-----------------|-----|
| 18 | YouTube Data API v3 | 354 video metadata + 2,597 comments | Official API ToS, public data | https://developers.google.com/youtube |
| 19 | Supadata | 8 full Bangla video transcripts (~40K chars) | API ToS | https://supadata.ai |
| 20 | Tavily search | 107 source-discovery URLs | API ToS | https://tavily.com |
| 21 | Firecrawl v2 (16 pages + 8 searches) | Wiktionary Bengali-slang category, bn.wiki গালি, Sylheti-language wiki, youswear, omniglot, ling-app, somewhereinblog, Prothom Alo review (~534K chars) | factual extraction + deep links | https://firecrawl.dev |
| 22 | ling-app Bengali slang blog | 6 Kolkata-Bengali slang entries with EN glosses + examples | factual extraction + deep link | https://ling-app.com/blog/bengali-slang-words |
| 23 | somewhereinblog | 6 Noakhali political gaalis with 2016 usage counts | factual extraction + deep link | https://m.somewhereinblog.net/mobile/blog/reanasblog/30135390 |
| 24 | Omniglot Sylheti phrases | 14 Sylheti Nagri-script phrases with romanization | factual extraction + deep link | https://www.omniglot.com/language/phrases/sylheti.htm |
| 25 | LRCLIB | 66 Bangla song lyrics (incl. Bangla rap) | LRCLIB open lyrics DB, no key | https://lrclib.net |
| 26 | Microsoft Edge-TTS | 230 generated Bengali audio clips | generated, no copyright | https://github.com/rany2/edge-tts |
| 27 | ragibhasan/bangla_speech_corpus_v1 | 100 speech transcripts + metadata | no license stated — research attribution | https://huggingface.co/datasets/ragibhasan/bangla_speech_corpus_v1 |
| 28 | RSS: BBC Bangla + Prothom Alo | 86 headlines (reference register) | public RSS feeds | https://feeds.bbci.co.uk/bengali/rss.xml |
| 29 | Telegram public previews | 37 meme-channel messages (7 channels) | public t.me/s/ web previews | https://t.me/s/bangla_memes |
