#!/usr/bin/env python3
"""V3 consolidation: organize corpus layers into repo, mine candidates, update stats."""
import csv, json, os, re, shutil
from collections import Counter

RAW = "/home/z/my-project/v3_raw"
REPO = "/home/z/my-project/bangla-slang-dataset"

# ---------- 1. organize corpus layers ----------
def ensure(p):
    os.makedirs(p, exist_ok=True); return p

yt = ensure(f"{REPO}/data/corpus/youtube")
tg = ensure(f"{REPO}/data/corpus/telegram")
ly = ensure(f"{REPO}/data/corpus/lyrics")
sp = ensure(f"{REPO}/data/audio/speech_samples")
ca = ensure(f"{REPO}/data/candidates")
pv = ensure(f"{REPO}/data/provenance")

shutil.copy(f"{RAW}/yt_videos.csv", f"{yt}/videos_bn.csv")
n_comments = 0
with open(f"{RAW}/yt_comments.jsonl") as f, open(f"{yt}/comments_bn.jsonl", "w") as g:
    for line in f:
        g.write(line); n_comments += 1

n_trans, chars_trans = 0, 0
with open(f"{RAW}/supadata_transcripts.jsonl") as f, open(f"{yt}/transcripts_bn.jsonl", "w") as g:
    for line in f:
        rec = json.loads(line)
        if rec.get("lang") == "bn" and len(rec.get("text", "")) > 500:
            g.write(line); n_trans += 1; chars_trans += len(rec["text"])

n_tg = 0
with open(f"{RAW}/telegram_messages.jsonl") as f, open(f"{tg}/messages_bn.jsonl", "w") as g:
    for line in f:
        g.write(line); n_tg += 1

n_ly, chars_ly = 0, 0
with open(f"{RAW}/lrclib_lyrics.jsonl") as f, open(f"{ly}/lrclib_lyrics_bn.jsonl", "w") as g:
    for line in f:
        g.write(line); n_ly += 1; chars_ly += len(json.loads(line)["plain_lyrics"])

# speech corpus: transcripts-only clean file
sp_rows = json.load(open(f"{sp}/ragibhasan__bangla_speech_corpus_v1_rows.json"))
sp_clean = [{"segment_id": r["row"].get("segment_id"), "transcript": r["row"].get("transcript"),
             "duration_s": r["row"].get("duration"), "speaker_id": r["row"].get("speaker_id"),
             "source_id": r["row"].get("source_id"), "dataset": "ragibhasan/bangla_speech_corpus_v1",
             "license": "none specified on HF — research use with attribution"} for r in sp_rows]
with open(f"{sp}/bangla_speech_corpus_transcripts.jsonl", "w") as f:
    for r in sp_clean:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
for junk in os.listdir(sp):
    if junk.endswith("_rows.json") and junk != "ragibhasan__bangla_speech_corpus_v1_rows.json":
        os.remove(f"{sp}/{junk}")

# firecrawl provenance
shutil.copy(f"{RAW}/firecrawl_docs.json", f"{pv}/firecrawl_v3_docs.json")
shutil.copy(f"{RAW}/firecrawl_searches.json", f"{pv}/firecrawl_v3_searches.json")
shutil.copy(f"{RAW}/tavily_urls.json", f"{pv}/tavily_v3_urls.json")

# ---------- 2. candidate mining ----------
master = list(csv.DictReader(open(f"{REPO}/data/final/bangla_slang_master.csv")))
known = set()
for r in master:
    known.add(re.sub(r"\s+", "", r["term_bn"]).lower())
    known.add(r["romanization"].strip().lower())
    for tok in re.split(r"[\s,،।;:()]+", r["term_bn"]):
        if len(tok) >= 2: known.add(re.sub(r"\s+", "", tok).lower())

STOP_BN = set("আমি তুমি সে এই ওই কি আর তার তারা জন্য হবে করে হয় হচ্ছে করা হয়েছে থেকে কিন্তু যে এক দুই বড় ভালো খারাপ আজ কাল সব এখন তখন যখন কোথায় কেন কিভাবে যেভাবে না হ্যাঁ মানে মত মতো জানি জানেন দেখেন দেখি বলছি বলেন আছে আছেন ছিল হলো করলাম করবেন দিয়ে নিয়ে পেয়ে দেখে শুনে এমন ওমন কোন কিছু সবাই অনেক এত খুব বেশি একটু ভাই আপু স্যার ওখানে এখানে ব্যাপার মনে হাত চোখ মুখ জীবন দিন রাত সময় বছর মাস ঘন্টা মিনিট গণপ্রজাতন্ত্রী বাংলাদেশ বাংলা বাঙালি".split())
STOP_EN = set("the a an and or of to in is are was were be been this that it its you your i we they he she for on at with from by as not no yes so if but about just like really very much more most can will would should could have has had do does did get got make made one two all some any now then when what how why who where which".split())

BN_WORD = re.compile(r"[\u0980-\u09FF]{2,}")
EN_WORD = re.compile(r"[a-zA-Z'][a-zA-Z']{2,}")

def norm_bn(w): return re.sub(r"^\W+|\W+$", "", w)

freq = {}   # term -> [count, {sources}, sample]
def add(term, src, ctx):
    t = norm_bn(term).lower()
    if len(t) < 2 or t in known or t in STOP_BN or t in STOP_EN: return
    if re.match(r"^[a-zA-Z']+$", t) and t.lower() in STOP_EN: return
    e = freq.setdefault(t, [0, Counter(), ""])
    e[0] += 1
    e[1][src] += 1
    if not e[2] and ctx: e[2] = ctx[:160]

def mine_text(text, src):
    toks_bn = [norm_bn(w) for w in BN_WORD.findall(text)]
    for w in toks_bn:
        add(w, src, text)
    for i in range(len(toks_bn) - 1):
        add(toks_bn[i] + " " + toks_bn[i+1], src, text)
    for w in EN_WORD.findall(text):
        w2 = w.strip("'")
        if 3 <= len(w2) <= 15 and not w2.isupper():
            add(w2, src, text)

with open(f"{yt}/comments_bn.jsonl") as f:
    for line in f:
        c = json.loads(line)
        mine_text(c["text"], f"yt_comment:{c['videoId']}")
with open(f"{tg}/messages_bn.jsonl") as f:
    for line in f:
        m = json.loads(line)
        mine_text(m["text"], f"telegram:{m['channel']}")
with open(f"{ly}/lrclib_lyrics_bn.jsonl") as f:
    for line in f:
        s = json.loads(line)
        mine_text(s["plain_lyrics"][:2000], f"lyrics:{s['artist']}")
with open(f"{yt}/transcripts_bn.jsonl") as f:
    for line in f:
        t = json.loads(line)
        mine_text(t["text"][:3000], f"transcript:{t['videoId']}")

# filter: appear 3+ times AND in 2+ distinct source docs
cands = [(t, c, dict(srcs), sample) for t, (c, srcs, sample) in freq.items()
         if c >= 3 and len(srcs) >= 2]
cands.sort(key=lambda x: -x[1])
with open(f"{ca}/v3_corpus_candidates.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["term", "corpus_frequency", "distinct_sources", "sources_sample", "first_context"])
    for t, c, srcs, sample in cands[:400]:
        w.writerow([t, c, len(srcs), ";".join(list(srcs)[:3]), sample])

# ---------- 3. provenance manifest ----------
manifest = {
  "version": "3.0",
  "layers": {
    "youtube_videos": {"count": sum(1 for _ in open(f"{yt}/videos_bn.csv")) - 1, "api": "YouTube Data API v3", "license": "metadata via official API ToS"},
    "youtube_comments": {"count": n_comments, "api": "YouTube Data API v3 commentThreads"},
    "youtube_transcripts": {"count": n_trans, "chars_bn": chars_trans, "api": "Supadata", "lang": "bn"},
    "telegram_messages": {"count": n_tg, "method": "t.me/s/ public web previews", "channels": 7},
    "lrclib_lyrics": {"count": n_ly, "chars": chars_ly, "license": "LRCLIB open lyrics db", "note": "artist_name search empty; q= full-text worked; heavy 503 backoff"},
    "edge_tts_audio": {"count": 160, "voices": ["bn-BD-NabanitaNeural", "bn-BD-PradeepNeural"], "license": "generated, no copyright"},
    "speech_corpus_transcripts": {"count": len(sp_clean), "dataset": "ragibhasan/bangla_speech_corpus_v1", "license": "none specified — attribution given"},
    "firecrawl_docs": {"count": 10, "chars": 533872},
    "tavily_urls": {"count": 107},
    "rss_headlines": {"count": 86, "feeds": ["bbc_bangla", "prothom_alo"]},
  },
  "blocked_or_failed": {
    "yt_dlp_audio_download": "YouTube bot-check wall on datacenter IP",
    "huggingface_datasets_server": "overloaded (429/503) for google/fleurs; gated for Kathbath/CV17 — pulled via hub search fallback: ragibhasan corpus OK",
    "lrclib_artist_search": "empty; q= mode used instead",
    "telegram_api_hash": "user provided api_hash only (32-hex); api_id number missing — keyless t.me/s/ previews used",
  },
}
json.dump(manifest, open(f"{pv}/v3_harvest_manifest.json", "w"), ensure_ascii=False, indent=1)

# ---------- 4. stats.json v3 section ----------
stats = json.load(open(f"{REPO}/data/final/stats.json"))
stats["v3_layers"] = {k: v.get("count", 0) for k, v in manifest["layers"].items()}
stats["v3_candidates"] = len(cands)
json.dump(stats, open(f"{REPO}/data/final/stats.json", "w"), ensure_ascii=False, indent=1)

print(json.dumps({k: v.get("count") for k, v in manifest["layers"].items()}, indent=1))
print(f"candidates: {len(cands)}")
print("TOP 60 candidates:")
for t, c, srcs, sample in cands[:60]:
    print(f"  {t}  x{c} [{len(srcs)}src]  {sample[:70]}")
