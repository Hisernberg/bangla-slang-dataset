#!/usr/bin/env python3
"""Final ScrapeGraphAI attempt: navigate to api.scrapegraphai.com, then same-origin fetch (no CORS)."""
import json, time
from playwright.sync_api import sync_playwright

SGAI_KEY = os.environ.get("SGAI_API_KEY", "")
RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36")
    page = ctx.new_page()
    out = {}
    try:
        page.goto("https://api.scrapegraphai.com/", timeout=60000, wait_until="domcontentloaded")
        time.sleep(2)
        r = page.evaluate("""async (key) => {
            const resp = await fetch('/v1/smartscraper', {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'SGAI-API-KEY': key},
                body: JSON.stringify({
                    website_url: 'https://ling-app.com/blog/bengali-slang-words/',
                    user_prompt: 'Extract every Bengali slang word from this page. Return a JSON list of objects with fields: slang_bn (Bengali script), romanization, english_meaning, usage_note.'
                })
            });
            return {status: resp.status, body: await resp.text()};
        }""", SGAI_KEY)
        open(f"{RAW}/scrapegraphai_final.json", "w").write(json.dumps(r))
        out = {"status": r["status"], "bytes": len(r["body"])}
        print("ScrapeGraphAI:", r["status"], len(r["body"]), "bytes")
    except Exception as e:
        out = {"status": "error", "err": str(e)[:300]}
        print("ScrapeGraphAI ERR:", str(e)[:300])
    browser.close()

json.dump(out, open(f"{RAW}/scrapegraphai_final_status.json", "w"), indent=1)
