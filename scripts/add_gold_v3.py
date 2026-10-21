#!/usr/bin/env python3
"""V3: append curated + parsed new entries to master (KS-3143+), recompute stats."""
import csv, json, re

RAW = "/home/z/my-project/v3_raw"
REPO = "/home/z/my-project/bangla-slang-dataset"

rows = list(csv.DictReader(open(f"{REPO}/data/final/bangla_slang_master.csv")))
FIELDS = list(rows[0].keys())
known = {re.sub(r"\s+", "", r["term_bn"]) for r in rows}
known_rom = {r["romanization"].strip().lower() for r in rows}
next_id = 3143
new = []

def add(term_bn, romanization, meaning_en, category, region, pos, register, off,
        ex_bn, ex_en, era, tags, popularity, confidence, tier, source_type, source_url,
        literal_meaning="", meaning_bn=""):
    global next_id
    t = re.sub(r"\s+", "", term_bn)
    if not t or t in known: return False
    if romanization.strip().lower() and romanization.strip().lower() in known_rom: 
        if t in known: return False
    known.add(t)
    rows.append({"id": f"KS-{next_id}", "term_bn": term_bn, "romanization": romanization,
                 "literal_meaning": literal_meaning, "meaning_en": meaning_en,
                 "meaning_bn": meaning_bn, "category": category, "region": region,
                 "part_of_speech": pos, "register": register, "offensiveness": off,
                 "usage_example_bn": ex_bn, "usage_example_en": ex_en, "era": era,
                 "tags": tags, "popularity": popularity, "confidence": confidence,
                 "tier": tier, "source_type": source_type, "source_url": source_url})
    next_id += 1
    new.append(term_bn)
    return True

# ---------- 1. ling-app (Kolkata / Indian Bengali) ----------
LING = "https://ling-app.com/blog/bengali-slang-words"
ling = json.load(open(f"{RAW}/v3_glossed_candidates.json"))["ling_app"]
for e in ling:
    if not e["term_bn"]: continue
    cat = "banglish_codemixed" if "টেনশন" in e["term_bn"] else "colloquial_dialectal"
    add(e["term_bn"], e["romanization"], e["meaning_en"], cat,
        "Kolkata / West Bengal (India)", "phrase", "casual-humorous", 0,
        e["example_bn"], e["example_rom"], "current", "kolkata,india,ling-app", 3, 0.9,
        1, "ling_app_web", LING, meaning_bn=e["note"][:120])

# ---------- 2. Wiktionary slang category ----------
add("ওলানচাষী", "olan-chashi", "one who 'cultivates breasts' — lecherous man, breast-ogler",
    "profanity_curses", "Bengal-wide", "noun", "vulgar-insult", 2,
    "", "", "current", "wiktionary-slang,vulgar", 2, 0.85, 2, "wiktionary_slang_cat",
    "https://en.wiktionary.org/wiki/Category:Bengali_slang",
    literal_meaning="ওলান (breast) + চাষ (cultivation)")

# ---------- 3. somewhereinblog 87-gaali (2016 MP audio, Noakhali) ----------
SW = "https://m.somewhereinblog.net/mobile/blog/reanasblog/30135390"
GAALI = [
    ("পুটকি মারা", "putki mara", "to fart (used as insult verb)", 1, 41),
    ("চোৎমারানির পোলা", "chot-marani-r pola", "son of a front-hitter (Noakhali curse)", 3, 4),
    ("বাল ফালাইন্না", "bal falainna", "to throw pubic hair — dismissive curse (Noakhali)", 3, 6),
    ("বাল ফালানী", "bal falani", "variant: dismissive 'throw pubic hair' curse", 3, 12),
    ("মুইত্তা দেই", "muitta dei", "I'll bite/snap you (Noakhali threat-gaali)", 2, 2),
    ("গোয়া মারা", "gowa mara", "head-butt / beat (Noakhali)", 2, 2),
    ("চ্যাটের বাল", "chatter bal", "pubic hair of the groin — contempt curse", 3, 1),
]
for t, rom, en, off, cnt in GAALI:
    add(t, rom, en, "profanity_curses", "Noakhali (political speech audio, 2016)",
        "phrase", "vulgar-insult", off,
        f"২০১৬ সালের ভাইরাল অডিওতে {cnt} বার উচ্চারিত",
        f"uttered {cnt} times in the 2016 viral MP audio", "2016", "noakhali,politics,viral-audio,usage-counted",
        2, 0.8, 3, "somewhereinblog", SW)

# ---------- 4. omniglot Sylheti Nagri phrases ----------
om = json.load(open(f"{RAW}/v3_glossed_candidates.json"))["omniglot_sylheti"]
OM = "https://www.omniglot.com/language/phrases/sylheti.htm"
added_om = 0
for row in om:
    en = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", row["en"]).strip()
    if en in ("Phrase", ""): continue
    for piece in row["col2"].split("<br>"):
        m = re.match(r"\s*([ꠀ-꠫][ꠀ-꠫\s]+?)\s*\(([^)]+)\)", piece)
        if not m: continue
        nagri, rom = m.group(1).strip(), m.group(2).strip()
        if added_om >= 14: break
        ok = add(nagri, rom, en, "regional_sylhet", "Sylhet (Sylheti Nagri script)",
                 "phrase", "everyday-colloquial", 0, "", "", "traditional",
                 "sylheti-nagri,script,omniglot", 2, 0.7, 3, "omniglot_sylheti", OM)
        if ok: added_om += 1

# ---------- 5. corpus-curated (from YouTube comments / memes) ----------
CORPUS = [
    ("হাই লেভেল", "high level", "high level — meme-praise for elite style/quality",
     "internet_social", "Bangladesh (online)", "adjective-phrase", "meme-humorous", 0,
     "হাই লেভেল, হাই লেভেল!", "High level, high level! (viral comment chant)", "current",
     "meme,youtube,praise", 4, 0.9, 1, "corpus_curated_v3", "youtube-comments-mined"),
    ("পুরা ফিদা", "pura fida", "totally smitten/fascinated", "relationships_emotions",
     "Nationwide (spoken)", "adjective-phrase", "casual", 0,
     "মামা আমি পুরা ফিদা", "Mama, I'm totally smitten", "current", "romance,comment-slang",
     3, 0.8, 1, "corpus_curated_v3", "youtube-comments-mined"),
    ("ছাইরা দিল", "chaira dil", "left it/dropped it (Chittagonian perfective)",
     "regional_chattogram", "Chattogram", "verb-phrase", "casual", 0,
     "ভাই কি গান করা ছাইরা দিল নাকি?", "Bro, did he drop the song or what?", "current",
     "chattogram,dialect,comment", 3, 0.75, 1, "corpus_curated_v3", "youtube-comments-mined"),
    ("বেইচা কামাইছে", "beicha kamaische", "sold and earned (Sylheti perfective)",
     "regional_sylhet", "Sylhet", "verb-phrase", "casual", 0,
     "৩০ হাজার দিয়ে গান বেইচা কামাইছে", "Earned by selling the song for 30k", "current",
     "sylheti,dialect,comment", 3, 0.75, 1, "corpus_curated_v3", "youtube-comments-mined"),
    ("হেরা কতো", "hera koto", "how much? (Sylheti interrogative)",
     "regional_sylhet", "Sylhet", "interrogative", "casual", 0,
     "৫৬ মিলিওন ভিউ — হেরা কতো কামাইছে?", "56M views — how much did he earn?", "current",
     "sylheti,dialect,comment", 3, 0.75, 1, "corpus_curated_v3", "youtube-comments-mined"),
]
for t, rom, en, cat, reg, pos, reg2, off, exb, exe, era, tags, pop, conf, tier, st, su in CORPUS:
    add(t, rom, en, cat, reg, pos, reg2, off, exb, exe, era, tags, pop, conf, tier, st, su)

# ---------- 6. Sylheti wiki vocabulary (auto, tier 3) ----------
docs = {d["url"]: d["markdown"] for d in json.load(open(f"{RAW}/firecrawl_docs.json"))}
swiki = next((md for u, md in docs.items() if "Sylheti_language" in u), "")
added_sw = 0
if swiki:
    sec = swiki[swiki.find("Vocabulary"):]
    for m in re.finditer(r"\|\s*([ꠀ-꠫][ꠀ-꠫\s]{1,25})\s*\|\s*([^|\n]{2,60})\s*\|", sec):
        nagri, en = m.group(1).strip(), re.sub(r"\[|\]", "", m.group(2)).strip()
        if added_sw >= 18: break
        ok = add(nagri, "", en, "regional_sylhet", "Sylhet (Sylheti Nagri script)",
                 "noun/phrase", "dialectal", 0, "", "", "traditional",
                 "sylheti-nagri,wikipedia-vocab", 2, 0.65, 3, "wikipedia_sylheti_vocab",
                 "https://en.wikipedia.org/wiki/Sylheti_language")
        if ok: added_sw += 1

# ---------- 7. firecrawl search-snippet pairs (auto, tier 3, cap 30) ----------
searches = json.load(open(f"{RAW}/firecrawl_searches.json"))
added_fs = 0
for s in searches:
    q = s["query"]
    if "gali" in q: cat = "profanity_curses"
    elif "campus" in q: cat = "campus_student"
    elif "rap" in q: cat = "entertainment_media"
    elif "chittagonian" in q or "sylheti" in q: cat = "regional_chattogram" if "chittagonian" in q else "regional_sylhet"
    else: cat = "internet_social"
    for res in s["results"]:
        if added_fs >= 30: break
        content = (res.get("content") or "")[:600]
        pairs = re.findall(r"([\u0980-\u09FF][\u0980-\u09FF\s]{2,25})\s*[-–(]\s*([A-Za-z][^)\n]{5,70})", content)
        for t, en in pairs[:2]:
            t = t.strip(); en = en.strip(" )")
            if added_fs >= 30: break
            ok = add(t, "", en, cat, "Bengal (web glossary)", "word/phrase", "casual", 0,
                     "", "", "current", "web-snippet,auto", 2, 0.5, 3, "web_lexicon_v3", res.get("url", ""))
            if ok: added_fs += 1

# ---------- save ----------
with open(f"{REPO}/data/final/bangla_slang_master.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader(); w.writerows(rows)
json.dump(rows, open(f"{REPO}/data/final/bangla_slang_master.json", "w"), ensure_ascii=False, indent=1)

from collections import Counter
stats = {
    "total": len(rows),
    "by_category": dict(Counter(r["category"] for r in rows)),
    "by_tier": dict(Counter(r["tier"] for r in rows)),
    "by_source_type": dict(Counter(r["source_type"] for r in rows)),
}
old_stats = json.load(open(f"{REPO}/data/final/stats.json"))
stats["v3_layers"] = old_stats.get("v3_layers", {})
stats["v3_candidates"] = old_stats.get("v3_candidates", 0)
json.dump(stats, open(f"{REPO}/data/final/stats.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in stats.items() if k.startswith("by") or k == "total"}, indent=1, ensure_ascii=False))
print(f"NEW ENTRIES: {len(new)}")
print(new)
