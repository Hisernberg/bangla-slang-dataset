#!/usr/bin/env python3
"""Extract all markdown from firecrawl search/scrape JSONs into .md files."""
import json, glob, os, re, hashlib

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl"
MD = RAW + "/md"
os.makedirs(MD, exist_ok=True)
manifest = []

def safe_name(u):
    return re.sub(r'[^a-zA-Z0-9]+', '_', u.replace('https://','').replace('http://',''))[:80]

for f in sorted(glob.glob(RAW + "/*.json")):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    tag = os.path.basename(f).replace('search_','').replace('scrape_','').replace('.json','')
    docs = []
    if f.endswith('.json') and isinstance(d.get('data'), dict):
        web = d.get('data', {}).get('web', [])
        if web:
            docs = [(x.get('url',''), x.get('title',''), x.get('markdown','') or '') for x in web if isinstance(x, dict)]
        elif d.get('data', {}).get('markdown'):
            docs = [(d['data'].get('url', d.get('metadata', {}).get('url','')), d['data'].get('metadata', {}).get('title',''), d['data']['markdown'])]
    elif isinstance(d.get('data'), dict) and d['data'].get('markdown'):
        m = d['data']
        url = m.get('metadata', {}).get('url', m.get('url',''))
        docs = [(url, m.get('metadata',{}).get('title',''), m['markdown'])]
    for url, title, md in docs:
        if len(md) < 500:
            continue
        name = safe_name(url or tag)
        out = f"{MD}/{name}.md"
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(f"---\nsource_url: {url}\ntitle: {title}\ncollection_tag: {tag}\n---\n\n{md}")
        manifest.append({"tag": tag, "url": url, "title": title, "file": out, "chars": len(md)})

json.dump(manifest, open(RAW + "/manifest.json", "w"), ensure_ascii=False, indent=1)
print(f"extracted {len(manifest)} markdown docs, total {sum(m['chars'] for m in manifest)} chars")
for m in sorted(manifest, key=lambda x: -x['chars'])[:40]:
    print(f"  {m['chars']:>7}  {m['tag']:14} {m['title'][:50]}")
