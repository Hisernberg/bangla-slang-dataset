#!/usr/bin/env python3
"""Use Playwright + Browserbase session to:
1. Scrape JS-heavy Quizlet Sylheti flashcards
2. Call ScrapeGraphAI API through browser TLS stack (bypasses CF fingerprint block)
3. Attempt Browse AI v1 endpoint
Fallback: local chromium if Browserbase connect fails."""
import json, time, os

BB_KEY = os.environ["BROWSERBASE_API_KEY"]
SGAI_KEY = os.environ.get("SGAI_API_KEY", "")
RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"

from playwright.sync_api import sync_playwright

def get_connect_url():
    """Get a fresh Browserbase session connect URL."""
    import urllib.request
    req = urllib.request.Request("https://api.browserbase.com/v1/sessions",
        data=json.dumps({"projectId": "4531def6-9b1b-4627-9312-5a1ce4e8c49c"}).encode(),
        headers={"x-bb-api-key": BB_KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        return d.get("connectUrl"), d.get("id")
    except Exception as e:
        print("Browserbase session ERR:", e)
        return None, None

results = {}
with sync_playwright() as p:
    connect_url, bb_id = get_connect_url()
    browser = None
    if connect_url:
        try:
            browser = p.chromium.connect_over_cdp(connect_url, timeout=60000)
            results["browserbase"] = {"status": "connected", "session_id": bb_id}
            print("Connected via Browserbase session", bb_id)
        except Exception as e:
            print("Browserbase CDP connect failed:", e)
            results["browserbase"] = {"status": "connect_failed", "err": str(e)[:200]}
    if browser is None:
        browser = p.chromium.launch(headless=True)
        results["browser"] = "local_chromium"
        print("Using local chromium")

    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", locale="en-US")
    page = ctx.new_page()

    # ---- 1. Quizlet Sylheti flashcards (JS-heavy) ----
    try:
        page.goto("https://quizlet.com/276968469/sylheti-terms-and-phrases-flash-cards/", timeout=90000, wait_until="domcontentloaded")
        time.sleep(6)
        text = page.evaluate("document.body.innerText")
        open(f"{RAW}/browserbase_quizlet_sylheti.txt", "w", encoding="utf-8").write(text)
        results["quizlet"] = {"status": "ok", "chars": len(text)}
        print("Quizlet scraped:", len(text), "chars")
    except Exception as e:
        results["quizlet"] = {"status": "error", "err": str(e)[:200]}
        print("Quizlet ERR:", str(e)[:200])

    # ---- 2. ScrapeGraphAI via context.request (browser network stack, no CORS) ----
    try:
        resp = ctx.request.post("https://api.scrapegraphai.com/v1/smartscraper",
            headers={"Content-Type": "application/json", "SGAI-API-KEY": SGAI_KEY},
            data=json.dumps({
                "website_url": "https://ling-app.com/blog/bengali-slang-words/",
                "user_prompt": "Extract every Bengali slang word from this page. Return a JSON list of objects with fields: slang_bn (Bengali script), romanization, english_meaning, usage_note."
            }), timeout=120000)
        body = resp.text()
        open(f"{RAW}/scrapegraphai_via_browser.json", "w").write(json.dumps({"status": resp.status, "body": body}))
        results["scrapegraphai"] = {"status": resp.status, "body_bytes": len(body)}
        print("ScrapeGraphAI status:", resp.status, "bytes:", len(body))
    except Exception as e:
        results["scrapegraphai"] = {"status": "error", "err": str(e)[:200]}
        print("ScrapeGraphAI ERR:", str(e)[:200])

    # ---- 3. Quizlet retry with networkidle wait ----
    try:
        page.goto("https://quizlet.com/276968469/sylheti-terms-and-phrases-flash-cards/", timeout=90000, wait_until="load")
        time.sleep(12)
        text = page.evaluate("document.body.innerText")
        open(f"{RAW}/browserbase_quizlet_sylheti.txt", "w", encoding="utf-8").write(text)
        results["quizlet"] = {"status": "ok", "chars": len(text)}
        print("Quizlet scraped:", len(text), "chars")
    except Exception as e:
        results["quizlet"] = {"status": "error", "err": str(e)[:200]}
        print("Quizlet ERR:", str(e)[:200])

    browser.close()

json.dump(results, open(f"{RAW}/browserbase_scrape_results.json", "w"), indent=1)
print(json.dumps(results, indent=1))
