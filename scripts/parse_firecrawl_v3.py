#!/usr/bin/env python3
"""V3: parse Firecrawl docs into structured glossed slang candidates."""
import json, re

RAW = "/home/z/my-project/v3_raw"
docs = {d["url"]: d["markdown"] for d in json.load(open(f"{RAW}/firecrawl_docs.json"))}
out = {}

# ---- 1. ling-app: full slang entries (Kolkata-flavored Bengali) ----
la = docs["https://ling-app.com/blog/bengali-slang-words"]
ling = []
for m in re.finditer(r"###\s*\d+\\\.\s*([^–-]+)\s*[–-]\s*([^(]+)\(?([^)]*)\)?\n\n(.{0,700}?)\n\n", la):
    en, rom, bn, body = (x.strip().replace("\\.", "") for x in m.groups())
    ex = re.search(r"\|\s*[^|]+\|\s*([^\n|]*[\u0980-\u09FF][^\n|]*)\|\s*([^|\n]*)\|", body)
    meaning = body.split("\n")[0][:220]
    ling.append({"term_bn": bn, "romanization": rom.strip(), "meaning_en": en.strip(),
                 "note": meaning, "example_bn": ex.group(1).strip() if ex else "",
                 "example_rom": ex.group(2).strip() if ex else "", "region": "kolkata_india",
                 "source": "ling-app.com/bengali-slang-words"})
out["ling_app"] = ling

# ---- 2. Wiktionary Bengali slang category terms ----
wt = docs["https://en.wiktionary.org/wiki/Category:Bengali_slang"]
terms = re.findall(r"\d+\.\s*\[([^\]]+)\]\(https://en\.wiktionary\.org/wiki/", wt)
out["wiktionary_slang_terms"] = [t for t in terms if t != "Fundamental"]

# ---- 3. somewhereinblog 87 gaali list ----
sw = docs["https://m.somewhereinblog.net/mobile/blog/reanasblog/30135390"]
# body after the title; list items likely separated by <br> or newlines with ●/number/bangla
body = sw[sw.find("গালাগালির লিস্ট"):]
pieces = re.split(r"\n+|\|", body)
gls = []
for p in pieces:
    p = p.strip()
    if 6 <= len(p) <= 70 and sum(1 for c in p if "\u0980" <= c <= "\u09FF") >= 4 and "http" not in p and "![" not in p:
        gls.append(p)
out["somewherein_gaali"] = gls[:120]

# ---- 4. omniglot Sylheti phrases table ----
om = docs["https://www.omniglot.com/language/phrases/sylheti.htm"]
syl = []
for row in re.findall(r"^\s*\|([^|]+)\|([^|]+)\|([^|]+)\|", om, re.M):
    a, b, c = (x.strip().strip("*_") for x in row)
    if a.lower() in ("english", ""): continue
    syl.append({"en": a, "col2": b[:60], "col3": c[:60]})
out["omniglot_sylheti"] = syl[:40]

# ---- 5. youswear content (try to find entries) ----
ys = docs["https://www.youswear.com/index.asp?language=Bengali"]
entries = re.findall(r"###\s*([^\n]{2,40})\s*\n+((?:(?!###).){0,300})", ys, re.S)
out["youswear_bengali_entries"] = [{"head": h.strip(), "body": b.strip()[:200]} for h, b in entries[:30]]

# ---- 6. prothom alo slang dictionary review: quoted bangla terms ----
pa = docs["https://en.prothomalo.com/opinion/yqlu6ra7r7"]
paterms = re.findall(r"[\"“'_]([\u0980-\u09FF][\u0980-\u09FF\s]{2,30})[\"”'_.]", pa)
out["prothomalo_terms"] = list(dict.fromkeys(t.strip() for t in paterms if len(t.strip()) >= 3))[:40]

json.dump(out, open(f"{RAW}/v3_glossed_candidates.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(f"{k}: {len(v)}")
print("\nLING-APP:", json.dumps(ling[:3], ensure_ascii=False, indent=1)[:800])
print("\nSYLHETI:", json.dumps(syl[:6], ensure_ascii=False, indent=1)[:500])
print("\nGAALI SAMPLE:", gls[:12])
print("\nPROTHOMALO:", out["prothomalo_terms"][:20])
