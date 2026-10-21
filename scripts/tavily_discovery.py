#!/usr/bin/env python3
"""V3: Tavily discovery of Bangla slang glossaries + Telegram channel finder."""
import os, json, re, time, requests

KEY = os.environ.get("TAVILY_KEY", "")
OUT = "/home/z/my-project/v3_raw"

QUERIES = [
    "bangla slang dictionary list", "bangla gaali list", "বাংলা গালি list meaning",
    "chittagonian dialect words list", "sylheti language slang words",
    "banglish slang words list", "bangla meme phrases meaning",
    "bangla college campus slang", "dhaka street slang words",
    "bangla rap lyrics slang words", "bangla slang reddit r/bangladesh",
    "noakhali dialect words list", "চটগাইয়া বুলি শব্দ",
    "bangla funny slang meaning english", "bangla college university slang words list",
]

def main():
    urls, tg_channels, seen = [], set(), set()
    for q in QUERIES:
        try:
            r = requests.post("https://api.tavily.com/search", json={
                "api_key": KEY, "query": q, "max_results": 8,
                "search_depth": "basic"}, timeout=40).json()
            for res in r.get("results", []):
                u = res.get("url", "")
                if not u or u in seen: continue
                seen.add(u)
                urls.append({"url": u, "title": res.get("title", ""), "query": q,
                             "snippet": (res.get("content") or "")[:300]})
                m = re.search(r"t\.me/([A-Za-z0-9_]+)", u)
                if m: tg_channels.add(m.group(1))
            print(f"[tavily] {q}: +{len(r.get('results', []))}", flush=True)
        except Exception as e:
            print(f"[tavily-err] {q}: {e}", flush=True)
        time.sleep(0.6)
    # find telegram channels from snippets too
    for u in urls:
        m = re.search(r"t\.me/([A-Za-z0-9_]+)", u.get("snippet", ""))
        if m: tg_channels.add(m.group(1))
    with open(f"{OUT}/tavily_urls.json", "w") as f:
        json.dump(urls, f, ensure_ascii=False, indent=1)
    with open(f"{OUT}/telegram_channels.txt", "w") as f:
        f.write("\n".join(sorted(tg_channels)))
    print(f"DONE urls={len(urls)} tg_channels={sorted(tg_channels)}")

if __name__ == "__main__":
    main()
