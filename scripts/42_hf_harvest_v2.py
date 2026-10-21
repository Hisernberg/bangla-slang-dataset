#!/usr/bin/env python3
"""v2 HuggingFace harvest: search hub for bengali/bangla slang-abuse-dialect datasets, sample rows via datasets-server."""
import json, os, time, urllib.request, urllib.parse, ssl, re

TOKEN = os.environ.get("HF_TOKEN", "")
RAW = "/home/z/my-project/bangla-slang-dataset/data/raw/hf"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()

def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "bangla-slang-collector/2.0",
                                             **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(r, timeout=60, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

QUERIES = ["bengali slang", "bangla slang", "bengali abusive", "bangla abusive",
           "bengali hate", "bangla toxic", "sylheti", "chittagonian", "bangla dialect",
           "bengali offensive", "banglish", "bengali profanity"]
found = {}
for q in QUERIES:
    try:
        d = get("https://huggingface.co/api/datasets?search=" + urllib.parse.quote(q) + "&limit=50&full=false")
        for it in d:
            did = it.get("id", "")
            if did not in found:
                found[did] = {"id": did, "query": q,
                              "downloads": it.get("downloads", 0), "likes": it.get("likes", 0),
                              "tags": it.get("tags", [])[:12], "url": f"https://huggingface.co/datasets/{did}"}
        print(f"{q}: +{len(d)}", flush=True)
    except Exception as e:
        print(f"ERR {q}: {e}", flush=True)
    time.sleep(1)

# relevance filter
rel = []
for did, meta in found.items():
    s = did.lower() + " " + " ".join(meta["tags"]).lower()
    if any(k in s for k in ["slang", "abus", "toxic", "hate", "offens", "profan", "sylhet", "chittag", "dialect", "sentiment", "comment"]):
        if "bengali" in s or "bangla" in s or "sylhet" in s or "chittag" in s:
            rel.append(meta)
rel.sort(key=lambda m: -m["downloads"])
print(f"relevant datasets: {len(rel)}", flush=True)
json.dump(rel, open(RAW + "/hf_manifest.json", "w"), indent=1)

def rows_endpoint(did, cfg, split, offset, length=100):
    u = (f"https://datasets-server.huggingface.co/rows?dataset={urllib.parse.quote(did)}"
         f"&config={urllib.parse.quote(cfg)}&split={urllib.parse.quote(split)}&offset={offset}&length={length}")
    return get(u)

def try_dataset(did):
    try:
        info = get(f"https://datasets-server.huggingface.co/splits?dataset={urllib.parse.quote(did)}")
        splits = info.get("splits", [])
        if not splits:
            return None
        cfg, split = splits[0]["config"], splits[0]["split"]
        rows_all = []
        for off in range(0, 400, 100):
            d = rows_endpoint(did, cfg, split, off)
            rows_all.extend(d.get("rows", []))
            time.sleep(0.5)
        return {"config": cfg, "split": split, "rows": rows_all}
    except Exception as e:
        print(f"  rows ERR {did}: {e}", flush=True)
        return None

results = {}
for meta in rel[:25]:
    did = meta["id"]
    print(f"PULL {did}", flush=True)
    d = try_dataset(did)
    if d and d["rows"]:
        results[did] = {**meta, **d, "row_count": len(d["rows"])}
        json.dump(results, open(RAW + "/hf_rows.json", "w"), ensure_ascii=False)
    time.sleep(1)

print(f"DONE hf datasets pulled: {len(results)}", flush=True)
