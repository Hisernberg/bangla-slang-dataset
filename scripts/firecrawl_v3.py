#!/usr/bin/env python3
"""V3: Firecrawl — scrape Tavily-discovered slang pages + targeted searches."""
import os, json, time, requests

KEY = os.environ.get("FIRECRAWL_KEY", "")
OUT = "/home/z/my-project/v3_raw"

# hand-picked highest-value URLs from Tavily discovery
SCRAPE_URLS = [
    "https://en.prothomalo.com/opinion/yqlu6ra7r7",
    "https://m.somewhereinblog.net",  # placeholder fixed below
]

SEARCHES = [
    "bangla gali list with meaning", "chittagonian slang words",
    "bangla campus slang university", "bangla rap slang words list",
    "bangla meme words dictionary", "sylheti dialect glossary",
    "bangla swear words romanized", "bangla slang 2024 gen z words",
]

def fc_scrape(url, tries=2):
    for i in range(tries):
        r = requests.post("https://api.firecrawl.dev/v2/scrape",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={"url": url, "formats": ["markdown"]}, timeout=90)
        if r.status_code == 200:
            return r.json().get("data", {}).get("markdown", "")
        time.sleep(3 * (i + 1))
    return ""

def fc_search(q):
    r = requests.post("https://api.firecrawl.dev/v2/search",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"query": q, "limit": 6}, timeout=90)
    if r.status_code == 200:
        return r.json().get("data", {}).get("web", []) or r.json().get("data", [])
    return []

def main():
    with open(f"{OUT}/tavily_urls.json") as f:
        tav = json.load(f)
    # pick scrape targets: reddit, blogs, wikis, linguistics, glossary pages
    picks = []
    for u in tav:
        d = u["url"].lower()
        if any(k in d for k in ["reddit.com", "somewhereinblog", "wiktionary", "wikipedia",
                                 "youswear", "ling-app", "omniglot", "prothomalo", "github.com",
                                 "talkpal", "researchgate"]):
            picks.append(u["url"])
    picks = list(dict.fromkeys(picks))[:16]
    print(f"scraping {len(picks)} URLs")
    docs = []
    for i, url in enumerate(picks):
        md = fc_scrape(url)
        if md and len(md) > 400:
            docs.append({"url": url, "chars": len(md), "markdown": md})
            print(f"[ok {i+1}/{len(picks)}] {len(md):6d} chars  {url[:80]}", flush=True)
        else:
            print(f"[fail {i+1}/{len(picks)}] {url[:80]}", flush=True)
        time.sleep(1)
    # targeted searches
    sdocs = []
    for q in SEARCHES:
        try:
            res = fc_search(q)
            sdocs.append({"query": q, "results": res})
            print(f"[search] {q}: {len(res)} results", flush=True)
        except Exception as e:
            print(f"[search-err] {q}: {e}", flush=True)
        time.sleep(1.2)
    with open(f"{OUT}/firecrawl_docs.json", "w") as f:
        json.dump(docs, f, ensure_ascii=False)
    with open(f"{OUT}/firecrawl_searches.json", "w") as f:
        json.dump(sdocs, f, ensure_ascii=False)
    print(f"DONE docs={len(docs)} searches={len(sdocs)} scrape_chars={sum(d['chars'] for d in docs)}")

if __name__ == "__main__":
    main()
