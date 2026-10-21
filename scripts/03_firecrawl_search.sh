#!/bin/bash
# Firecrawl search for Bangla slang sources
FC_KEY="${FIRECRAWL_API_KEY:?export FIRECRAWL_API_KEY first}"
mkdir -p /home/z/my-project/bangla-slang-dataset/data/raw/firecrawl

search() {
  local q="$1"; local out="$2"
  curl -s -X POST https://api.firecrawl.dev/v2/search \
    -H "Authorization: Bearer $FC_KEY" -H "Content-Type: application/json" \
    -d "{\"query\":\"$q\",\"limit\":8,\"scrapeOptions\":{\"formats\":[\"markdown\"]}}" \
    -o "/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl/search_$out.json"
  echo "search_$out: $(python3 -c "import json;d=json.load(open('/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl/search_$out.json'));print(d.get('success'), len(d.get('data',[])))" 2>/dev/null || echo FAIL)"
}

search "বাংলা স্ল্যাং শব্দের তালিকা অর্থসহ" bn_slang_list
search "ঢাকাইয়া ভাষার শব্দ তালিকা" dhakaiya
search "bangla slang words meaning list blog" en_slang
search "বাংলা ইন্টারনেট স্ল্যাং ফেসবুক" internet
search "বাংলা গালি কোটিন শব্দ" gali
search "sylheti dialect words kita slang" sylheti
search "chittagonian dialect words list slang" chittagong
search "banglish college campus slang bangladesh students" campus
