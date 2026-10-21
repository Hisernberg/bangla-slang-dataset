# TAXONOMY — 10 Categories of Bangla Slang

Kothar Rong organizes Bangla slang along **two axes**: *where* the language lives (region) and *how* it is used (style). Four categories are regional, six are style-based — mirroring how slang actually spreads: a dialect word can become a meme, a film line can become a street insult, and a campus joke can become national vocabulary.

## Regional categories

### 1. `regional_dhaka` — ঢাকাইয়া (101 entries)
Street speech of Dhaka city — the Kutti/Sobbasi heritage of Old Dhaka blended with modern urban slang. Includes address terms (মামা, ব্যাটা, কিরে), street-life vocabulary (টোকাই, মাস্তান, মোক্তার, ঠুঙ্গি), Dhakaiya verbs (জিগাই, বুঝলা, গেলা), and mild curses with local flavor (টাইটা যা, মাইরা খা). *Inclusion criterion:* term is documented as Dhaka-street usage or appears in Dhakaiya dialect sources.

### 2. `regional_chattogram` — চট্টগ্রামীয়া (744 entries)
The Chittagonian dialect's slang and vulgar lexicon — the largest regional block, reflecting how distinctive the dialect is from standard Bangla. Includes iconic catchphrases (কেন মামা লাগব), hospitality phrases (তালে বাইয়া যাইর), and the Apache-2.0 licensed vulgar lexicon harvested from Hugging Face. *Inclusion criterion:* term attested in Chittagonian dialect sources.

### 3. `regional_sylhet` — সিলেটি (14 entries)
Sylheti interrogatives, greetings, and humor markers (কিতা, কিতা খবর, কিতা গরু মামা, বালে বালে). A deliberately high-quality small set: every entry is gold-curated with transliteration. Reference material in Sylheti Nagri script (ꠡꠣꠉꠔꠝ) is linked in SOURCES.md. *Inclusion criterion:* term attested in Sylheti sources or gold-verified.

### 4. `colloquial_dialectal` — সাধারণ কথ্য ও আঞ্চলিক (125 entries)
The catch-all for general colloquial Bangla, old-school slang, and minor-dialect words (Noakhali, Barishal, Dinajpur, Kolkata) that don't belong to the three flagship regions. Includes parliamentary-meme vocabulary (চুদুর বুদুর) and dialect verbs collected from Wiktionary's dialectal labels. *Inclusion criterion:* colloquial/dialectal attestation without a flagship-region anchor.

## Style categories

### 5. `profanity_curses` — গালি ও অভিশাপ (1,048 entries)
The largest style category — insults, curses, and severe profanity, harvested from community moderation lexicons (Nirmol, deshi-slang), the 175-item blog list, and Wiktionary's vulgar/offensive labels. Every entry carries `offensiveness` 0–3 so researchers can grade severity. *Inclusion criterion:* primary function is insult/curse, per source labels or gold judgment. ⚠️ Content warning applies.

### 6. `internet_social` — ইন্টারনেট ও সোশ্যাল মিডিয়া (18 entries)
Meme-era vocabulary: হাহাকার (despair meme), আইডি ডিলিট (fake-hacker threat), ব্লুটিক (verified show-off), মিম লর্ড, স্ক্রিনশট নিলাম ("I have the receipts"). Mostly Bangla-English hybrids. *Inclusion criterion:* term was born or mutated online.

### 7. `campus_student` — ক্যাম্পাস ও ছাত্রজীবন (15 entries)
Exam and hostel culture: সাপ্লাই, রেফার, ব্যাকলগ, ক্র্যাশ প্রোগ্রাম, কাটিং, প্রক্সি, টেবিল ভাড়া (the cheating racket), ফার্স্ট/ব্যাক বেঞ্চার, রাগিং. *Inclusion criterion:* term used primarily in student life.

### 8. `entertainment_media` — সিনেমা-নাটক ও বিনোদন (9 entries)
Cinema and TV catchphrases that escaped the screen: সিনেমা দেখিস বেশি, ডায়ালগ মারা, হিরো সাহেব, ফুল ডায়ালগ, ক্যান মামা লাগব (doubly categorized as Chittagonian in origin). *Inclusion criterion:* film/TV origin with street adoption.

### 9. `relationships_emotions` — সম্পর্ক ও আবেগ (13 entries)
The vocabulary of love, sulks, and heartbreak: মায়া, ভালো লাগা, মন খারাপ, অভিমান, একতারা প্রেম (one-sided love), প্রেম পালানো (elope), ব্রেকআপ পার্টি. *Inclusion criterion:* term expresses a relationship/emotion register.

### 10. `social_political` — সামাজিক-রাজনৈতিক (13 entries)
Power-talk: চামচা (sycophant), হাওয়া (political wind), ক্যাডার (party muscle), রাজাকার (the heaviest political slur), গুম (forced disappearance), এনকাউন্টার (staged shootout euphemism), বিদেশি চক্র (foreign conspiracy excuse). *Inclusion criterion:* term comments on power, politics, or society.

## Assignment pipeline

1. **Gold entries** — assigned at curation time (human judgment).
2. **Wiktionary entries** — mapped from sense labels (`vulgar` → profanity) and dialect categories (Chittagonian/Sylheti/Dhakaiya).
3. **Structured lexicons** — mapped from the source's own label system.
4. **Residue** — keyword classifier on meanings/tags, then a slang-family tag fallback.
5. **Auto-extracts that still fail classification are quarantined**, never force-fitted — no junk in the 10 categories.
