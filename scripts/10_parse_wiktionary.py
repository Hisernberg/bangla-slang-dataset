#!/usr/bin/env python3
"""Parse en.wiktionary + bn.wiktionary wikitext into structured slang entries."""
import json, re, os

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"

# ---------------- helpers ----------------
TEMPLATES = re.compile(r'\{\{[^{}]*\}\}')
def clean_wikitext(s):
    if not s: return ""
    s = re.sub(r'<ref[^>]*/>', '', s)
    s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'\[\[w?:[^\]|]*\|([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\[\[([^\]]*)\]\]', r'\1', s)
    s = re.sub(r"'''?", '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = TEMPLATES.sub('', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,;:')
    return s.strip()

# label templates that carry sense tags
LABEL_RE = re.compile(r'\{\{(lb|label|lbl)\|bn\|([^{}]*)\}\}')
def extract_labels(line):
    tags = []
    for m in LABEL_RE.finditer(line):
        for part in m.group(2).split('|'):
            p = part.strip().lower()
            if p and p not in ('bn',) and not p.startswith('_'):
                tags.append(p)
    return tags

def remove_all_templates(line):
    # iteratively remove nested templates
    prev = None
    while prev != line:
        prev = line
        line = re.sub(r'\{\{(?:[^{}]|\{[^{}]*\})*\}\}', '', line)
    return line

# ---------------- en.wiktionary ----------------
en_wt = json.load(open(RAW + "/wiktionary_en_wikitext.json", encoding="utf-8"))
en_cats = json.load(open(RAW + "/wiktionary_en_pages.json", encoding="utf-8"))

SENSE_TAGS = {
    'slang': 'slang', 'vulgar': 'vulgar', 'vulgar slang': 'vulgar', 'offensive': 'offensive',
    'derogatory': 'derogatory', 'informal': 'informal', 'pejorative': 'pejorative',
    'colloquial': 'colloquial', 'humorous': 'humorous', 'crude': 'crude', 'rude': 'rude',
    'ethnic slur': 'slur', 'slur': 'slur', 'obsolete': 'obsolete', 'archaic': 'archaic',
    'euphemistic': 'euphemism', 'figuratively': 'figurative', 'internet slang': 'internet',
    'regional': 'regional', 'dialectal': 'dialectal', 'dialect': 'dialectal',
    'chiefly bangladesh': 'bangladesh', 'bangladesh': 'bangladesh', 'india': 'india',
    'kolkata': 'kolkata', 'west bengal': 'west_bengal', 'dhaka': 'dhaka',
    'chittagong': 'chittagong', 'sylhet': 'sylhet', 'noakhali': 'noakhali',
}
REGION_MAP = {
    'chittagong': 'Chattogram', 'sylhet': 'Sylhet', 'dhaka': 'Dhaka', 'noakhali': 'Noakhali',
}
CAT_REGION = [
    ('Chittagonian Bengali', ('regional_chattogram', 'Chattogram')),
    ('Chittagonian', ('regional_chattogram', 'Chattogram')),
    ('Sylheti Bengali', ('regional_sylhet', 'Sylhet')),
    ('Sylheti', ('regional_sylhet', 'Sylhet')),
    ('Dhakaiya', ('regional_dhaka', 'Dhaka')),
    ('Noakhali', ('regional_other', 'Noakhali')),
    ('Bangladeshi Bengali', ('', 'Bangladesh')),
]
CAT_REG = {
    'slang': 'internet_social',  # default for generic slang; refined later
    'vulgar': 'profanity_curses', 'offensive': 'profanity_curses', 'crude': 'profanity_curses',
    'derogatory': 'profanity_curses', 'slur': 'profanity_curses', 'rude': 'profanity_curses',
}

COLLOQUIAL_FAMILY = {'slang','vulgar','offensive','crude','derogatory','slur','rude','informal','colloquial',
                     'pejorative','humorous','internet','euphemism','dialectal','regional','obsolete','archaic'}

def parse_en():
    entries = []
    for title, wt in en_wt.items():
        if title.startswith('-') or title.endswith('-'):
            continue  # skip bare morphemes
        # locate Bengali section
        m = re.search(r'^==\s*Bengali\s*==\s*$', wt, flags=re.M)
        if not m:
            continue
        sec = wt[m.end():]
        nxt = re.search(r'^==\s*[^=\n]+\s*==\s*$', sec, flags=re.M)
        if nxt:
            sec = sec[:nxt.start()]
        if not sec.strip():
            continue
        page_cats = [c for c in re.findall(r'\[\[Category:([^\]|]+)\]\]', wt)]
        pos = None
        defs = []
        for line in sec.split('\n'):
            pm = re.match(r'^===\s*([^=\n]+?)\s*===\s*$', line)
            if pm:
                pos = pm.group(1).strip().lower(); continue
            dm = re.match(r'^#(?!\#)[^#:*]', line)
            if not dm and line.startswith('#'):
                dm = True
            if dm and line.startswith('#'):
                raw_line = line.lstrip('#').strip()
                tags = extract_labels(line)
                text = remove_all_templates(raw_line)
                gloss = clean_wikitext(text)
                if len(gloss) < 2:
                    continue
                tags = sorted(set(SENSE_TAGS.get(t, t) for t in tags))
                # region/page-based
                region = 'Bangladesh'
                cat_hint = ''
                for pat, (cat, reg) in CAT_REGION:
                    if pat.lower() in ' '.join(page_cats).lower() or pat.lower() in ' '.join(tags).lower():
                        cat_hint, region = cat, reg
                        break
                # category choice: strongest signal wins
                if cat_hint:
                    category = cat_hint
                else:
                    category = None
                    for t in ('vulgar', 'offensive', 'crude', 'derogatory', 'slur', 'rude'):
                        if t in tags:
                            category = 'profanity_curses'; break
                defs.append({
                    'gloss': gloss, 'pos': pos, 'tags': tags,
                    'category': category, 'region': region,
                })
        if not defs:
            continue
        # keep only entries with a colloquial-family sense tag or slang/vulgar page category
        page_tag_cats = set()
        for c in en_cats.get(title, []):
            c = c.replace('Category:', '')
            if 'slang' in c: page_tag_cats.add('slang')
            if 'vulgar' in c: page_tag_cats.add('vulgar')
            if 'offensive' in c: page_tag_cats.add('offensive')
            if 'colloquial' in c: page_tag_cats.add('colloquial')
            if 'informal' in c: page_tag_cats.add('informal')
        defs = [d for d in defs if set(d['tags']) & COLLOQUIAL_FAMILY] if not page_tag_cats else defs
        # merge defs: prefer ones with explicit sense tags if any
        tagged = [d for d in defs if set(d['tags']) & COLLOQUIAL_FAMILY]
        keep = tagged or defs
        if not keep:
            continue
        # skip purely non-colloquial? keep everything; confidence reflects it
        glosses = []
        all_tags = set()
        for d in keep:
            glosses.append(d['gloss'])
            all_tags.update(d['tags'])
        cats = set(d['category'] for d in keep if d['category'])
        regions = set(d['region'] for d in keep)
        if not cats:
            if 'vulgar' in page_tag_cats or 'offensive' in page_tag_cats:
                cats = {'profanity_curses'}
            elif 'slang' in page_tag_cats:
                cats = set()
            else:
                cats = set()
        all_tags |= page_tag_cats
        all_tags &= COLLOQUIAL_FAMILY | {'bangladesh','india','kolkata','west_bengal','dhaka','chittagong','sylhet','noakhali','figurative','euphemism'}
        if not all_tags:  # no colloquial tags -> weak entry
            continue
        if 'bangladesh' not in regions and 'india' not in regions:
            regions.add('Bengal')
        entries.append({
            'term_bn': title,
            'meaning_en': ' ; '.join(glosses[:3]),
            'part_of_speech': keep[0]['pos'],
            'tags': sorted(all_tags),
            'category': sorted(cats)[0] if cats else '',
            'region': sorted(regions)[0] if regions else 'Bengal',
            'source_type': 'wiktionary_en',
            'source_url': 'https://en.wiktionary.org/wiki/' + title.replace(' ', '_'),
        })
    return entries

# ---------------- bn.wiktionary ----------------
bn_wt = json.load(open(RAW + "/wiktionary_bn_wikitext.json", encoding="utf-8"))
bn_cats = json.load(open(RAW + "/wiktionary_bn_pages.json", encoding="utf-8"))

def parse_bn():
    entries = []
    for title, wt in bn_wt.items():
        m = re.search(r'^==\s*(?:\{\{ভাষা\|bn\}\}|বাংলা)\s*==\s*$', wt, flags=re.M)
        if not m:
            continue
        sec = wt[m.end():]
        nxt = re.search(r'^==\s*[^=\n]+\s*==\s*$', sec, flags=re.M)
        if nxt:
            sec = sec[:nxt.start()]
        if not sec.strip():
            continue
        cats = [c.replace('Category:', '').replace('বিষয়শ্রেণী:', '') for c in re.findall(r'\[\[বিষয়শ্রেণী:([^\]|]+)\]\]', wt)]
        # POS from bn subheaders
        pos = ''
        pm = re.search(r'===\s*(বিশেষ্য|ক্রিয়া|বিশেষণ|ক্রিয়াবিশেষণ|সর্বনাম)\s*===', sec)
        if pm:
            pos = {'বিশেষ্য': 'noun', 'ক্রিয়া': 'verb', 'বিশেষণ': 'adjective',
                   'ক্রিয়াবিশেষণ': 'adverb', 'সর্বনাম': 'pronoun'}.get(pm.group(1), '')
        defs = []
        examples = []
        for line in sec.split('\n'):
            lx = re.search(r'\{\{usex\|bn\|([^{}|]+)', line)
            if lx:
                examples.append(re.sub(r'<[^>]+>', '', lx.group(1)).strip())
            if line.startswith('#'):
                text = remove_all_templates(line.lstrip('#').strip())
                gloss = clean_wikitext(text)
                if len(gloss) >= 2:
                    defs.append(gloss)
        if not defs:
            continue
        page_cats = ' '.join(bn_cats.get(title, []) + cats)
        if ('ঢাকাইয়া' not in page_cats and 'স্ল্যাং' not in page_cats and 'গালি' not in page_cats):
            continue  # drop broad-vocabulary pages
        category, region = '', 'Dhaka'
        if 'ঢাকাইয়া' in page_cats:
            category, region = 'regional_dhaka', 'Dhaka (Old Dhaka / Kutti)'
        elif 'গালি' in page_cats or 'অশ্লীল' in page_cats:
            category, region = 'profanity_curses', 'Bangladesh'
        entries.append({
            'term_bn': title,
            'meaning_bn': ' ; '.join(defs[:3]),
            'usage_example_bn': examples[0] if examples else '',
            'part_of_speech': pos,
            'tags': ['colloquial'] if not category else ['colloquial', 'dialectal'],
            'category': category,
            'region': region,
            'source_type': 'wiktionary_bn',
            'source_url': 'https://bn.wiktionary.org/wiki/' + title,
        })
    return entries

en_entries = parse_en()
bn_entries = parse_bn()
json.dump(en_entries, open(RAW + "/parsed_wiktionary_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bn_entries, open(RAW + "/parsed_wiktionary_bn.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"en parsed: {len(en_entries)} | bn parsed: {len(bn_entries)}")
from collections import Counter
print("en by category:", Counter(e['category'] for e in en_entries).most_common())
print("en sample:")
for e in en_entries[:8]:
    print("  ", e['term_bn'], '|', e['meaning_en'][:70], '|', e['category'], '|', e['tags'][:5])
print("bn sample:")
for e in bn_entries[:8]:
    print("  ", e['term_bn'], '|', e.get('meaning_bn','')[:60])
