#!/usr/bin/env python3
"""v3.2: pull Urban Dictionary (keyless) definitions for EN source terms of the XLM layer.
Evidence cache -> /home/z/my-project/harvest_v31/ud_evidence_v32.json"""
import json, time, urllib.request, urllib.parse, importlib.util, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

S = "/home/z/my-project/scripts/v32"
mods = [load(f"{S}/xlm_en_core.py", "c"), load(f"{S}/xlm_en_internet.py", "i"), load(f"{S}/xlm_en_idioms_uk_au.py", "u")]
terms = []
for m in mods:
    for e in m.ENTRIES:
        t = e["source_term"].strip().lower()
        if e["source_lang"] in ("en", "en-GB", "en-AU") and t not in terms:
            terms.append(t)
print(f"EN source terms: {len(terms)}", flush=True)

OUT = "/home/z/my-project/harvest_v31/ud_evidence_v32.json"
try:
    cache = json.load(open(OUT))
except Exception:
    cache = {}

def clean(s):
    return s.replace("[", "").replace("]", "").strip()[:400]

ok = 0
for i, t in enumerate(terms):
    if t in cache and cache[t]:
        continue
    url = "https://api.urbandictionary.com/v0/define?term=" + urllib.parse.quote(t)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode())
        lst = data.get("list") or []
        if lst:
            top = sorted(lst, key=lambda d: -(d.get("thumbs_up") or 0))[0]
            cache[t] = {"defid": top.get("defid"), "definition": clean(top.get("definition", "")),
                        "example": clean(top.get("example", "")), "thumbs_up": top.get("thumbs_up")}
            ok += 1
        else:
            cache[t] = None
    except Exception as e:
        cache[t] = None
        print(f"  miss {t}: {type(e).__name__}", flush=True)
    if (i + 1) % 25 == 0:
        json.dump(cache, open(OUT, "w"), ensure_ascii=False, indent=1)
        print(f"  {i+1}/{len(terms)} done (hits this run: {ok})", flush=True)
    time.sleep(0.25)

json.dump(cache, open(OUT, "w"), ensure_ascii=False, indent=1)
hits = sum(1 for v in cache.values() if v)
print(f"UD evidence: {hits}/{len(cache)} terms with definitions -> {OUT}")
