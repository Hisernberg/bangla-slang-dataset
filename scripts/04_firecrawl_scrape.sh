#!/bin/bash
# Scrape remaining key URLs with Firecrawl v2
FC_KEY="${FIRECRAWL_API_KEY:?export FIRECRAWL_API_KEY first}"
RAW=/home/z/my-project/bangla-slang-dataset/data/raw/firecrawl
mkdir -p "$RAW"

scrape() {
  local url="$1"; local out="$2"
  local body=$(python3 -c "import json,sys; print(json.dumps({'url':sys.argv[1],'formats':['markdown']}))" "$url")
  curl -s -X POST https://api.firecrawl.dev/v2/scrape \
    -H "Authorization: Bearer $FC_KEY" -H "Content-Type: application/json" \
    -d "$body" -o "$RAW/scrape_$out.json"
  local size=$(stat -c%s "$RAW/scrape_$out.json" 2>/dev/null || echo 0)
  echo "scrape_$out: $size bytes"
}

scrape "https://www.dhakatribune.com/magazine-archive/weekend-tribune/7449/dhaka-dictionary" dhaka_tribune
scrape "https://www.thedailystar.net/slow-reads/unheard-voices/news/bazaira-vasha-dhakaiya-sobbasi-and-their-language-3907471" daily_star_bazaira
scrape "https://talkpal.ai/culture/what-is-the-vocabulary-for-internet-slang-in-bangladesh-versus-west-bengal" talkpal_internet
scrape "https://allzinone.blogspot.com/2014/12/list-of-175-abusive-language-bangla.html" blogspot_175_gali
scrape "https://en.wikipedia.org/wiki/Dhakaiya_Kutti_dialect" en_wiki_dhakaiya
scrape "https://www.languagetrainers.co.uk/blog/must-know-bengali-phrases-for-all-occasions/" languagetrainers
scrape "https://www.somewhereinblog.net/blog/icarusss/29879801" sib_slang_thread
scrape "https://daakbangla.com/topic/bengali-slangs/" daakbangla
scrape "https://www.omniglot.com/language/phrases/sylheti.htm" omniglot_sylheti
scrape "https://www.languageshome.com/English-Sylheti.htm" languageshome_sylheti
scrape "https://en.wikivoyage.org/wiki/Chittagonian_phrasebook" wikivoyage_chatgaiya
scrape "https://wikitravel.org/en/Chittagonian_phrasebook" wikitravel_chatgaiya
scrape "https://www.ajkerpatrika.com/bishesh/ajpky7vptcoxv" ajkerpatrika_dhakaiya
scrape "https://ypfbd.org/aro-bak-aro-bhasha-dhakaiya/" ypf_dhakaiya
scrape "https://quizlet.com/276968469/sylheti-terms-and-phrases-flash-cards/" quizlet_sylheti
