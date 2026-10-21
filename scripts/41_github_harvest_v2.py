#!/usr/bin/env python3
"""v2 GitHub harvest: search for more Bangla slang/profanity/dialect repos, fetch raw text files."""
import json, os, time, urllib.request, urllib.parse, ssl

TOKEN = os.environ.get("GH_TOKEN", "")
RAW = "/home/z/my-project/bangla-slang-dataset/data/raw/gh"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()
UA = {"User-Agent": "bangla-slang-collector-2.0"}

def req(url, headers=None, as_json=True):
    h = dict(UA)
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    if headers:
        h.update(headers)
    r = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(r, timeout=60, context=ctx) as resp:
        data = resp.read()
        return json.loads(data.decode("utf-8")) if as_json else data

QUERIES = [
    "bangla slang", "bengali slang", "bangla profanity", "bengali profanity",
    "bangla abusive words", "bengali abuse list", "banglish words", "bangla gali list",
    "sylheti words", "chittagonian words", "bangla dialect dataset", "bangla slur",
    "bangla toxic lexicon", "bangla hate words",
]
repos = {}
for q in QUERIES:
    try:
        d = req("https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + "&per_page=20")
        for it in d.get("items", []):
            repos[it["full_name"]] = {
                "full_name": it["full_name"], "stars": it["stargazers_count"],
                "license": (it.get("license") or {}).get("spdx_id", ""),
                "desc": it.get("description", ""), "url": it["html_url"], "query": q,
            }
        print(f"{q}: {d.get('total_count')} results", flush=True)
    except Exception as e:
        print(f"ERR {q}: {e}", flush=True)
    time.sleep(2)

# rank: stars desc, keep interesting ones
cand = sorted(repos.values(), key=lambda r: -r["stars"])
print(f"unique repos: {len(cand)}", flush=True)

keep = []
for r in cand:
    name = r["full_name"].lower()
    desc = (r["desc"] or "").lower()
    if any(k in name + " " + desc for k in ["slang", "profan", "abuse", "gali", "gaali", "toxic", "hate", "dialect", "sylhet", "chittag", "swear", "curse", "banglish", "lexicon", "obscen", "vulgar"]):
        keep.append(r)
print(f"relevant repos: {len(keep)}", flush=True)

manifest = []
for r in keep[:60]:
    fn, branch = r["full_name"], "HEAD"
    try:
        tree = req(f"https://api.github.com/repos/{fn}/git/trees/{branch}?recursive=1")
        files = [t for t in tree.get("tree", [])
                 if t.get("type") == "blob" and (t.get("size") or 0) < 3_000_000
                 and t["path"].lower().endswith((".csv", ".json", ".jsonl", ".txt", ".tsv", ".md"))]
        saved = 0
        repo_dir = RAW + "/" + fn.replace("/", "__")
        os.makedirs(repo_dir, exist_ok=True)
        for t in files[:15]:
            p = t["path"]
            low = p.lower()
            if not any(k in low for k in ["slang", "profan", "abuse", "gali", "toxic", "hate", "swear", "word", "lexicon", "term", "dialect", "data", "corpus", "list"]) and not low.endswith((".csv", ".json", ".jsonl")):
                continue
            try:
                raw_url = f"https://raw.githubusercontent.com/{fn}/HEAD/{urllib.parse.quote(p)}"
                blob = req(raw_url, as_json=False)
                if b"\x00" in blob[:2000]:
                    continue
                outp = repo_dir + "/" + p.replace("/", "__")
                open(outp, "wb").write(blob)
                saved += 1
                time.sleep(0.4)
            except Exception:
                pass
        if saved:
            manifest.append({**r, "files_saved": saved, "file_list": [t["path"] for t in files[:15]]})
            print(f"SAVED {fn}: {saved} files", flush=True)
        json.dump(manifest, open(RAW + "/manifest.json", "w"), indent=1)
    except Exception as e:
        print(f"ERR tree {fn}: {e}", flush=True)
    time.sleep(1.5)

print(f"DONE. repos with files: {len(manifest)}", flush=True)
