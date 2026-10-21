#!/usr/bin/env python3
"""v2 API probes: ScrapeGraphAI, Browse AI, CrawlForge — try multiple endpoint variants, log results."""
import json, os, urllib.request, urllib.error, ssl, time

OUT = "/home/z/my-project/bangla-slang-dataset/data/raw/probe_v2.json"
ctx = ssl.create_default_context()
res = {}

def post(url, body, headers, timeout=45):
    r = urllib.request.Request(url, data=json.dumps(body).encode(),
                               headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(r, timeout=timeout, context=ctx) as resp:
        return resp.status, resp.read().decode("utf-8")[:1500]

def try_post(name, url, body, headers):
    try:
        s, b = post(url, body, headers)
        res[name] = {"url": url, "status": s, "body_head": b}
        print(f"OK {name} {s}", flush=True)
    except urllib.error.HTTPError as e:
        res[name] = {"url": url, "status": e.code, "err": e.read().decode()[:300]}
        print(f"HTTP {name} {e.code}", flush=True)
    except Exception as e:
        res[name] = {"url": url, "err": str(e)[:300]}
        print(f"ERR {name}: {str(e)[:120]}", flush=True)

SGAI = os.environ.get("SGAI_KEY", "")
if SGAI:
    for ep in ["https://api.scrapegraphai.com/v1/smartscraper", "https://api.scrapegraphai.com/v2/smartscraper"]:
        try_post(f"scrapegraph@{ep}", ep,
                 {"api_key": SGAI, "website_url": "https://en.wiktionary.org/wiki/%E0%A6%95%E0%A6%BE%E0%A6%9F%E0%A6%BE",
                  "user_prompt": "Extract the slang word, its meaning and an example sentence.",
                  "llm": "gpt-4o-mini"},
                 {})
    time.sleep(1)

BAI = os.environ.get("BROWSEAI_KEY", "")
if BAI:
    for ep, hd in [("https://api.browse.ai/v2/robots", {"Authorization": f"Bearer {BAI}"}),
                   ("https://api.browse.ai/v2/robots", {"Apikey": BAI}),
                   ("https://api.browse.ai/v2/tasks", {"Authorization": f"Bearer {BAI}"})]:
        try:
            r = urllib.request.Request(ep, headers={"User-Agent": "curl/8", **hd})
            with urllib.request.urlopen(r, timeout=30, context=ctx) as resp:
                res[f"browseai@{hd['User-Agent']}@{ep}"] = {"status": resp.status, "body": resp.read().decode()[:400]}
                print(f"OK browseai {resp.status}", flush=True)
        except urllib.error.HTTPError as e:
            res[f"browseai@{ep}"] = {"status": e.code, "err": e.read().decode()[:200]}
            print(f"HTTP browseai {e.code}", flush=True)
        except Exception as e:
            res[f"browseai@{ep}"] = {"err": str(e)[:200]}
            print(f"ERR browseai: {str(e)[:120]}", flush=True)
        time.sleep(1)

CF = os.environ.get("CRAWLFORGE_KEY", "")
if CF:
    for host in ["https://api.crawlforge.net", "https://api.crawlforge.dev", "https://crawlforge.net/api"]:
        try_post(f"crawlforge@{host}", host + "/v1/scrape",
                 {"url": "https://example.com", "apiKey": CF}, {"Authorization": f"Bearer {CF}"})
        try:
            r = urllib.request.Request(host + f"/scrape?url=https://example.com&token={CF}",
                                       headers={"User-Agent": "curl/8"})
            with urllib.request.urlopen(r, timeout=30, context=ctx) as resp:
                res[f"crawlforge-get@{host}"] = {"status": resp.status, "body": resp.read().decode()[:300]}
                print(f"OK crawlforge GET {resp.status}", flush=True)
        except Exception as e:
            res[f"crawlforge-get@{host}"] = {"err": str(e)[:200]}
            print(f"ERR crawlforge GET: {str(e)[:120]}", flush=True)
        time.sleep(1)

BB = os.environ.get("BROWSERBASE_KEY", "")
if BB:
    try_post("browserbase-sessions", "https://www.browserbase.com/v1/sessions", {}, {"x-bb-api-key": BB})

json.dump(res, open(OUT, "w"), indent=1)
print("PROBES DONE", flush=True)
