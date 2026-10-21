#!/usr/bin/env python3
"""v2 Reddit harvest: public JSON API — r/bangladesh, r/Dhaka slang threads + comments."""
import json, os, time, urllib.request, urllib.parse, ssl, gzip

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw/reddit"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36 bangla-slang-research/2.0"}

def get_json(url):
    r = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(r, timeout=45, context=ctx) as resp:
        data = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return json.loads(data.decode("utf-8", "replace"))

threads = {}
for sub, q in [("bangladesh", "slang"), ("bangladesh", "bangla slang words"),
               ("bangladesh", "gali"), ("Dhaka", "slang"),
               ("bdMuslims", "slang"), ("bangladesh", "dhakaiya")]:
    try:
        u = f"https://www.reddit.com/r/{sub}/search.json?q={urllib.parse.quote(q)}&restrict_sr=on&limit=40&sort=comments"
        d = get_json(u)
        for c in d.get("data", {}).get("children", []):
            p = c.get("data", {})
            tid = p.get("id")
            if tid and tid not in threads:
                threads[tid] = {"sub": sub, "title": p.get("title", ""),
                                "selftext": (p.get("selftext") or "")[:4000],
                                "permalink": "https://www.reddit.com" + p.get("permalink", ""),
                                "score": p.get("score", 0), "num_comments": p.get("num_comments", 0)}
        print(f"{sub}/{q}: {len(d.get('data',{}).get('children',[]))}", flush=True)
    except Exception as e:
        print(f"ERR {sub}/{q}: {str(e)[:100]}", flush=True)
    time.sleep(3)

# fetch top comments for threads with most comments
top = sorted(threads.values(), key=lambda t: -t["num_comments"])[:25]
out = {"threads": list(threads.values()), "comments": {}}
for t in top:
    try:
        d = get_json(t["permalink"].rstrip("/") + ".json?limit=500&sort=top")
        cs = []
        for c in d[1]["data"]["children"] if len(d) > 1 else []:
            body = (c.get("data", {}) or {}).get("body", "")
            if body and body not in ("[deleted]", "[removed]"):
                cs.append(body[:1500])
        out["comments"][t["permalink"]] = cs
        print(f"COMMENTS {t['permalink']}: {len(cs)}", flush=True)
    except Exception as e:
        print(f"ERR comments: {str(e)[:100]}", flush=True)
    time.sleep(3)

json.dump(out, open(RAW + "/reddit_threads.json", "w"), ensure_ascii=False, indent=1)
print(f"DONE reddit: {len(threads)} threads, {sum(len(v) for v in out['comments'].values())} comments", flush=True)
