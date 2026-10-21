#!/usr/bin/env python3
import json
"""Gold layer part 2: profanity, internet, campus, entertainment, relationships, social-political."""

E = []
def a(term, roman, literal, men, mbn, cat, region, pos='noun', reg='street', off=0, ex='', exen='', era='modern', tags=''):
    E.append(dict(term_bn=term, romanization=roman, literal_meaning=literal, meaning_en=men,
                  meaning_bn=mbn, category=cat, region=region, part_of_speech=pos, register=reg,
                  offensiveness=off, usage_example_bn=ex, usage_example_en=exen, era=era, tags=tags))

# ================= 5. PROFANITY & CURSES (গালি ও অভিশাপ) =================
c, r = 'profanity_curses', 'Bengal-wide'
a('শালার পোলা', 'shalar pola', 'son of brother-in-law', 'standard mild-to-medium insult', 'মাঝারি মাত্রার প্রচলিত গালি', c, r, 'phrase', 'vulgar', 2, '', '', 'classic', 'insult')
a('কুত্তার বাচ্চা', 'kuttar baccha', 'son of a dog', 'you son of a bitch', 'কুকুরের বাচ্চা — কঠোর গালি', c, r, 'phrase', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('হারামজাদা', 'haramjada', 'illegitimate (Arabic)', 'bastard', 'অবৈধজাত — কঠোর গালি', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('হারামখোর', 'haramkhor', 'eater of the forbidden', 'scoundrel, shameless freeloader', 'হারাম খাওয়া নীতিহীন লোক', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('মাদারচোদ', 'madarchod', '(Hindi/Urdu root)', 'motherfucker (shared Indo-Aryan profanity)', 'কঠোর মাতৃভিত্তিক গালি', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('বাঞ্চোদ', 'bonchod', '(sister-root)', 'sisterfucker (common abbreviated curse)', 'কঠোর গালি (সংক্ষিপ্ত রূপ)', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('হুজ্জা', 'hujja', '(nuisance)', 'annoying pest; shameless person', 'দুষ্টু নোংরা লোক', c, r, 'noun', 'street', 2, '', '', 'classic', 'insult')
a('বোকাচোদা', 'bokachoda', 'fool-fucker', 'dumbass (very common online insult)', 'বোকা — অনলাইনে অতি প্রচলিত', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('হিজরা', 'hijra', 'eunuch/trans person (derogatory use)', 'derogatory term implying cowardice or uselessness; slur context', 'অপমানজনক ব্যবহার; রূপক অর্থে কর্মহীন', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'slur_caution')
a('চোদনা', 'chodna', '(vulgar root)', 'severe sexual profanity (verb)', 'কঠোর যৌন গালি', c, r, 'verb', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('গালমন্দ', 'galmand', 'insult-prone', 'abusive-mouthed person', 'গালি দেওয়ার অভ্যাসযুক্ত লোক', c, r, 'adjective', 'informal', 1, '', '', 'classic', 'character')
a('বেইমান', 'beiman', 'without honor', 'traitor, dishonest person', 'বিশ্বাসঘাতক', c, r, 'adjective', 'informal', 1, 'বেইমান বন্ধু!', 'Traitor friend!', 'classic', 'betrayal')
a('জারজ', 'jaraj', 'illegitimate', 'bastard (classical/Biblical-rooted curse)', 'অবৈধজাত', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('ভাড়াতের বাপ', 'bharater bap', 'hired father', 'sellout who betrays for money', 'টাকায় বিক্রি হওয়া ব্যক্তি', c, r, 'phrase', 'street', 2, '', '', 'modern', 'sellout')
a('টাকার পোলা', 'takar pola', 'money boy', 'spoiled rich brat', 'বাবুর ছেলে; অহংকারী ধনী পোলা', c, r, 'phrase', 'street', 1, '', '', 'modern', 'class_mockery')
a('খেয়ালি খানকি', 'kheyali khanki', 'whimsical whore (euphemistic joke)', 'humorous euphemism for a fickle person — famous "clean cuss" joke', 'গালি না বলে বলা কৌতুক-প্রতিশব্দ', c, r, 'phrase', 'humorous', 2, '', '', 'classic', 'euphemism_joke')

# ================= 6. INTERNET & SOCIAL MEDIA (ইন্টারনেট) =================
c, r = 'internet_social', 'Bangladesh (online)'
a('জোস', 'joss', '(Eng. josh/zeal)', 'awesome, lit', 'দুর্দান্ত, জমঝমাট', c, r, 'adjective', 'informal', 0, 'পিকটা একদম জোস!', 'The pic is totally lit!', 'modern', 'praise')
a('হাহাকার', 'hahakar', 'cry of despair', 'dramatic despair meme — "my life is over"', 'নাটকীয় বিষণ্ণতার মিম-শব্দ', c, r, 'noun', 'informal', 0, 'ফেল খাইলাম, হাহাকার!', 'I failed, hahakar!', 'modern', 'meme')
a('ভাইরাল', 'viral', '(Eng.)', 'gone viral', 'সবার কাছে ছড়িয়ে পড়া', c, r, 'adjective', 'informal', 0, '', '', 'modern', 'platform')
a('ব্লুটিক', 'bluetick', 'blue tick', 'verified-badge show-off', 'নীল টিক ধরে রাখা অহংকার', c, r, 'noun', 'informal', 1, '', '', 'modern', 'platform_status')
a('ট্রল', 'troll', '(Eng.)', 'trolling; a troll', 'কষ্ট দেওয়ার জন্য মন্তব্যকারী', c, r, 'noun', 'informal', 1, '', '', 'modern', 'platform')
a('মিম লর্ড', 'meme lord', 'meme lord', 'self-crowned king of memes', 'মিমের রাজা দাবিদার', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'meme')
a('আইডি ডিলিট', 'ID delete', 'ID delete', '"I\'ll delete your ID" — iconic fake-hacker threat', 'হ্যাকার-অভিনয়ের ক্লাসিক হুমকি', c, r, 'phrase', 'informal', 1, 'বন্ধু ভাবোয়াইলা আইডি ডিলিট করবো', 'Act like a friend or I\'ll delete your ID', 'modern', 'meme|threat')
a('স্ক্রিনশট নিলাম', 'screenshot nilam', 'took a screenshot', '"I have the receipts" — proof-keeping warning', 'প্রমাণ সংগ্রহ করে ফেলেছি', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'receipts')
a('ইনবক্স করো', 'inbox koro', 'do inbox', 'DM me', 'মেসেজ দাও ইনবক্সে', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'platform')
a('চেক কইরো না', 'check koiro na', 'don\'t check', '"don\'t check my profile" — guilty plea', 'প্রোফাইল দেখো না — অপরাধবোধের আর্তনাদ', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'guilty')
a('ফ্রি রিলোড', 'free reload', 'free reload', 'getting something free repeatedly; freeloading', 'বিনামূল্যে বারবার সুবিধা নেওয়া', c, r, 'phrase', 'informal', 1, '', '', 'modern', 'freeloader')
a('এক্সপোজড', 'exposed', '(Eng.)', 'exposed!', 'ধরা পড়ে গেছো!', c, r, 'interjection', 'informal', 1, '', '', 'modern', 'callout')
a('সেলফি বাজ', 'selfie baj', 'selfie-addict', 'selfie addict (বাজ = addicted)', 'সেলফির পেছনে পাগল', c, r, 'noun', 'informal', 1, '', '', 'modern', 'addiction')
a('প্যাঁচ', 'pyech', 'coil', 'tricky twist in talk; mind-game', 'কথার ফাঁদ; বোকা বানানোর ফন্দি', c, r, 'noun', 'street', 1, '', '', 'classic', 'trickery')
a('পাইস্তা', 'paista', 'street rat', 'cunning little rascal', 'ছোকরা ধূর্ত লোক', c, r, 'noun', 'street', 2, '', '', 'classic', 'mockery')
a('বাপের পল্লাও', 'baper pollao', 'father\'s pulao', 'cushioned life of privilege — "fed on father\'s pulao"', 'বাপের টাকায় পরতে বসে থাকা', c, r, 'phrase', 'street', 2, '', '', 'modern', 'class_mockery')
a('একদম ফ্রি', 'ekdom free', 'totally free', 'shamelessly free(loading)', 'একেবারে মাগে-ফ্রি', c, r, 'phrase', 'informal', 1, '', '', 'modern', 'freeloader')
a('নাইট লাইফ', 'night life', 'night life', 'late-night internet socializing', 'গভীর রাতের ফেসবুক-বিচরণ', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'platform')

# ================= 7. CAMPUS & STUDENT LIFE (ক্যাম্পাস) =================
c, r = 'campus_student', 'Bangladesh (campus)'
a('সাপ্লাই', 'supply', 'supplementary', 'supplementary exam (failed but promotable)', 'পরীক্ষায় কন্ডিশনাল পাস', c, r, 'noun', 'informal', 0, 'ম্যাথে সাপ্লাই খাইছি', 'I got a supply in math', 'classic', 'exam')
a('রেফার', 'refer', '(Eng. refer)', 'failed a course needing retake', 'কোর্স ফেল করা', c, r, 'verb', 'informal', 0, 'থিমোতে রেফার হইছে', 'Got referred in thermo', 'classic', 'exam')
a('ব্যাকলগ', 'backlog', 'backlog', 'piled-up failed courses', 'জমে থাকা ফেল করা কোর্স', c, r, 'noun', 'informal', 0, '', '', 'classic', 'exam')
a('ক্র্যাশ প্রোগ্রাম', 'crash program', 'crash program', 'last-minute all-nighter syllabus sprint', 'রাতজাগা করে সিলেবাস শেষ করা', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'study')
a('গেস পেপার', 'guess paper', 'guess paper', 'predictive question pack — shortcut culture', 'সম্ভাব্য প্রশ্নের বই', c, r, 'noun', 'informal', 1, '', '', 'classic', 'study')
a('টেবিল ভাড়া', 'table bhara', 'rent a table', 'seat-rental cheating racket in colleges', 'কলাকার ভাড়া দিয়ে নকল করা', c, r, 'phrase', 'street', 2, '', '', 'classic', 'cheating')
a('কাটিং', 'cutting', 'cutting', 'bunking class', 'ক্লাস ফাঁকি দেওয়া', c, r, 'noun', 'informal', 0, 'আজ কাটিং দিমু', 'Bunking today', 'classic', 'attendance')
a('প্রক্সি', 'proxy', 'proxy', 'attendance marked by a friend in your place', 'বন্ধুর নামে হাজিরা', c, r, 'noun', 'informal', 1, '', '', 'classic', 'attendance')
a('ভাইভার প্যাঁচ', 'vivar pyech', 'viva twist', 'the examiner\'s sneaky question', 'ভাইভায় শিক্ষকের ফাঁদপ্রশ্ন', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'exam')
a('ফার্স্ট বেঞ্চার', 'first bencher', 'first bencher', 'teacher\'s pet, front-row nerd', 'প্রথম বেঞ্চে বসা গুনিয়ে', c, r, 'noun', 'informal', 0, '', '', 'classic', 'stereotype')
a('ব্যাক বেঞ্চার', 'back bencher', 'back bencher', 'rear-row legend; unserious student', 'পেছনের বেঞ্চের দুর্দান্ত দুষ্টু', c, r, 'noun', 'informal', 0, '', '', 'classic', 'stereotype')
a('সেশনাল', 'sessional', 'sessional', 'lab/practical course ( BUET/varsity slang)', 'ল্যাব কোর্স', c, r, 'noun', 'informal', 0, '', '', 'classic', 'study')
a('সিনিয়র ভাই', 'senior bhai', 'senior brother', 'senior — often a source of enforced respect (ragging culture)', 'উর্ধ্বতন শিক্ষার্থী', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'hierarchy')
a('রাগিং', 'ragging', 'ragging', 'hazing of juniors', 'জুনিয়রদের প্রথা-ভাঙা হেনস্থা', c, r, 'noun', 'informal', 2, '', '', 'classic', 'hazing')
a('হল বন্ধু', 'hall bondhu', 'hall friend', 'dorm-mate for life', 'হলের আপন বন্ধু', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'friendship')

# ================= 8. ENTERTAINMENT (সিনেমা-নাটক) =================
c, r = 'entertainment_media', 'Bengali cinema/TV'
a('সিনেমা দেখিস বেশি', 'cinema dekhis beshi', 'you watch too many movies', '"you watch too much cinema" — telling someone they\'re fantasizing', 'অবাস্তব কল্পনা করছিস', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'fantasy_callout')
a('ডায়ালগ মারা', 'dialog mara', 'throw a dialogue', 'deliver cinematic punchlines', 'সিনেমার মতো সংলাপ ছোড়া', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'performance')
a('ক্যান মামা লাগব', 'ken mama lagbe', 'why uncle needed', 'film-origin refusal catchphrase (Chittagonian)', 'চলচ্চিত্র-উৎসের বিখ্যাত প্রত্যাখ্যান', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'film_origin')
a('হিরো সাহেব', 'hero shaheb', 'Mr. Hero', 'ironic "Mr. Hero"', 'ব্যঙ্গে হিরো সম্বোধন', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'sarcasm')
a('ভিলেন', 'villain', '(Eng.)', 'villain — real-life label', 'খলনায়ক — বাস্তবে লাগানো লেবেল', c, r, 'noun', 'informal', 1, '', '', 'classic', 'labeling')
a('রিল লাইফ', 'reel life', 'reel life', 'performative fake life vs real', 'নাটকীয় নকল জীবন', c, r, 'phrase', 'informal', 1, '', '', 'modern', 'authenticity')
a('ক্লাইম্যাক্স', 'climax', '(Eng.)', 'dramatic finale of any mundane event', 'ছোট বিষয়ে নাটকীয়তা', c, r, 'noun', 'informal', 0, '', '', 'modern', 'drama')
a('ফুল ডায়ালগ', 'full dialog', 'full dialogue', 'giving a full cinematic monologue', 'পুরো সিনেমার মনোলগ দেওয়া', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'performance')
a('নায়িকা হওয়ার স্বপ্ন', 'nayika hoiyar shopno', 'dream of becoming heroine', 'daydreamer; delusional aspirant', 'কল্পনাপ্রবণ; অবাস্তব স্বপ্নদেখা', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'daydream')

# ================= 9. RELATIONSHIPS & EMOTIONS (সম্পর্ক-আবেগ) =================
c, r = 'relationships_emotions', 'Bengal (popular)'
a('মায়া', 'maya', 'affection/illusion', 'deep infatuation — also the trap of it', 'প্রবল ভালোবাসা; মায়াজাল', c, r, 'noun', 'informal', 0, 'মায়ায় পড়েছে বন্ধু', 'Fallen into maya, my friend', 'classic', 'love')
a('ভালো লাগা', 'bhalo laga', 'feeling good', 'crush feeling; liking someone', 'পছন্দ; ক্রাশ', c, r, 'noun', 'informal', 0, '', '', 'classic', 'crush')
a('মন খারাপ', 'mon kharap', 'heart bad', 'feeling down — the national catch-all sadness', 'মন খারাপ — জাতীয় দুঃখ-বাক্য', c, r, 'phrase', 'informal', 0, 'আজকে বহুত মন খারাপ', 'Feeling so down today', 'classic', 'sadness')
a('অভিমান', 'obhiman', 'hurt pride', 'the loving sulkt — hurt from someone dear', 'প্রিয়জনের আচরণে হৃদয়ব্যথা', c, r, 'noun', 'informal', 0, '', '', 'classic', 'emotion')
a('প্রেম পালানো', 'prem palano', 'elope with love', 'elope; also "love-flee" as romance cliché', 'প্রেম করে পালিয়ে যাওয়া', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'romance')
a('প্রপোজ', 'propose', '(Eng.)', 'confess love (formalized by romcoms)', 'ভালোবাসার প্রস্তাব দেওয়া', c, r, 'verb', 'informal', 0, '', '', 'modern', 'romance')
a('ব্রেকআপ পার্টি', 'breakup party', 'breakup party', 'moving-on celebration meme', 'বিচ্ছেদ-উৎসব (মিম-সংস্কৃতি)', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'meme')
a('ক্রাশ', 'crash/crush', '(Eng.)', 'crush', 'গোপন পছন্দের মানুষ', c, r, 'noun', 'informal', 0, '', '', 'modern', 'romance')
a('একতারা প্রেম', 'ektara prem', 'one-string love', 'one-sided love', 'একতরফা ভালোবাসা', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'one_sided')
a('রাগ করা', 'rag kora', 'do anger', 'sulking anger (usually cute, in relationships)', 'কষ্ট করে রাগ দেখানো', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'emotion')
a('খেপা', 'khepa', 'temper flare', 'the sulks; a fit of temper', 'আমেষা রাগ', c, r, 'noun', 'informal', 0, '', '', 'classic', 'emotion')
a('বিরক্ত', 'birokto', 'irritated', 'fed up', 'বিরক্ত — যথেষ্ট হয়েছে', c, r, 'adjective', 'informal', 0, '', '', 'classic', 'emotion')
a('প্রেমিক-ছদ্মবেশ', 'premik chhadmobesh', 'lover in disguise', 'friend acting secretly as lover', 'বন্ধুর ছদ্মবেশে প্রেমিক', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'situationship')

# ================= 10. SOCIAL & POLITICAL (সামাজিক-রাজনৈতিক) =================
c, r = 'social_political', 'Bengal (politics)'
a('চামচা', 'chamcha', 'spoon', 'sycophant, hanger-on — the eternal political spoon', 'তোষামোদকারী; চাটুকার', c, r, 'noun', 'informal', 1, 'দলের চামচা', 'Party spoon-sycophant', 'classic', 'politics')
a('হাওয়া', 'hawa', 'wind', 'political wind — shifting loyalty with power', 'ক্ষমতার দিকে হাওয়ার দিক বদল', c, r, 'noun', 'informal', 1, 'হাওয়া উল্টো দিকে বইছে', 'The wind is blowing the other way now', 'classic', 'politics')
a('ক্যাডার', 'cadre', 'cadre', 'party muscleman on campus or street', 'দলীয় সন্ত্রাসী; সংগঠক-সন্ত্রাসী', c, r, 'noun', 'street', 2, '', '', 'classic', 'politics')
a('লাইন মানা', 'line mana', 'obey the line', 'toe the party line', 'দলীয় নির্দেশ মানা', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'politics')
a('গুম', 'gum', 'disappearance', 'forced disappearance — the darkest word of the decade', 'গুম — জোরপূর্বক নিখোঁজ', c, r, 'noun', 'formal_slang', 0, '', '', 'modern', 'rights')
a('এনকাউন্টার', 'encounter', '(Eng.)', 'staged shootout euphemism', 'মঞ্চস্থ বন্দুকযুদ্ধের মৃদু প্রয়োগ', c, r, 'noun', 'formal_slang', 0, '', '', 'modern', 'euphemism')
a('হলুদ সাংবাদিকতা', 'holud sangbadikota', 'yellow journalism', 'yellow journalism (borrowed but localized)', 'পেশাদার মিথ্যা সংবাদ', c, r, 'phrase', 'informal', 0, '', '', 'modern', 'media')
a('রাজাকার', 'rajakar', 'war collaborator (\'71)', '1971 war collaborator — heaviest political slur in Bangladesh', 'স্বাধীনতা-বিরোধী দোসর — সবচেয়ে ভারী রাজনৈতিক গালি', c, r, 'noun', 'formal_slang', 2, '', '', 'classic', 'history')
a('বিদেশি চক্র', 'bideshi chokro', 'foreign ring', '"foreign conspiracy" — the universal excuse', 'বিদেশি ষড়যন্ত্র — সর্বজনীন অজুহাত', c, r, 'phrase', 'formal_slang', 1, '', '', 'modern', 'excuse')
a('বার্জি', 'bargi', '(historic marauder)', 'police van / law-enforcement (slang dread)', 'পুলিশের ভ্যান — ভয়ের রূপক', c, r, 'noun', 'street', 2, '', '', 'classic', 'policing')
a('মামা হওয়া', 'mama howa', 'become uncle', 'become the establishment\'s favorite', 'সরকারি পছন্দের লোক হয়ে যাওয়া', c, r, 'phrase', 'informal', 1, '', '', 'modern', 'power')
a('আন্দোলন-ভাই', 'andolon bhai', 'movement brother', 'professional protest figure', 'পেশাদার আন্দোলনকারী', c, r, 'phrase', 'street', 2, '', '', 'modern', 'activism')

json.dump(E, open('/home/z/my-project/bangla-slang-dataset/data/raw/gold_part2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('part2 entries:', len(E))
from collections import Counter
print(Counter(e['category'] for e in E))
