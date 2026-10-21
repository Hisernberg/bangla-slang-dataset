#!/usr/bin/env python3
"""Harvest Wiktionary Bengali slang/informal/vulgar entries (en.wiktionary + bn.wiktionary categories)."""
import json, urllib.request, urllib.parse, ssl, time, re, os

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()
UA = {"User-Agent": "BanglaSlangDatasetCollector/1.0 (academic research; contact: research@example.org)"}

def api(url, params):
    u = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

# ---------- 1. en.wiktionary categories ----------
EN_CATS = [
    "Category:Bengali slang",
    "Category:Bengali vulgarities",
    "Category:Bengali vulgar slang",
    "Category:Bengali offensive terms",
    "Category:Bengali colloquialisms",
    "Category:Bengali derogatory terms",
    "Category:Bengali informal terms",
    "Category:Bengali insults",
    "Category:Bengali terms with usage examples",
]
en_pages = {}  # title -> category set
for cat in EN_CATS:
    cont = {}
    got = []
    while True:
        p = {"action": "query", "list": "categorymembers", "cmtitle": cat,
             "cmlimit": "500", "format": "json", "cmtype": "page"}
        p.update(cont)
        try:
            d = api("https://en.wiktionary.org/w/api.php", p)
        except Exception as e:
            print(f"ERR {cat}: {e}"); break
        for m in d.get("query", {}).get("categorymembers", []):
            got.append(m["title"])
        if "continue" in d:
            cont = {"cmcontinue": d["continue"]["cmcontinue"]}
        else:
            break
        time.sleep(0.3)
    print(f"{cat}: {len(got)} pages")
    for t in got:
        en_pages.setdefault(t, set()).add(cat)

print("TOTAL unique en.wiktionary pages:", len(en_pages))

# ---------- 2. bn.wiktionary categories ----------
BN_CATS = [
    "বিষয়শ্রেণী:ঢাকাইয়া কুট্টি ভাষার শব্দ",
    "বিষয়শ্রেণী:বাংলা স্ল্যাং",
    "বিষয়শ্রেণী:বাংলা গালি",
    "বিষয়শ্রেণী:বাংলা ভাষার শব্দ",
]
bn_pages = {}
for cat in BN_CATS:
    cont = {}
    got = []
    while True:
        p = {"action": "query", "list": "categorymembers", "cmtitle": cat,
             "cmlimit": "500", "format": "json", "cmtype": "page"}
        p.update(cont)
        try:
            d = api("https://bn.wiktionary.org/w/api.php", p)
        except Exception as e:
            print(f"ERR {cat}: {e}"); break
        for m in d.get("query", {}).get("categorymembers", []):
            got.append(m["title"])
        if "continue" in d:
            cont = {"cmcontinue": d["continue"]["cmcontinue"]}
        else:
            break
        time.sleep(0.3)
    print(f"{cat}: {len(got)} pages")
    for t in got:
        bn_pages.setdefault(t, set()).add(cat)

print("TOTAL unique bn.wiktionary pages:", len(bn_pages))

# ---------- 3. Fetch wikitext in batches (en) ----------
def fetch_wikitext(api_base, titles):
    out = {}
    ts = list(titles)
    for i in range(0, len(ts), 40):
        batch = ts[i:i+40]
        try:
            d = api(api_base, {"action": "query", "prop": "revisions", "rvprop": "content",
                               "rvslots": "main", "titles": "|".join(batch), "format": "json"})
        except Exception as e:
            print(f"  batch {i} ERR: {e}"); continue
        for page in d.get("query", {}).get("pages", {}).values():
            if "revisions" in page:
                try:
                    out[page["title"]] = page["revisions"][0]["slots"]["main"]["*"]
                except Exception:
                    pass
        time.sleep(0.4)
        print(f"  wikitext {api_base.split('//')[1][:12]} {i+len(batch)}/{len(ts)}")
    return out

en_wikitext = fetch_wikitext("https://en.wiktionary.org/w/api.php", en_pages.keys())
bn_wikitext = fetch_wikitext("https://bn.wiktionary.org/w/api.php", bn_pages.keys())

json.dump({t: sorted(c) for t, c in en_pages.items()}, open(RAW + "/wiktionary_en_pages.json", "w"), ensure_ascii=False)
json.dump({t: sorted(c) for t, c in bn_pages.items()}, open(RAW + "/wiktionary_bn_pages.json", "w"), ensure_ascii=False)
json.dump(en_wikitext, open(RAW + "/wiktionary_en_wikitext.json", "w"), ensure_ascii=False)
json.dump(bn_wikitext, open(RAW + "/wiktionary_bn_wikitext.json", "w"), ensure_ascii=False)
print(f"SAVED en:{len(en_wikitext)} bn:{len(bn_wikitext)} wikitext entries")
