#!/usr/bin/env python3
"""v2 parse: gold3-6 + new GitHub lists + HF dialect mining + Firecrawl candidates + wt2 (if present).
License policy: MIT/Apache/CC -> tier3 master; GPL -> attribution-required; no-license -> reference+candidates only."""
import json, re, os, csv, glob, shutil, unicodedata

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"
GH = RAW + "/gh"
REF = "/home/z/my-project/bangla-slang-dataset/data/reference"
os.makedirs(REF, exist_ok=True)

# ---------------- gold v2 ----------------
gold = []
for p in [3, 4, 5, 6]:
    f = f"{RAW}/gold_part{p}.json"
    if os.path.exists(f):
        gold += json.load(open(f))
json.dump(gold, open(RAW + "/parse_v2_gold.json", "w"), ensure_ascii=False)
print(f"gold v2: {len(gold)}")

def norm(t):
    t = unicodedata.normalize("NFC", (t or "")).strip()
    t = re.sub(r"[।,;:!?\-–—_()\.]+", " ", t)
    return re.sub(r"\s+", " ", t).strip().lower()

# ---------------- GitHub: kuntalojha bengali.js (MIT) ----------------
gh_terms = []
src = open(GH + "/kuntalojha__slangs/languages__bengali.js", encoding="utf-8").read()
words = re.findall(r'"([^"]+)"', src) + re.findall(r"'([^']+)'", src)
for w in words:
    w = w.strip()
    if re.search(r"[\u0980-\u09FF]", w) and 2 <= len(w) <= 25:
        gh_terms.append({"term_bn": w, "source_type": "kuntalojha_slangs_mit",
                         "source_url": "https://github.com/kuntalojha/slangs (MIT)",
                         "license": "MIT", "tags": ["slang_list"]})
json.dump(gh_terms, open(RAW + "/parse_v2_gh_kuntalojha.json", "w"), ensure_ascii=False)
print(f"kuntalojha terms: {len(gh_terms)}")

# ---------------- GitHub: BanglaWordKit slang->clean (no-license -> candidates) ----------------
bw = []
try:
    d = json.load(open(GH + "/reja273__BanglaWordKit/BanglaWordKit__data__slang_words_dataset.json"))
    for it in d:
        bw.append({"term_bn": it["slang"].strip(), "meaning_bn": it["clean"].strip(),
                   "source_type": "banglawordkit_no_license",
                   "source_url": "https://github.com/reja273/BanglaWordKit (no license; attribution-required)",
                   "tags": ["attribution_required"]})
    shutil.copy(GH + "/reja273__BanglaWordKit/BanglaWordKit__data__slang_words_dataset.json",
                REF + "/banglawordkit_slang_pairs_attribution_required.json")
except Exception as e:
    print("bw ERR", e)
json.dump(bw, open(RAW + "/parse_v2_gh_banglawordkit.json", "w"), ensure_ascii=False)
print(f"banglawordkit pairs: {len(bw)}")

# ---------------- HF: zmsali dialect-normalization (Apache-2.0) -> dialect word candidates ----------------
hf_dialect = []
try:
    d = json.load(open(RAW + "/hf/hf_rows.json"))
    rows = d["zmsali/bangla-dialect-normalization"]["rows"]
    for r in rows:
        row = r.get("row", r)
        db = (row.get("dialect_bangla") or "").strip()
        sb = (row.get("standard_bangla") or "").strip()
        reg = (row.get("region") or "").strip()
        en = (row.get("english") or "").strip()
        if db and sb and db != sb:
            hf_dialect.append({"term_bn": db, "standard_bn": sb, "meaning_en": en,
                               "region": reg, "source_type": "hf_dialect_norm_apache2",
                               "source_url": "https://huggingface.co/datasets/zmsali/bangla-dialect-normalization (Apache-2.0)",
                               "tags": ["dialect", "sentence_pair"]})
except Exception as e:
    print("hf ERR", e)
json.dump(hf_dialect, open(RAW + "/parse_v2_hf_dialect.json", "w"), ensure_ascii=False)
print(f"hf dialect pairs: {len(hf_dialect)}")

# copy dialect-normalization reference
try:
    import urllib.request
    with urllib.request.urlopen("https://huggingface.co/datasets/zmsali/bangla-dialect-normalization/resolve/main/README.md") as r:
        open(REF + "/hf_dialect_norm_README.txt", "wb").write(r.read())
except Exception:
    pass

# ---------------- Firecrawl2 markdown -> candidates ----------------
JUNK = re.compile(r"(Source:|Share this|Leave a comment|Follow us|Subscribe|Advertisement|©|All rights reserved|Privacy Policy|Cookie|related posts?|Read more)", re.I)
BN = re.compile(r"[\u0980-\u09FF]")
candidates = []
seen_c = set()
for fp in sorted(glob.glob(RAW + "/firecrawl2/pages/*.md")):
    txt = open(fp, encoding="utf-8").read()
    url = ""
    m = re.search(r"url: (\S+)", txt)
    if m:
        url = m.group(1)
    # dash lists and table rows with bn word + meaning
    for line in txt.split("\n"):
        line = line.strip().lstrip("-*|").strip()
        if len(line) < 8 or JUNK.search(line):
            continue
        # pattern: bangla text ... (latin or meaning)
        mm = re.match(r"^\*{0,2}([\u0980-\u09FF][\u0980-\u09FF\s]{1,30}?)\*{0,2}\s*[-–—:|=]+\s*(.{3,120})$", line)
        if not mm:
            mm = re.match(r"^\*{0,2}([\u0980-\u09FF][\u0980-\u09FF\s]{1,30}?)\*{0,2}\s*=\s*(.{3,120})$", line)
        if mm:
            term, mean = mm.group(1).strip(), mm.group(2).strip()
            term = re.sub(r"\s+", " ", term)
            if not (2 <= len(term) <= 32) or norm(term) in seen_c:
                continue
            if any(x in mean.lower() for x in ["http", "www.", ".com", "facebook", "youtube"]):
                continue
            seen_c.add(norm(term))
            candidates.append({"term_bn": term, "meaning_en": mean, "source_type": "fc2_web_auto",
                               "source_url": url, "tier": 4, "tags": ["auto_extract"]})
json.dump(candidates, open(RAW + "/parse_v2_fc.json", "w"), ensure_ascii=False)
print(f"firecrawl2 candidates: {len(candidates)}")

# ---------------- wt2 (if wiktionary succeeded) ----------------
wt2_parsed = []
def clean_wt(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("'''", "").replace("''", "").replace("[[", "").replace("]]", "")
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    return s.strip()

def parse_wt_dict(wtdict, lang_labels, source_type, base_url):
    out = []
    for title, wt in wtdict.items():
        lang_re = re.compile(r"==\s*(" + "|".join(lang_labels) + r")\s*==")
        m = lang_re.search(wt)
        if not m:
            continue
        seg = wt[m.end():]
        nxt = re.search(r"\n==[^=]", seg)
        if nxt:
            seg = seg[:nxt.start()]
        pos = "noun"
        for line in seg.split("\n"):
            pm = re.match(r"===\s*([A-Za-z ]+)\s*===", line)
            if pm:
                pos = pm.group(1).strip().lower()
                continue
            sm = re.match(r"#\s*(.+)", line)
            if sm:
                body = sm.group(1)
                tags = re.findall(r"\{\{lb\|bn\|([^}]+)\}\}|\{\{label\|bn\|([^}]+)\}\}", body)
                tagset = []
                for a, b in tags:
                    tagset += [x.strip() for x in (a or b).split("|") if x.strip()]
                gloss = clean_wt(re.sub(r"\{\{[^}]*\}\}", "", body))
                gloss = re.sub(r"^\s*[\[\(]?\d*[\]\)]?\s*", "", gloss).strip(" .;")
                ex_m = re.search(r"\{\{ux\|bn\|([^|}]+)(?:\|\|([^|}]+))?", wt)
                if gloss and 3 < len(gloss) < 250 and BN.search(title):
                    e = {"term_bn": title, "meaning_en": gloss, "part_of_speech": pos,
                         "source_type": source_type, "tags": tagset[:5],
                         "source_url": base_url + "/wiki/" + title.replace(" ", "_")}
                    if ex_m:
                        e["usage_example_bn"] = ex_m.group(1).strip()
                        if ex_m.group(2):
                            e["usage_example_en"] = ex_m.group(2).strip()
                    out.append(e)
    return out

wt2f = RAW + "/wt2_en_wikitext.json"
if os.path.exists(wt2f) and os.path.getsize(wt2f) > 100:
    d = json.load(open(wt2f))
    wt2_parsed += parse_wt_dict(d, ["Bengali", "Sylheti", "Chittagonian"], "wiktionary_en_v2", "https://en.wiktionary.org")
bn2f = RAW + "/wt2_bn_wikitext.json"
if os.path.exists(bn2f) and os.path.getsize(bn2f) > 100:
    d = json.load(open(bn2f))
    wt2_parsed += parse_wt_dict(d, ["বাংলা"], "wiktionary_bn_v2", "https://bn.wiktionary.org")
json.dump(wt2_parsed, open(RAW + "/parse_v2_wt2.json", "w"), ensure_ascii=False)
print(f"wt2 parsed: {len(wt2_parsed)}")
print("PARSE V2 DONE")
