#!/usr/bin/env python3
"""v2 Kaggle harvest: Bearer-token API search + download small relevant datasets."""
import json, os, time, urllib.request, urllib.parse, ssl

TOKEN = os.environ.get("KAGGLE_TOKEN", "")
RAW = "/home/z/my-project/bangla-slang-dataset/data/raw/kaggle"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()

def api(path, params=None, raw=False):
    url = f"https://www.kaggle.com/api/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    r = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(r, timeout=90, context=ctx) as resp:
        data = resp.read()
        return data if raw else json.loads(data.decode("utf-8"))

QUERIES = ["bengali slang", "bangla slang", "bengali abusive", "bangla hate speech",
           "bengali text", "bangla toxic", "bengali nlp", "bangla sentiment",
           "bengali dialect", "bangla comments facebook"]
found = {}
for q in QUERIES:
    try:
        d = api("/datasets/list", {"search": q, "pageSize": 20})
        for it in d:
            ref = it.get("ref") or it.get("datasetRef") or ""
            if ref and ref not in found:
                found[ref] = {"ref": ref, "title": it.get("title", ""),
                              "size": it.get("totalBytes", 0), "votes": it.get("voteCount", 0),
                              "download_url": it.get("downloadUrl", ""),
                              "url": f"https://www.kaggle.com/datasets/{ref}", "query": q}
        print(f"{q}: +{len(d)}", flush=True)
    except Exception as e:
        print(f"ERR {q}: {e}", flush=True)
    time.sleep(1.5)

cand = sorted(found.values(), key=lambda x: -x["votes"])
rel = [c for c in cand if any(k in (c["title"] + " " + c["ref"]).lower()
                              for k in ["slang", "abus", "toxic", "hate", "sentiment", "text", "comment", "dialect", "nlp"])]
print(f"relevant: {len(rel)}", flush=True)
json.dump(rel, open(RAW + "/kaggle_manifest.json", "w"), indent=1)

for c in rel[:12]:
    ref = c["ref"]
    if c["size"] and c["size"] > 80_000_000:
        print(f"SKIP too big {ref}", flush=True)
        continue
    slug = ref.replace("/", "~")
    try:
        blob = api(f"/datasets/download/{ref}", raw=True)
        outp = RAW + f"/{slug}.zip"
        open(outp, "wb").write(blob)
        print(f"DOWNLOADED {ref}: {len(blob)//1024} KB", flush=True)
    except Exception as e:
        print(f"ERR dl {ref}: {e}", flush=True)
    time.sleep(2)

# unzip small archives
import zipfile
for f in os.listdir(RAW):
    if f.endswith(".zip"):
        try:
            zdir = RAW + "/" + f[:-4]
            os.makedirs(zdir, exist_ok=True)
            with zipfile.ZipFile(RAW + "/" + f) as z:
                z.extractall(zdir)
            print(f"UNZIPPED {f}", flush=True)
        except Exception as e:
            print(f"ERR unzip {f}: {e}", flush=True)
print("DONE kaggle", flush=True)
