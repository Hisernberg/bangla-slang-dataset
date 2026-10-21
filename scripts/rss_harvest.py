#!/usr/bin/env python3
"""V3: RSS — Bangla news headlines corpus (reference/trend layer)."""
import csv, re, xml.etree.ElementTree as ET
import requests

REPO = "/home/z/my-project/bangla-slang-dataset"
FEEDS = [
    ("bbc_bangla", "https://feeds.bbci.co.uk/bengali/rss.xml"),
    ("prothom_alo", "https://www.prothomalo.com/feed/"),
    ("bdnews24_bn", "https://bangla.bdnews24.com/feed"),
    ("jugantor", "https://www.jugantor.com/feed/rss.xml"),
    ("kaler_kantho", "https://www.kalerkantho.com/rss.xml"),
]
UA = {"User-Agent": "Mozilla/5.0 (research dataset collection)"}

def main():
    rows = []
    for name, url in FEEDS:
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code != 200:
                print(f"[fail {r.status_code}] {name}"); continue
            root = ET.fromstring(r.content)
            items = root.findall(".//item")
            n = 0
            for it in items:
                title = re.sub(r"\s+", " ", (it.findtext("title") or "").strip())
                desc = re.sub(r"\s+", " ", (it.findtext("description") or "").strip())[:250]
                link = (it.findtext("link") or "").strip()
                pub = (it.findtext("pubDate") or "").strip()
                if title:
                    rows.append([name, title, desc, link, pub]); n += 1
            print(f"[ok] {name}: {n} items")
        except Exception as e:
            print(f"[err] {name}: {e}")
    with open(f"{REPO}/data/corpus/news_rss/headlines_bn.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["feed", "title_bn", "description_bn", "link", "published"])
        w.writerows(rows)
    print(f"DONE headlines={len(rows)}")

import os
os.makedirs(f"{REPO}/data/corpus/news_rss", exist_ok=True)
main()
