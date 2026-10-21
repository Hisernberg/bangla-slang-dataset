#!/usr/bin/env python3
"""Probe remaining scraper APIs: ScrapeGraphAI, Browse AI, Browserbase, CrawlForge.
Each gets a real Bangla-slang scrape task; status recorded for README methodology."""
import json, os, urllib.request, ssl, time

ctx = ssl.create_default_context()
OUT = {}

def post(url, key, body, extra_headers=None, name=""):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if key: headers["Authorization"] = f"Bearer {key}"
    if extra_headers: headers.update(extra_headers)
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            data = r.read().decode()
        OUT[name] = {"status": "ok", "http": 200, "secs": round(time.time()-t0,1), "bytes": len(data)}
        return data
    except Exception as e:
        OUT[name] = {"status": "error", "err": str(e)[:200], "secs": round(time.time()-t0,1)}
        return None

def get(url, key, extra_headers=None, name=""):
    headers = {"Accept": "application/json"}
    if key: headers["Authorization"] = f"Bearer {key}"
    if extra_headers: headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            data = r.read().decode()
        OUT[name] = {"status": "ok", "http": 200, "bytes": len(data)}
        return data
    except Exception as e:
        OUT[name] = {"status": "error", "err": str(e)[:200]}
        return None

# 1. ScrapeGraphAI smartscraper — LLM extraction of slang list from a page
sgai = post("https://api.scrapegraphai.com/v1/smartscraper", os.environ.get("SGAI_API_KEY", ""), {
    "website_url": "https://ling-app.com/blog/bengali-slang-words/",
    "user_prompt": "Extract every Bengali slang word from this page. Return a JSON list of objects with fields: slang_bn (Bengali script), romanization, english_meaning, context_note.",
    "output_schema": {
        "type": "object",
        "properties": {
            "slangs": {"type": "array", "items": {"type": "object", "properties": {
                "slang_bn": {"type": "string"}, "romanization": {"type": "string"},
                "english_meaning": {"type": "string"}, "context_note": {"type": "string"}}}}
        }
    }
}, name="scrapegraphai_smartscraper")
if sgai:
    open("/home/z/my-project/bangla-slang-dataset/data/raw/scrapegraphai_lingapp.json", "w").write(sgai)
    print("ScrapeGraphAI result head:", sgai[:300])

# 2. Browse AI — list robots
browsai = get("https://api.browse.ai/v2/robots", os.environ.get("BROWSEAI_API_KEY", ""), name="browseai_robots")
if browsai:
    d = json.loads(browsai)
    robots = d.get("resultObject", {}).get("robots", [])
    print("BrowseAI robots:", len(robots), [r.get('name') for r in robots][:5])

# 3. Browserbase — create session
bb = post("https://api.browserbase.com/v1/sessions", os.environ.get("BROWSERBASE_API_KEY", ""), {}, name="browserbase_session")
if bb:
    d = json.loads(bb)
    print("Browserbase session:", d.get("id"), d.get("status"))
    OUT["browserbase_session"]["session_id"] = d.get("id")

# 4. CrawlForge — probe common endpoints
for ep, nm in [
    ("https://api.crawlforge.dev/v1/scrape?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FDhakaiya_Kutti_dialect", "crawlforge_scrape"),
    ("https://crawlforge.net/api/scrape?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FDhakaiya_Kutti_dialect", "crawlforge_alt"),
]:
    r = get(ep, os.environ.get("CRAWLFORGE_API_KEY", ""), name=nm)
    if r: print(nm, "head:", r[:150])

json.dump(OUT, open("/home/z/my-project/bangla-slang-dataset/data/raw/api_probe_results.json", "w"), indent=1)
print(json.dumps(OUT, indent=1))
