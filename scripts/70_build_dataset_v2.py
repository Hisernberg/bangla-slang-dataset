#!/usr/bin/env python3
"""Build v2: existing master (2100) + gold v2 (601) + kuntalojha + HF dialect words + wt2 + firecrawl candidates.
16-category taxonomy, stable IDs, popularity column, by-category files, stats."""
import json, re, csv, os, unicodedata, sys
from collections import Counter, defaultdict

BASE = "/home/z/my-project/bangla-slang-dataset"
RAW = BASE + "/data/raw"
FINAL = BASE + "/data/final"
os.makedirs(FINAL + "/by_category", exist_ok=True)
os.makedirs(BASE + "/data/candidates", exist_ok=True)

CONS = {'ক':'k','খ':'kh','গ':'g','ঘ':'gh','ঙ':'ng','চ':'ch','ছ':'chh','জ':'j','ঝ':'jh','ট':'t','ঠ':'th',
        'ড':'d','ঢ':'dh','ণ':'n','ত':'t','থ':'th','দ':'d','ধ':'dh','ন':'n','প':'p','ফ':'ph','ব':'b','ভ':'bh',
        'ম':'m','য':'j','র':'r','ল':'l','শ':'sh','ষ':'sh','স':'s','হ':'h','ড়':'r','ঢ়':'rh','য়':'y','ৎ':'t','ঁ':'n','ং':'ng','ঃ':'h'}
INDEP = {'অ':'o','আ':'a','ই':'i','ঈ':'i','উ':'u','ঊ':'u','ঋ':'ri','এ':'e','ঐ':'oi','ও':'o','ঔ':'ou'}
MATRA = {'া':'a','ি':'i','ী':'i','ু':'u','ূ':'u','ৃ':'ri','ে':'e','ৈ':'oi','ো':'o','ৌ':'ou','্য':'ya'}

def translit(s):
    out, i, s = [], 0, (s or '').strip()
    while i < len(s):
        c = s[i]
        if s[i:i+2] == 'ক্ষ': out.append('kkh'); i += 2; continue
        if s[i:i+2] == 'জ্ঞ': out.append('gg'); i += 2; continue
        if c == '্': i += 1; continue
        if c in CONS:
            out.append(CONS[c]); i += 1
            if i < len(s) and s[i] == '়': i += 1
            continue
        if c in INDEP: out.append(INDEP[c]); i += 1; continue
        if c in MATRA: out.append(MATRA[c]); i += 1; continue
        if c in '।,;:!?-–—()[]{}"\' ': out.append(' ' if c in '।,;:!?-–—()[]{}"\'' else ''); i += 1; continue
        if c.isascii(): out.append(c); i += 1; continue
        i += 1
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

def norm_term(t):
    t = unicodedata.normalize('NFC', (t or '')).strip()
    t = re.sub(r'[।,;:!?\-–—_()\.]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

CATS = ['regional_dhaka','regional_chattogram','regional_sylhet','colloquial_dialectal','profanity_curses',
        'internet_social','campus_student','entertainment_media','relationships_emotions','social_political',
        'banglish_codemixed','exclamations_interjections','old_school_retro','street_transport_market',
        'cricket_sports_gaming','idioms_figurative']
OLD_REGION_MAP = {'regional_dhaka':'Dhaka','regional_chattogram':'Chattogram','regional_sylhet':'Sylhet','colloquial_dialectal':'Bengal'}

FIELDS = ['id','term_bn','romanization','literal_meaning','meaning_en','meaning_bn','category','region',
          'part_of_speech','register','offensiveness','usage_example_bn','usage_example_en','era','tags',
          'popularity','confidence','tier','source_type','source_url']

# ---------------- load existing master ----------------
master = json.load(open(FINAL + '/bangla_slang_master.json'))
print("existing master:", len(master))
KEY = {}
for e in master:
    e['popularity'] = e.get('popularity') or ''
    KEY[norm_term(e['term_bn']).lower()] = e
    k2 = re.sub(r'[^a-z]', '', translit(e['term_bn']).lower().replace(' ', ''))
    if k2 and k2 not in KEY:
        KEY[k2] = e
used_keys = set()
for e in master:
    used_keys.add(norm_term(e['term_bn']).lower())

new_entries = []
def add_new(e):
    new_entries.append(e)

# ---------------- gold v2 ----------------
gold = json.load(open(RAW + '/parse_v2_gold.json'))
g_enriched = 0
for g in gold:
    e = {'term_bn': g['term_bn'].strip(), 'romanization': g.get('romanization',''),
         'literal_meaning': g.get('literal_meaning',''), 'meaning_en': g.get('meaning_en',''),
         'meaning_bn': g.get('meaning_bn',''), 'category': g['category'], 'region': g['region'],
         'part_of_speech': g.get('part_of_speech',''), 'register': g.get('register',''),
         'offensiveness': int(g.get('offensiveness',0) or 0),
         'usage_example_bn': g.get('usage_example_bn',''), 'usage_example_en': g.get('usage_example_en',''),
         'era': g.get('era','modern'), 'tags': [t for t in (g.get('tags','') or '').split('|') if t],
         'popularity': g.get('popularity',''), 'confidence': 'high', 'tier': 1,
         'source_type': 'gold_curated_v2', 'source_url': 'curated by dataset maintainers'}
    k = norm_term(e['term_bn']).lower()
    old = KEY.get(k)
    if old:  # enrich existing
        for f in ['meaning_en','meaning_bn','usage_example_bn','usage_example_en','literal_meaning','era','part_of_speech','popularity']:
            if not old.get(f) and e.get(f):
                old[f] = e[f]
        if old.get('offensiveness') in (None, 0) and e['offensiveness']:
            old['offensiveness'] = e['offensiveness']
        if not old.get('romanization'):
            old['romanization'] = e['romanization']
        g_enriched += 1
        for t in e['tags']:
            if t not in old['tags']:
                old['tags'].append(t)
        old['tags'].append('also:gold_v2')
    else:
        if k in used_keys:
            continue
        used_keys.add(k)
        add_new(e)
print(f"gold v2: {len(gold)} raw, enriched {g_enriched}, new {len(new_entries)}")
n_before = len(new_entries)

# ---------------- kuntalojha (MIT, tier3) ----------------
KW = [('profanity_curses', r'গালি|গাঁজা|খাঙ্কি|বোড়া|চুদ|বাঁদ|হালা|কুত্ত|শুয়োর|বাজারু|ধোঁকা|বোকা|গাধা|ছাগল|নালায়েক|বদমাশ|পাগল|খাঙ্গ|কুলাং|ভাঁড়|চ্যাংড়া|কেলাস|পদ্দা|ধাপ্পাবাজ'),
      ('exclamations_interjections', r'ধুর|বাহ|ইস|আরে|উফ|ব্যাস|হুম|হুঁ|আচ্ছা|থাক'),
      ('banglish_codemixed', r'[A-Za-z]'),
      ('relationships_emotions', r'ভালোবাসা|প্রেম|মন|রাগ|মান')]
def classify_kw(term, mean=''):
    text = term + ' ' + (mean or '')
    for cat, pat in KW:
        if re.search(pat, text):
            return cat
    return 'colloquial_dialectal'

kt = json.load(open(RAW + '/parse_v2_gh_kuntalojha.json'))
kt_added = 0
for d in kt:
    k = norm_term(d['term_bn']).lower()
    if k in used_keys or not (2 <= len(d['term_bn']) <= 30):
        continue
    used_keys.add(k)
    cat = classify_kw(d['term_bn'])
    off = 2 if cat == 'profanity_curses' else 1
    e = {'term_bn': d['term_bn'], 'romanization': '', 'literal_meaning': '', 'meaning_en': '',
         'meaning_bn': '', 'category': cat, 'region': 'Bengal', 'part_of_speech': '', 'register': '',
         'offensiveness': off, 'usage_example_bn': '', 'usage_example_en': '', 'era': '',
         'tags': d.get('tags', []) + ['attribution:MIT'], 'popularity': '',
         'confidence': 'medium', 'tier': 3, 'source_type': d['source_type'], 'source_url': d['source_url']}
    add_new(e); kt_added += 1
print(f"kuntalojha new: {kt_added}")

# ---------------- HF dialect-normalization (Apache-2.0): mine dialect words ----------------
hf = json.load(open(RAW + '/parse_v2_hf_dialect.json'))
def toks(s):
    return set(re.findall(r'[\u0980-\u09FF]+', s or ''))
hf_counter = {}
for d in hf:
    dt, st = toks(d['term_bn']), toks(d.get('standard_bn', ''))
    diff = dt - st
    for w in diff:
        if 2 <= len(w) <= 22 and w not in used_keys:
            hf_counter.setdefault(w, {'count': 0, 'region': d.get('region', ''), 'example': d['term_bn'],
                                      'standard': d.get('standard_bn', ''), 'meaning_en': d.get('meaning_en', '')})
            hf_counter[w]['count'] += 1
hf_added = 0
for w, v in sorted(hf_counter.items(), key=lambda x: -x[1]['count']):
    if v['count'] < 2:  # require recurrence
        continue
    if w in used_keys:
        continue
    used_keys.add(w)
    reg = v['region'] or 'Bengal'
    e = {'term_bn': w, 'romanization': '', 'literal_meaning': '', 'meaning_en': v['meaning_en'],
         'meaning_bn': '', 'category': 'colloquial_dialectal', 'region': reg,
         'part_of_speech': '', 'register': 'dialect', 'offensiveness': 0,
         'usage_example_bn': v['example'], 'usage_example_en': '', 'era': '',
         'tags': ['dialect', 'attribution:Apache-2.0', 'sent_pair'], 'popularity': '',
         'confidence': 'medium', 'tier': 3, 'source_type': 'hf_dialect_norm_apache2',
         'source_url': 'https://huggingface.co/datasets/zmsali/bangla-dialect-normalization (Apache-2.0)'}
    add_new(e); hf_added += 1
print(f"hf dialect words new: {hf_added}")

# ---------------- wt2 (if present) ----------------
if os.path.exists(RAW + '/parse_v2_wt2.json'):
    wt2 = json.load(open(RAW + '/parse_v2_wt2.json'))
    wt_added = 0
    for d in wt2:
        k = norm_term(d['term_bn']).lower()
        if k in used_keys or not (2 <= len(d['term_bn']) <= 40):
            continue
        used_keys.add(k)
        tags = d.get('tags', [])
        off = 3 if any(t in tags for t in ('vulgar', 'offensive', 'slur')) else (1 if 'slang' in tags else 0)
        cat = 'colloquial_dialectal'
        if 'Sylheti' in d['source_url']:
            cat, reg = 'regional_sylhet', 'Sylhet'
        elif 'Chittagonian' in d['source_url']:
            cat, reg = 'regional_chattogram', 'Chattogram'
        else:
            reg = 'Bengal'
        if off >= 2:
            cat = 'profanity_curses'
        e = {'term_bn': d['term_bn'], 'romanization': '', 'literal_meaning': '', 'meaning_en': d.get('meaning_en', ''),
             'meaning_bn': '', 'category': cat, 'region': reg, 'part_of_speech': d.get('part_of_speech', ''),
             'register': '', 'offensiveness': off, 'usage_example_bn': d.get('usage_example_bn', ''),
             'usage_example_en': d.get('usage_example_en', ''), 'era': '', 'tags': tags,
             'popularity': '', 'confidence': 'medium', 'tier': 2, 'source_type': d['source_type'],
             'source_url': d['source_url']}
        add_new(e); wt_added += 1
    print(f"wt2 new: {wt_added}")

# ---------------- finalize new entries ----------------
for e in new_entries:
    if not e['romanization'] and re.search(r'[\u0980-\u09FF]', e['term_bn']):
        e['romanization'] = translit(e['term_bn'])
    if not e['register']:
        e['register'] = 'vulgar' if (e['offensiveness'] or 0) >= 3 else ('street' if (e['offensiveness'] or 0) == 2 else 'informal')
    if not e['era']:
        e['era'] = ''
    if e['popularity'] == '':
        e['popularity'] = ''
    if not e['region']:
        e['region'] = OLD_REGION_MAP.get(e['category'], 'Bengal')
    if e['offensiveness'] is None:
        e['offensiveness'] = 3 if e['category'] == 'profanity_curses' else 0

master += new_entries

# translit-fuzzy dedupe on the FULL set (old master already deduped; check new vs old by translit)
seen_t = {}
final = []
for e in master:
    k1 = norm_term(e['term_bn']).lower()
    k2 = re.sub(r'[^a-z]', '', translit(e['term_bn']).lower().replace(' ', ''))
    dup = False
    for k in (k1, k2):
        if k and k in seen_t:
            old = seen_t[k]
            for f in ['meaning_en', 'meaning_bn', 'usage_example_bn', 'usage_example_en']:
                if not old.get(f) and e.get(f):
                    old[f] = e[f]
            dup = True
            break
    if not dup:
        if k1: seen_t[k1] = e
        if k2: seen_t.setdefault(k2, e)
        final.append(e)

# unknown categories -> fix or drop
for e in final:
    if e['category'] not in CATS:
        t = ' '.join(e.get('tags', []))
        if any(x in t for x in ('vulgar', 'offensive', 'profanity')):
            e['category'] = 'profanity_curses'
        elif 'dialect' in t:
            e['category'] = 'colloquial_dialectal'
        else:
            e['category'] = 'colloquial_dialectal'
final.sort(key=lambda e: (CATS.index(e['category']), e['tier'], e['term_bn']))
for i, e in enumerate(final, 1):
    e['id'] = f"KS-{i:04d}"

# ---------------- candidates v2 (banglawordkit + firecrawl) ----------------
cand_old = json.load(open(BASE + '/data/candidates/web_candidates_for_annotation.json')) if os.path.exists(BASE + '/data/candidates/web_candidates_for_annotation.json') else []
cand_bw = json.load(open(RAW + '/parse_v2_gh_banglawordkit.json'))
cand_fc = json.load(open(RAW + '/parse_v2_fc.json'))
JUNKM = re.compile(r'(Source|ছবি|Source:)', re.I)
master_keys = set(norm_term(e['term_bn']).lower() for e in final)
cand_new = []
seen_ck = set(norm_term(c['term_bn']).lower() for c in cand_old)
for c in cand_bw + cand_fc:
    t = (c.get('term_bn') or '').strip()
    if not t or len(t) < 2 or len(t) > 60:
        continue
    if JUNKM.search(t) or t.endswith('Source'):
        continue
    k = norm_term(t).lower()
    if k in master_keys or k in seen_ck:
        continue
    seen_ck.add(k)
    cand_new.append({'term_bn': t, 'meaning_en': c.get('meaning_en', ''), 'meaning_bn': c.get('meaning_bn', ''),
                     'source_type': c.get('source_type', ''), 'source_url': c.get('source_url', ''),
                     'tier': 4, 'tags': c.get('tags', [])})
candidates = cand_old + cand_new

# ---------------- write outputs ----------------
def write_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({**r, 'tags': '|'.join(r.get('tags', []))})

write_csv(FINAL + '/bangla_slang_master.csv', final)
json.dump(final, open(FINAL + '/bangla_slang_master.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
write_csv(BASE + '/data/candidates/web_candidates_for_annotation.csv', candidates)
json.dump(candidates, open(BASE + '/data/candidates/web_candidates_for_annotation.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

by_cat = defaultdict(list)
for e in final:
    by_cat[e['category'] or 'unclassified'].append(e)
for cat, rows in by_cat.items():
    write_csv(FINAL + f'/by_category/{cat}.csv', rows)
# clean stale category files
for f in os.listdir(FINAL + '/by_category'):
    if f[:-4] not in by_cat and f.endswith('.csv'):
        os.remove(FINAL + '/by_category/' + f)

by_region = defaultdict(list)
for e in final:
    by_region[e.get('region', 'Bengal')].append(e)
stats = {'total': len(final),
         'by_category': {c: len(v) for c, v in sorted(by_cat.items())},
         'by_tier': dict(Counter(e['tier'] for e in final)),
         'by_source_type': dict(Counter(e['source_type'] for e in final)),
         'by_region': {r: len(v) for r, v in sorted(by_region.items(), key=lambda x: -len(x[1]))[:12]},
         'tier4_candidates': len(candidates),
         'with_meaning_en': sum(1 for e in final if e['meaning_en']),
         'with_meaning_bn': sum(1 for e in final if e['meaning_bn']),
         'with_romanization': sum(1 for e in final if e['romanization']),
         'with_example': sum(1 for e in final if e['usage_example_bn'] or e['usage_example_en']),
         'with_popularity': sum(1 for e in final if e.get('popularity') not in ('', None))}
json.dump(stats, open(FINAL + '/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1, ensure_ascii=False))
