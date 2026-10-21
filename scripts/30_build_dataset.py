#!/usr/bin/env python3
"""Final dataset build: merge gold + wiktionary + structured + generic sources.
Dedupe by normalized term, priority-merge fields, transliterate, tier, output CSV/JSON."""
import json, re, csv, os, unicodedata
from collections import Counter, defaultdict

BASE = "/home/z/my-project/bangla-slang-dataset"
RAW = BASE + "/data/raw"
FINAL = BASE + "/data/final"
os.makedirs(FINAL + "/by_category", exist_ok=True)

# ---------------- transliteration ----------------
CONS = {'ক':'k','খ':'kh','গ':'g','ঘ':'gh','ঙ':'ng','চ':'ch','ছ':'chh','জ':'j','ঝ':'jh','ট':'t','ঠ':'th',
        'ড':'d','ঢ':'dh','ণ':'n','ত':'t','থ':'th','দ':'d','ধ':'dh','ন':'n','প':'p','ফ':'ph','ব':'b','ভ':'bh',
        'ম':'m','য':'j','র':'r','ল':'l','শ':'sh','ষ':'sh','স':'s','হ':'h','ড়':'r','ঢ়':'rh','য়':'y','ৎ':'t',
        '઼':'','ঁ':'n','ং':'ng','ঃ':'h','য়':'y'}
INDEP = {'অ':'o','আ':'a','ই':'i','ঈ':'i','উ':'u','ঊ':'u','ঋ':'ri','এ':'e','ঐ':'oi','ও':'o','ঔ':'ou','অ্যা':'a'}
MATRA = {'া':'a','ি':'i','ী':'i','ু':'u','ূ':'u','ৃ':'ri','ে':'e','ৈ':'oi','ো':'o','ৌ':'ou','্য':'ya'}

def translit(s):
    out = []
    i = 0
    s = s.strip()
    while i < len(s):
        c = s[i]
        two = s[i:i+2]
        if two in ('ক্ষ',):
            out.append('kkh'); i += 2; continue
        if two in ('জ্ঞ',):
            out.append('gg'); i += 2; continue
        if c == '্':  # hasanta — conjunct, drop
            i += 1; continue
        if c in CONS:
            out.append(CONS[c]); i += 1
            if i < len(s) and s[i] == '়':
                i += 1
            continue
        if c in INDEP:
            out.append(INDEP[c]); i += 1; continue
        if c in MATRA:
            out.append(MATRA[c]); i += 1; continue
        if c in '।,;:!?-–—()[]{}"\' ':
            out.append(' ' if c in '।,;:!?-–—()[]{}"\'' else '')
            i += 1; continue
        if c.isascii():
            out.append(c); i += 1; continue
        i += 1
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

def norm_term(t):
    t = unicodedata.normalize('NFC', (t or '')).strip()
    t = re.sub(r'[।,;:!?\-–—_()\.]+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

# ---------------- load sources ----------------
gold = json.load(open(RAW + '/gold_part1.json')) + json.load(open(RAW + '/gold_part2.json'))
wt_en = json.load(open(RAW + '/parsed_wiktionary_en.json'))
wt_bn = json.load(open(RAW + '/parsed_wiktionary_bn.json'))
src = json.load(open(RAW + '/parsed_sources.json'))

def tag_of(w):
    return ' '.join(w.get('tags', []))

# keyword classifier for entries with no category
KW = [
    ('profanity_curses', r'\b(whore|prostitute|bitch|slut|fuck|fucker|bastard|insult|curse|vulgar|obscene|idiot|stupid|fool|harlot)\b'),
    ('regional_chattogram', r'chittagon|chatgaiy'),
    ('regional_sylhet', r'sylhet'),
    ('regional_dhaka', r'dhaka'),
    ('colloquial_dialectal', r'noakhali|dinajpur|barishal|rangpur|khulna|mymensingh|dialect|colloquial'),
    ('internet_social', r'internet|social media|online|meme|facebook'),
    ('relationships_emotions', r'\b(love|romance|crush|heart|affection|emotion|sad)\b'),
    ('social_political', r'politic|party|protest|movement|election'),
    ('campus_student', r'student|campus|exam|college|university'),
    ('entertainment_media', r'film|cinema|movie|drama|actor'),
]
def classify(e):
    text = (e.get('meaning_en','') + ' ' + e.get('meaning_bn','') + ' ' + tag_of(e)).lower()
    for cat, pat in KW:
        if re.search(pat, text):
            return cat
    return ''

# ---------------- normalize to entry schema ----------------
def base_entry(term):
    return {'term_bn': term, 'romanization': '', 'literal_meaning': '', 'meaning_en': '',
            'meaning_bn': '', 'category': '', 'region': '', 'part_of_speech': '',
            'register': '', 'offensiveness': None, 'usage_example_bn': '', 'usage_example_en': '',
            'era': '', 'tags': [], 'confidence': '', 'tier': 0, 'source_type': '', 'source_url': ''}

POOLED = []  # (priority, entry)
# priority: lower = stronger
for i, g in enumerate(gold):
    e = base_entry(g['term_bn'])
    e.update({k: g.get(k, '') for k in ['term_bn','romanization','literal_meaning','meaning_en','meaning_bn','category','region','part_of_speech','register','usage_example_bn','usage_example_en','era']})
    e['offensiveness'] = int(g.get('offensiveness', 0) or 0)
    e['tags'] = [t for t in (g.get('tags','') or '').split('|') if t]
    e.update(confidence='high', tier=1, source_type='gold_curated', source_url='curated by dataset maintainers')
    POOLED.append((0, e))

LAB2TAG = {'profanity':'profanity','sexual_slang':'vulgar','abusive':'abusive','slur':'slur','hate_speech':'hate_speech','harassment':'harassment','threat':'threat','slang':'slang','neutral':'colloquial','derogatory':'derogatory','spam':''}
for d in src:
    e = base_entry(d['term_bn'])
    e['romanization'] = d.get('romanization','')
    e['meaning_en'] = d.get('meaning_en','')
    e['meaning_bn'] = d.get('meaning_bn','')
    e['category'] = d.get('category','') or ''
    e['region'] = d.get('region','')
    e['offensiveness'] = d.get('offensiveness') if d.get('offensiveness') is not None else None
    e['tags'] = d.get('tags', [])
    st = d['source_tag']
    if st in ('nirmol_github','deshi_slang_github','hf_chittagong_vulgar'):
        prio, tier, conf = 10, 3, 'medium'
        e['source_type'] = st
    elif st in ('blogspot175','gali','gali2'):
        prio, tier, conf = 11, 3, 'medium'
        e['source_type'] = 'web_lexicon_list'
    else:
        prio, tier, conf = 20, 4, 'low'
        e['source_type'] = 'web_auto_extract'
    e.update(confidence=conf, tier=tier, source_url=d.get('source_url',''))
    POOLED.append((prio, e))

for d in wt_en:
    e = base_entry(d['term_bn'])
    e['meaning_en'] = d.get('meaning_en','')
    e['part_of_speech'] = d.get('part_of_speech') or ''
    e['tags'] = d.get('tags', [])
    e['category'] = d.get('category','')
    e['region'] = d.get('region','')
    off = 3 if ('vulgar' in e['tags'] or 'offensive' in e['tags'] or 'slur' in e['tags']) else (1 if 'slang' in e['tags'] else 0)
    e['offensiveness'] = off
    e.update(confidence='medium', tier=2, source_type='wiktionary_en', source_url=d['source_url'])
    POOLED.append((5, e))

for d in wt_bn:
    e = base_entry(d['term_bn'])
    e['meaning_bn'] = d.get('meaning_bn','')
    e['usage_example_bn'] = d.get('usage_example_bn','')
    e['part_of_speech'] = d.get('part_of_speech') or ''
    e['tags'] = d.get('tags', [])
    e['category'] = d.get('category','')
    e['region'] = d.get('region','')
    e.update(confidence='medium', tier=2, source_type='wiktionary_bn', source_url=d['source_url'])
    POOLED.append((4, e))

# ---------------- merge by normalized term ----------------
KEY2ENTRY = {}
for prio, e in POOLED:
    key = norm_term(e['term_bn']).lower()
    if not key:
        continue
    if key not in KEY2ENTRY:
        KEY2ENTRY[key] = e
        continue
    cur = KEY2ENTRY[key]
    # fill missing fields from lower-priority
    for f in ['romanization','literal_meaning','meaning_en','meaning_bn','usage_example_bn','usage_example_en','part_of_speech','register','era']:
        if not cur.get(f) and e.get(f):
            cur[f] = e[f]
    if cur.get('offensiveness') in (None, 0) and e.get('offensiveness') not in (None,):
        cur['offensiveness'] = e['offensiveness']
    newcats = set(filter(None, [cur.get('category','')])) | set(filter(None, [e.get('category','')]))
    if len(newcats) == 1:
        cur['category'] = newcats.pop()
    for t in e.get('tags', []):
        if t not in cur['tags']:
            cur['tags'].append(t)
    if e.get('source_url') and e['source_url'] != cur.get('source_url'):
        cur['tags'].append('also:' + e.get('source_type',''))

entries = list(KEY2ENTRY.values())

# ---------------- final fixes ----------------
for e in entries:
    if not e['category']:
        e['category'] = classify(e)
    # tag-based final fallbacks
    if not e['category']:
        tagstr = ' '.join(e.get('tags', []))
        if any(t in tagstr for t in ('vulgar','offensive','crude','derogatory','slur','rude','abusive','profanity')):
            e['category'] = 'profanity_curses'
        elif any(t in tagstr for t in ('slang','informal','colloquial','pejorative','humorous','euphemism','dialectal','obsolete','archaic')):
            e['category'] = 'colloquial_dialectal'
    # auto-extracted entries that could not be categorized are noise -> drop
    if e['tier'] == 4 and not e['category']:
        e['term_bn'] = ''
    # tier-4 junk patterns: image-caption "Source" artifacts, ad copy
    if e['tier'] == 4:
        t = e.get('term_bn', '')
        m_en, m_bn = e.get('meaning_en',''), e.get('meaning_bn','')
        if (';' in t or t.endswith('Source') or t.endswith('ছবি') or 'রথ; Source' in t
                or m_en in ('BBC','Facebook','YouTube','Instagram','Google','Wikipedia')
                or m_bn.endswith('করুন') or m_bn.endswith('করুন।')):
            e['term_bn'] = ''
    if e['offensiveness'] is None:
        e['offensiveness'] = 3 if e['category'] == 'profanity_curses' else 0
    if not e['romanization'] and re.search(r'[\u0980-\u09FF]', e['term_bn']):
        e['romanization'] = translit(e['term_bn'])
    if not e['register']:
        e['register'] = 'vulgar' if e['offensiveness'] >= 3 else ('street' if e['offensiveness'] == 2 else 'informal')
    if not e['region']:
        e['region'] = {'regional_dhaka':'Dhaka','regional_chattogram':'Chattogram','regional_sylhet':'Sylhet','colloquial_dialectal':'Bengal'}.get(e['category'], 'Bengal')
    if e['tier'] >= 4 and e['category'] == 'profanity_curses' and not (e['meaning_en'] or e['meaning_bn']):
        e['meaning_en'] = e['meaning_en'] or 'profanity term harvested from community lexicon list'
    e['term_bn'] = e['term_bn'].strip()
    # drop empties
    if not re.search(r'[\u0980-\u09FF\w]', e['term_bn']):
        e['term_bn'] = ''

entries = [e for e in entries if e['term_bn'] and len(e['term_bn']) >= 2]
# dedupe Latin-script Nirmol variants vs Bengali same term handled by translit key fallback
seen = {}
final = []
for e in entries:
    k1 = norm_term(e['term_bn']).lower()
    k2 = translit(e['term_bn']).lower().replace(' ', '')
    k2 = re.sub(r'[^a-z]', '', k2)
    dup = False
    for k in (k1, k2):
        if k and k in seen:
            # merge meaning if present
            old = seen[k]
            if (not old['meaning_en']) and e['meaning_en']:
                old['meaning_en'] = e['meaning_en']
            dup = True
            break
    if not dup:
        if k1: seen[k1] = e
        if k2: seen.setdefault(k2, e)
        final.append(e)

# sort: category order, then tier, then term
CAT_ORDER = ['regional_dhaka','regional_chattogram','regional_sylhet','colloquial_dialectal','profanity_curses',
             'internet_social','campus_student','entertainment_media','relationships_emotions','social_political']
final.sort(key=lambda e: (CAT_ORDER.index(e['category']) if e['category'] in CAT_ORDER else 99, e['tier'], e['term_bn']))

os.makedirs(BASE + '/data/candidates', exist_ok=True)
# split: verified master (tier 1-3) vs auto-extracted candidates (tier 4, kept for future annotation)
master = [e for e in final if e['tier'] <= 3]
candidates = [e for e in final if e['tier'] == 4]

# IDs
for i, e in enumerate(master, 1):
    e['id'] = f"KS-{i:04d}"

# ---------------- write outputs ----------------
FIELDS = ['id','term_bn','romanization','literal_meaning','meaning_en','meaning_bn','category','region',
          'part_of_speech','register','offensiveness','usage_example_bn','usage_example_en','era','tags',
          'confidence','tier','source_type','source_url']

def write_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({**r, 'tags': '|'.join(r.get('tags', []))})

write_csv(FINAL + '/bangla_slang_master.csv', master)
write_csv(BASE + '/data/candidates/web_candidates_for_annotation.csv', candidates)
json.dump(master, open(FINAL + '/bangla_slang_master.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(candidates, open(BASE + '/data/candidates/web_candidates_for_annotation.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

by_cat = defaultdict(list)
for e in master:
    by_cat[e['category'] or 'unclassified'].append(e)
for cat, rows in by_cat.items():
    write_csv(FINAL + f'/by_category/{cat}.csv', rows)

os.makedirs(BASE + '/data/candidates', exist_ok=True)
stats = {
    'total': len(master),
    'by_category': {c: len(v) for c, v in sorted(by_cat.items())},
    'by_tier': dict(Counter(e['tier'] for e in master)),
    'by_source_type': dict(Counter(e['source_type'] for e in master)),
    'tier4_candidates': len(candidates),
    'with_meaning_en': sum(1 for e in master if e['meaning_en']),
    'with_meaning_bn': sum(1 for e in master if e['meaning_bn']),
    'with_romanization': sum(1 for e in master if e['romanization']),
    'with_example': sum(1 for e in master if e['usage_example_bn'] or e['usage_example_en']),
}
json.dump(stats, open(FINAL + '/stats.json', 'w', encoding='utf-8'), indent=1)
print(json.dumps(stats, indent=1))
