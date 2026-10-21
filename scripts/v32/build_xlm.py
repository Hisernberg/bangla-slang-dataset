#!/usr/bin/env python3
"""v3.2 BUILD: cross-lingual reverse-mapping layer (XLM) + gold addendum into repo.
- loads 5 XLM data files -> dedupe -> master_link lookup -> UD evidence join
- writes data/final/crosslingual_mappings.{csv,json}
- merges gold_v32.json (anglicism_borrowings) into master, rebuilds by_category + stats
"""
import json, csv, os
from collections import defaultdict, Counter

REPO = "/home/z/my-project/repo"
H31 = "/home/z/my-project/harvest_v31"
S = "/home/z/my-project/scripts/v32"
import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

# ---------- 1. load XLM entries ----------
files = ["xlm_en_core.py", "xlm_en_internet.py", "xlm_en_idioms_uk_au.py", "xlm_hindi.py", "xlm_ur_ar_ko_ja_es.py", "xlm_wave2.py"]
raw = []
for f in files:
    raw.extend(load(f"{S}/{f}", f.replace(".py", "")).ENTRIES)
print(f"XLM raw: {len(raw)}", flush=True)

FIELDS = ["map_id", "source_lang", "source_term", "source_gloss_en", "bangla_native_equivalent",
          "bangla_codemixed_form", "bangla_romanization", "mapping_process", "register", "offensiveness",
          "domain", "usage_example_banglish", "usage_example_pure_bn", "example_source_lang",
          "process_note", "confidence", "source_evidence", "master_link"]

LANG_ORDER = {"en": 0, "en-GB": 1, "en-AU": 2, "hi": 3, "ur": 4, "ar": 5, "fa": 6, "ko": 7, "ja": 8, "es": 9}
seen = {}
for e in raw:
    key = (e["source_lang"], e["source_term"].strip().lower())
    if key in seen:
        continue
    seen[key] = e
rows = sorted(seen.values(), key=lambda e: (LANG_ORDER.get(e["source_lang"], 9), e["source_term"].lower()))
dedup = len(raw) - len(rows)
print(f"XLM deduped: {len(rows)} (removed {dedup})", flush=True)

# ---------- 2. master_link lookup ----------
master = json.load(open(f"{REPO}/data/final/bangla_slang_master.json"))
for m in master:
    if "tier" in m and not isinstance(m["tier"], str): m["tier"] = str(m["tier"])
    for k in ("popularity", "offensiveness"):
        if k in m and not isinstance(m[k], str): m[k] = str(m[k])
master_by_term = defaultdict(list)
for m in master:
    t = (m.get("term_bn") or "").strip()
    if t: master_by_term[t].append(m["id"])
    r = (m.get("romanization") or "").strip().lower()
    if r: master_by_term[r].append(m["id"])

def link(text):
    t = (text or "").strip()
    if not t: return ""
    # exact term match first
    for cand in [t] + [p.strip() for p in t.replace("/", " ").split() if len(p.strip()) >= 2]:
        ids = master_by_term.get(cand)
        if ids: return ids[0]
    return ""

n_link = 0
for e in rows:
    ml = link(e["bangla_codemixed_form"]) or link(e["bangla_native_equivalent"])
    e["master_link"] = ml
    if ml: n_link += 1
print(f"master_link resolved: {n_link}/{len(rows)}", flush=True)

# ---------- 3. UD evidence join ----------
try:
    ud = json.load(open(f"{H31}/ud_evidence_v32.json"))
except Exception:
    ud = {}
n_ud = 0
for e in rows:
    ev = ud.get(e["source_term"].strip().lower())
    if ev:
        e["source_evidence"] = f"UD#{ev['defid']}: {ev['definition'][:160]}"
        n_ud += 1
    else:
        e["source_evidence"] = ""
print(f"UD evidence joined: {n_ud}/{len(rows)}", flush=True)

# ---------- 4. write XLM files ----------
for i, e in enumerate(rows, 1):
    e["map_id"] = f"XLM-{i:04d}"
os.makedirs(f"{REPO}/data/final", exist_ok=True)
with open(f"{REPO}/data/final/crosslingual_mappings.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for e in rows: w.writerow({k: e.get(k, "") for k in FIELDS})
json.dump(rows, open(f"{REPO}/data/final/crosslingual_mappings.json", "w"), ensure_ascii=False, indent=1)
by_lang = Counter(e["source_lang"] for e in rows)
by_proc = Counter(e["mapping_process"] for e in rows)
print(f"XLM written: {len(rows)} rows", flush=True)
print("  by_lang:", dict(by_lang), flush=True)
print("  by_process:", dict(by_proc), flush=True)

# ---------- 5. gold v3.2 addendum into master ----------
gold = json.load(open(f"{H31}/gold_v32.json"))
existing = {(m["term_bn"] or "").strip().lower() for m in master}
nid = 3288
g_added = 0
for e in gold:
    if e["term_bn"].strip().lower() in existing: continue
    e["id"] = f"KS-{nid:04d}"; nid += 1
    existing.add(e["term_bn"].strip().lower())
    master.append(e); g_added += 1
print(f"gold added: {g_added}", flush=True)

# ---------- 6. rebuild by_category + master files + stats ----------
os.makedirs(f"{REPO}/data/final/by_category", exist_ok=True)
for old in os.listdir(f"{REPO}/data/final/by_category"):
    os.remove(f"{REPO}/data/final/by_category/{old}")
by_cat = defaultdict(list)
for m in master: by_cat[m["category"]].append(m)
for cat, catrows in by_cat.items():
    json.dump(catrows, open(f"{REPO}/data/final/by_category/{cat}.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{REPO}/data/final/by_category/{cat}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(catrows[0].keys()))
        w.writeheader()
        for m in catrows: w.writerow({k: m.get(k, "") for k in w.fieldnames})
with open(f"{REPO}/data/final/bangla_slang_master.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(master[0].keys()))
    w.writeheader()
    for m in master: w.writerow({k: m.get(k, "") for k in w.fieldnames})
json.dump(master, open(f"{REPO}/data/final/bangla_slang_master.json", "w"), ensure_ascii=False, indent=1)

by_tier = Counter(str(m.get("tier", "")) for m in master)
by_src = Counter(m.get("source_type", "") for m in master)
stats = {"total": len(master), "crosslingual_mappings": len(rows), "crosslingual_by_lang": dict(by_lang),
         "crosslingual_by_process": dict(by_proc), "by_category": dict(by_cat),
         "by_tier": {k: by_tier.get(k, 0) for k in ("1", "2", "3")}, "by_source_type": dict(by_src)}
json.dump(stats, open(f"{REPO}/data/final/stats.json", "w"), ensure_ascii=False, indent=1)
json.dump({"xlm_rows": len(rows), "ud_evidence_hits": n_ud, "master_link_hits": n_link,
           "gold_added": g_added, "master_total": len(master), "categories": len(by_cat)},
          open(f"{REPO}/data/provenance/xlm_build_manifest.json", "w"), ensure_ascii=False, indent=1)
print(f"MASTER: {len(master)} entries / {len(by_cat)} categories", flush=True)
print("v3.2 build complete", flush=True)
