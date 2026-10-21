#!/usr/bin/env python3
"""v2 Wiktionary harvest: NEW categories (idioms, phrases, interjections, Sylheti, Chittagonian, reduplications)."""
import json, urllib.request, urllib.parse, ssl, time, os, sys

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()
UA = {"User-Agent": "BanglaSlangDatasetCollector/2.0 (academic research)"}

def api(base, params):
    u = base + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        req = urllib.request.Request(u, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            wait = min(60, 5 * (2 ** attempt))
            print(f"  api retry {attempt+1} after {wait}s: {str(e)[:80]}", flush=True)
            time.sleep(wait)
    raise RuntimeError("api failed after retries")

def get_members(base, cat):
    cont, got = {}, []
    while True:
        p = {"action": "query", "list": "categorymembers", "cmtitle": cat,
             "cmlimit": "500", "format": "json", "cmtype": "page"}
        p.update(cont)
        try:
            d = api(base, p)
        except Exception as e:
            print(f"ERR {cat}: {e}", flush=True); break
        for m in d.get("query", {}).get("categorymembers", []):
            got.append(m["title"])
        if "continue" in d:
            cont = {"cmcontinue": d["continue"]["cmcontinue"]}
        else:
            break
        time.sleep(2.5)
    return got

def fetch_wikitext(base, titles):
    out, ts = {}, list(titles)
    for i in range(0, len(ts), 40):
        batch = ts[i:i+40]
        for attempt in range(3):
            try:
                d = api(base, {"action": "query", "prop": "revisions", "rvprop": "content",
                               "rvslots": "main", "titles": "|".join(batch), "format": "json"})
                break
            except Exception as e:
                print(f"  batch retry {i}: {e}", flush=True); time.sleep(2)
        else:
            continue
        for page in d.get("query", {}).get("pages", {}).values():
            if "revisions" in page:
                try:
                    out[page["title"]] = page["revisions"][0]["slots"]["main"]["*"]
                except Exception:
                    pass
        time.sleep(2.0)
        print(f"  wikitext {i+len(batch)}/{len(ts)}", flush=True)
    return out

EN_CATS = [
    "Category:Bengali idioms",
    "Category:Bengali phrases",
    "Category:Bengali interjections",
    "Category:Bengali similes",
    "Category:Bengali reduplications",
    "Category:Bengali onomatopoeias",
    "Category:Bengali sarcastic terms",
    "Category:Bengali jocular terms",
    "Category:Bengali childish terms",
    "Category:Sylheti lemmas",
    "Category:Sylheti slang",
    "Category:Sylheti vulgarities",
    "Category:Sylheti idioms",
    "Category:Chittagonian lemmas",
    "Category:Chittagonian vulgarities",
    "Category:Bengali nonstandard terms",
    "Category:Bengali terms with audio pronunciation",
]
BN_CATS = [
    "বিষয়শ্রেণী:বাংলা বাগধারা",
    "বিষয়শ্রেণী:বাংলা প্রবাদ বাক্য",
    "বিষয়শ্রেণী:ঢাকাইয়া কুট্টি ভাষা",
    "বিষয়শ্রেণী:বাংলা স্ল্যাং",
]

en_pages, bn_pages = {}, {}
for cat in EN_CATS:
    got = get_members("https://en.wiktionary.org/w/api.php", cat)
    print(f"EN {cat}: {len(got)}", flush=True)
    for t in got:
        en_pages.setdefault(t, set()).add(cat)
for cat in BN_CATS:
    got = get_members("https://bn.wiktionary.org/w/api.php", cat)
    print(f"BN {cat}: {len(got)}", flush=True)
    for t in got:
        bn_pages.setdefault(t, set()).add(cat)

print("UNIQUE en:", len(en_pages), "bn:", len(bn_pages), flush=True)
en_wt = fetch_wikitext("https://en.wiktionary.org/w/api.php", en_pages.keys())
bn_wt = fetch_wikitext("https://bn.wiktionary.org/w/api.php", bn_pages.keys())

json.dump({t: sorted(c) for t, c in en_pages.items()}, open(RAW + "/wt2_en_pages.json", "w"), ensure_ascii=False)
json.dump({t: sorted(c) for t, c in bn_pages.items()}, open(RAW + "/wt2_bn_pages.json", "w"), ensure_ascii=False)
json.dump(en_wt, open(RAW + "/wt2_en_wikitext.json", "w"), ensure_ascii=False)
json.dump(bn_wt, open(RAW + "/wt2_bn_wikitext.json", "w"), ensure_ascii=False)
print(f"SAVED wt2 en:{len(en_wt)} bn:{len(bn_wt)}", flush=True)
