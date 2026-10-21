#!/usr/bin/env python3
"""Parse all scraped markdown/txt/csv/jsonl sources into candidate slang entries.
Sources: firecrawl md docs, blogspot175, Nirmol, deshi-slang, HF Chittagonian."""
import json, re, os, glob, unicodedata

BASE = "/home/z/my-project/bangla-slang-dataset/data/raw"
MD = BASE + "/firecrawl/md"
BN = re.compile(r'[\u0980-\u09FF]')
LAT = re.compile(r'[A-Za-z]')

STOP_BN = set("""কিন্তু আর তাই যে এই ওই কি কী কেন কিভাবে যখন তখন আমি আমার তুমি তোমার সে তার ওর
হ্যাঁ না এবং অথবা জন্য সাথে করে হয় হবে করা কারণ এমন সব অনেক মানুষ দিয়ে থেকে হচ্ছে
ছিল আছে ছাড়া মত রকম হল হলো করি করো করুন এখন তখন আজ কাল এক দুই তিন বহু যাও আসো
আসুন দেখুন পড়ুন লিখুন বলুন শুনুন জানি জানেন বুঝেছি বলছি মনে হয় মনে হচ্ছে তাহলে
তবে মাত্র প্রায় গুলো টা টি রা কে কার কোথায় কখন কীভাবে যদি নইলে যাতে হয়তো বুঝলা""".split())

EN_STOP = set("""the a an and or of to in is are was were be been being it its this that these those
i you he she we they me my your his her our their with for from at on by as not no yes
""".split())

NAV_WORDS = set("""লগইন রেজিস্ট্রেশন সকল পোস্ট নির্বাচিত নোটিশ আরও পড়ুন শেয়ার কমেন্ট
মেনু হোম খবর বিজ্ঞাপন অনুসন্ধান ডাউনলোড প্রচ্ছদ""".split())

def norm(s):
    return unicodedata.normalize('NFC', (s or '')).strip()

def bn_ratio(s):
    s = s or ''
    alpha = [c for c in s if c.isalpha()]
    if not alpha: return 0.0
    return sum(1 for c in alpha if '\u0980' <= c <= '\u09FF') / len(alpha)

def is_valid_term(t):
    t = (t or '').strip(' ।,;:!?-*•—–"\'`()[]{}')
    if len(t) < 2 or len(t) > 42: return None
    if bn_ratio(t) < 0.5: return None
    words = t.split()
    if len(words) > 6: return None
    if any(w in STOP_BN or w in NAV_WORDS for w in words): return None
    if re.search(r'https?://|www\.|@|#\w', t): return None
    # junk patterns: blog-comment artifacts, headers, spam phrases
    JUNK = ['বলেছেন', 'পর্ব ', '##', 'উচ্চ শব্দে', 'ক্যাশব্যাক', 'গ্যারান্টিড', 'ছাড় পাবেন', 'ফ্রি টাকা',
            'ল্যাপটপ পাবেন', 'বিকাশ', 'লোন নিন', 'এসএমস পাঠিয়ে', 'অফার', 'নাম্বার দিন', 'অ্যাকাউন্ট খোলান',
            'শব্দটি', 'ডায়লগ বাদ', 'জানতাম না', 'বলেছিলাম', 'লিখেছেন', 'বলছেন']
    if any(j in t for j in JUNK): return None
    if len(set(t.split())) < 1: return None
    return t

def is_valid_meaning(m):
    m = (m or '').strip(' ।,;:!?-*•—–"\'`()[]{}')
    if len(m) < 3 or len(m) > 300: return None
    if re.search(r'https?://|www\.', m): return None
    return m

# ------------- source priors -------------
PRIORS = [
    (r'dhakaiya|bazaira|ajkerpatrika|prothomalo|ypf|dhaka_tribune', 'regional_dhaka', 'Dhaka'),
    (r'chittagonian|chatgaiya|wikivoyage|wikitravel', 'regional_chattogram', 'Chattogram'),
    (r'sylheti|omniglot|languageshome|mylittlewordland|sylhetiproject|pmc', 'regional_sylhet', 'Sylhet'),
    (r'noakhali|chatkhil|dinajpur|ijcrt', 'colloquial_dialectal', 'Noakhali/Dinajpur'),
    (r'teachers_gov|blogspot|gali', 'profanity_curses', 'Bangladesh'),
    (r'talkpal|meme|punchforon', 'internet_social', 'Bangladesh (online)'),
    (r'movie|oneindia|indianexpress|giphy', 'entertainment_media', 'Bengali cinema'),
    (r'romance|love|sms|caption|gonevis|wishinall|bdlove', 'relationships_emotions', 'Bengal (popular)'),
    (r'political|anandabazar|tangleofwires|cpim|slogan', 'social_political', 'Bengal (politics)'),
    (r'campus|springer|ssrn|harvard|cornell', 'campus_student', 'Bangladesh (campus)'),
]
def prior_for(tag, url):
    s = (tag + ' ' + (url or '')).lower()
    for pat, cat, region in PRIORS:
        if re.search(pat, s):
            return cat, region
    return '', 'Bengal'

# ------------- pattern extractors -------------
def extract_tables(text, tag, url):
    out = []
    text = text.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    for line in text.split('\n'):
        if not line.strip().startswith('|') or line.strip().startswith('|--'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        cells = [re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', c) for c in cells]
        cells = [c.strip() for c in cells if c and not re.match(r'^[-: ]+$', c)]
        if len(cells) < 2:
            continue
        # find bengali-ish cells and english cells
        bn_cells = [c for c in cells if bn_ratio(c) > 0.5 and len(c) <= 60]
        en_cells = [c for c in cells if bn_ratio(c) < 0.3 and len(c) <= 200 and LAT.search(c)]
        if not bn_cells:
            continue
        term = is_valid_term(bn_cells[0])
        if not term:
            continue
        meaning_en = ''
        meaning_bn = ''
        if len(bn_cells) > 1:
            meaning_bn = is_valid_meaning(bn_cells[1]) or ''
        if en_cells:
            # pick the longest plausible english cell
            en_cells.sort(key=len, reverse=True)
            meaning_en = is_valid_meaning(en_cells[0]) or ''
        roman = ''
        for c in cells:
            m = re.match(r'^[A-Za-zāīūṭḍṅñṃśṣḥâîûéèô\- ]+$', c.strip())
            if m and 2 < len(c.strip()) < 50:
                roman = c.strip(); break
        out.append({'term_bn': term, 'romanization': roman, 'meaning_en': meaning_en,
                    'meaning_bn': meaning_bn, 'source_tag': tag, 'source_url': url})
    return out

def extract_dash(text, tag, url):
    out = []
    text = text.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    SEP = r'(?:\s+[—–−]\s*|\s+-\s+|\s*[::]\s+|\s+=\s+|\s+→\s+)'
    for raw in text.split('\n'):
        line = raw.strip()
        line = re.sub(r'^[-*•]\s+', '', line)
        line = re.sub(r'^(\d+|[০-৯]+)[.).।]\s*', '', line)
        line = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', line)
        if not BN.search(line) or 'http' in line:
            continue
        parts = re.split(SEP, line, maxsplit=1)
        if len(parts) != 2:
            continue
        term = is_valid_term(parts[0])
        meaning = is_valid_meaning(parts[1])
        if not term or not meaning:
            continue
        # romanization: latin words inside term side or right after
        roman = ''
        rm = re.search(r'\(([^)]*[A-Za-z][^)]*)\)', parts[0])
        if rm and bn_ratio(rm.group(1)) < 0.3:
            roman = rm.group(1).strip()
        out.append({'term_bn': term, 'romanization': roman,
                    'meaning_en': meaning if bn_ratio(meaning) < 0.4 else '',
                    'meaning_bn': meaning if bn_ratio(meaning) >= 0.4 else '',
                    'source_tag': tag, 'source_url': url})
    return out

def extract_lingapp(text, tag, url):
    out = []
    pat = re.compile(r'^#{2,4}\s*\d+\\?\.?\s*(.+?)\s*[–-]\s*([A-Za-z][^()]*?)\s*\(([^)]*[\u0980-\u09FF][^)]*)\)\s*$', re.M)
    for m in pat.finditer(text):
        en, roman, bn = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        term = is_valid_term(bn)
        if term:
            out.append({'term_bn': term, 'romanization': roman, 'meaning_en': en,
                        'meaning_bn': '', 'source_tag': tag, 'source_url': url})
    return out

def extract_numbered_bn(text, tag, url, category='', region='Bangladesh', offensiveness=3):
    out = []
    for raw in text.split('\n'):
        line = raw.strip()
        m = re.match(r'^(?:\d+|[০-৯]+)\s*[।.)]\s*(.+)$', line)
        if not m:
            continue
        term = is_valid_term(m.group(1))
        if not term:
            continue
        out.append({'term_bn': term, 'romanization': '', 'meaning_en': '',
                    'meaning_bn': '', 'source_tag': tag, 'source_url': url,
                    'category': category, 'region': region, 'offensiveness': offensiveness})
    return out

# ------------- run over md docs -------------
manifest = json.load(open(BASE + "/firecrawl/manifest.json", encoding="utf-8"))
cands = []
seen_files = set()
for m in manifest:
    f = m['file']
    if f in seen_files: continue
    seen_files.add(f)
    try:
        text = open(f, encoding='utf-8').read()
    except Exception:
        continue
    tag = m['tag']
    url = m['url']
    body = text.split('---\n\n', 1)[-1] if text.startswith('---') else text
    cat, region = prior_for(tag, url)
    got = []
    if 'ling-app' in f:
        got += extract_lingapp(body, tag, url)
    got += extract_tables(body, tag, url)
    got += extract_dash(body, tag, url)
    for g in got:
        g.setdefault('category', '')
        g.setdefault('region', '')
        if cat and not g['category']:
            g['category'], g['region'] = cat, region
        cands.append(g)

# ------------- dedicated txt/csv/jsonl sources -------------
# blogspot 175 gali (browser-rendered txt)
try:
    t = open(BASE + '/browser_blogspot_175gali.txt', encoding='utf-8').read()
    cands += extract_numbered_bn(t, 'blogspot175', 'https://allzinone.blogspot.com/2014/12/list-of-175-abusive-language-bangla.html',
                                 category='profanity_curses', region='Bangladesh', offensiveness=3)
except Exception as e:
    print('blogspot175 ERR', e)

# Nirmol (github) — profanity term list
nirmol = open(BASE + '/gh_nirmol_v1.csv', encoding='utf-8').read().split('\n')
for t in nirmol:
    t = t.strip()
    if not t: continue
    roman = t if bn_ratio(t) < 0.3 else ''
    cands.append({'term_bn': t, 'romanization': roman,
                  'meaning_en': 'severe Bangla profanity / insult (moderation lexicon term)' if not roman else 'severe Bangla profanity term (Roman-script variant in source)',
                  'meaning_bn': '', 'source_tag': 'nirmol_github',
                  'source_url': 'https://github.com/Sigmakib2/Nirmol',
                  'category': 'profanity_curses', 'region': 'Bangladesh', 'offensiveness': 3})

# deshi-slang jsonl — structured with romanization + severity
LAB2TAG = {'profanity': 'profanity', 'sexual_slang': 'vulgar', 'sexual': 'vulgar', 'abusive': 'abusive',
           'slur': 'slur', 'hate_speech': 'hate_speech', 'harassment': 'harassment', 'threat': 'threat',
           'slang': 'slang', 'neutral': 'colloquial', 'derogatory': 'derogatory', 'spam': ''}
try:
    for line in open(BASE + '/gh_deshi_slang.jsonl', encoding='utf-8'):
        line = line.strip()
        if not line: continue
        d = json.loads(line)
        labels_raw = d.get('labels', [])
        if 'spam' in labels_raw or d.get('is_obfuscated'):
            continue  # skip spam and obfuscated duplicates
        term = is_valid_term(d.get('text', ''))
        if not term: continue
        labels = [LAB2TAG.get(l, l) for l in d.get('labels', []) if LAB2TAG.get(l, l)]
        sev = int(d.get('severity_score', 0) or 0)
        cat = 'profanity_curses' if sev >= 2 else ('internet_social' if 'slang' in labels else '')
        if not cat: cat = 'profanity_curses' if labels else ''
        cands.append({'term_bn': term, 'romanization': d.get('romanized', ''),
                      'meaning_en': '', 'meaning_bn': '',
                      'source_tag': 'deshi_slang_github', 'source_url': 'https://github.com/amirulsizan/deshi-slang',
                      'category': cat, 'region': 'Bangladesh', 'offensiveness': sev,
                      'tags': labels})
except Exception as e:
    print('deshi ERR', e)

# HF Chittagonian vulgar lexicon
try:
    for line in open(BASE + '/hf_chittagong_vulgar_TanjimKIT.csv', encoding='utf-8').read().split('\n')[1:]:
        t = line.strip().lstrip('\ufeff')
        if not t: continue
        term = is_valid_term(t)
        if not term: continue
        cands.append({'term_bn': term, 'romanization': '',
                      'meaning_en': '', 'meaning_bn': '',
                      'source_tag': 'hf_chittagong_vulgar', 'source_url': 'https://huggingface.co/datasets/TanjimKIT/Vulgar_Lexicon_of_Chittagonian_Dialect_of_Bangla_or_Bengali',
                      'category': 'regional_chattogram', 'region': 'Chattogram',
                      'offensiveness': 2 if bn_ratio(term) > 0.5 else 3, 'tags': ['vulgar', 'dialectal']})
except Exception as e:
    print('hf ERR', e)

json.dump(cands, open(BASE + '/parsed_sources.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(f"total candidates: {len(cands)}")
print("by source_tag:", Counter(c['source_tag'] for c in cands).most_common(20))
print("by category:", Counter(c.get('category','') for c in cands).most_common())
