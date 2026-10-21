#!/bin/bash
# Round 2 firecrawl searches: entertainment, relationships, political slang
FC_KEY="${FIRECRAWL_API_KEY:?export FIRECRAWL_API_KEY first}"
RAW=/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl

search() {
  local q="$1"; local out="$2"
  local body=$(python3 -c "import json,sys; print(json.dumps({'query':sys.argv[1],'limit':8,'scrapeOptions':{'formats':['markdown']}}))" "$q")
  curl -s -X POST https://api.firecrawl.dev/v2/search \
    -H "Authorization: Bearer $FC_KEY" -H "Content-Type: application/json" \
    -d "$body" -o "$RAW/search_$out.json"
  local n=$(python3 -c "import json;d=json.load(open('$RAW/search_$out.json'));print(len(d.get('data',{}).get('web',[])))" 2>/dev/null || echo FAIL)
  echo "search_$out: $n results"
}

search "বাংলা সিনেমার বিখ্যাত সংলাপ মিম ক্যান মামা লাগব" entertainment
search "bangla movie famous dialogue meme list" movie_dialog
search "বাংলা রাজনৈতিক শব্দ চামচা হাওয়া মামা স্ল্যাং" political
search "bangladeshi political slang words hawa chamcha" political_en
search "বাংলা প্রেম ভালোবাসা স্ল্যাং শব্দ তরুণ" romance
search "ফেসবুক মিম শব্দ ভাইরাল বাংলা তালিকা" meme_bn
search "dhaka street slang words mama bap faltu meaning" street
search "bangla gali list blogspot গালির তালিকা" gali2
search "noakhali barishal rangpur dialect slang words list" regional2
search "bangla university slang supply refer back paper" campus2
