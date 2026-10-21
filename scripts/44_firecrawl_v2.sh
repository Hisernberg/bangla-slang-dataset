#!/bin/bash
# v2 Firecrawl harvest: 24 searches w/ inline markdown scrape, then targeted scrapes.
FC_KEY="${FIRECRAWL_KEY:-}"
OUT="/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl2"
mkdir -p "$OUT/pages"
QUERIES=(
 "bangla slang words list meaning"
 "banglish words list bengali english mixed"
 "dhakaiya slang words list"
 "chittagonian dialect words list meaning"
 "sylheti dialect words list meaning"
 "noakhali dialect words list"
 "bangla gali list meaning english"
 "bangla gen z slang words"
 "bangla facebook status slang words"
 "university slang bangladesh varsity words"
 "bangla cricket slang words"
 "rickshaw bus slang bangla street language"
 "old dhaka language words puran dhaka bhasha"
 "bangla meme words 2024"
 "bangla swearing words english translation list"
 "বাংলা স্ল্যাং শব্দের তালিকা"
 "বাংলা গালি শব্দ"
 "ঢাকাইয়া কুট্টি ভাষার শব্দ"
 "বাংলা বাগধারা তালিকা অর্থ"
 "চটগাঁইয়া ভাষার শব্দ"
 "সিলেটি ভাষার শব্দ তালিকা"
 "bangla slang dictionary online"
 "bangla abusive language dataset github"
 "bengali slang quiz meaning"
)
i=0
for Q in "${QUERIES[@]}"; do
  i=$((i+1))
  BODY=$(python3 - "$Q" <<'EOF'
import json,sys
q=sys.argv[1]
print(json.dumps({"query":q,"limit":5,"scrapeOptions":{"formats":["markdown"],"onlyMainContent":True}}))
EOF
)
  RES=$(curl -s --max-time 90 -X POST https://api.firecrawl.dev/v1/search \
    -H "Authorization: Bearer $FC_KEY" -H "Content-Type: application/json" -d "$BODY")
  echo "$RES" > "$OUT/search_$i.json"
  echo "[$i] $Q -> $(echo "$RES" | python3 -c 'import json,sys
try:
 d=json.load(sys.stdin); print(len(d.get("data",[])),"results")
except: print("parse-err")')"
  python3 - "$i" "$OUT" <<'EOF'
import json,sys,re,os
i,out=sys.argv[1],sys.argv[2]
try:
    d=json.load(open(f"{out}/search_{i}.json"))
except Exception:
    sys.exit()
for j,r in enumerate(d.get("data",[]) or []):
    md=(r.get("markdown") or "")
    url=r.get("metadata",{}).get("sourceURL") or r.get("url","")
    if len(md)>400:
        safe=re.sub(r'[^a-zA-Z0-9]+','_',url[:80])
        open(f"{out}/pages/q{i}_{j}_{safe}.md","w").write(f"---\nurl: {url}\nquery_index: {i}\n---\n\n{md}")
EOF
  sleep 2
done
echo "FIRECRAWL2 DONE"
