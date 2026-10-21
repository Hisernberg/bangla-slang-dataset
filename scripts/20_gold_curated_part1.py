#!/usr/bin/env python3
import json
"""Curated gold-layer entries: full-schema Bangla slang, verified senses, 10 categories.
Part 1: regional (dhaka, chattogram, sylhet, other) + profanity basics.
Fields: term_bn, romanization, literal_meaning, meaning_en, meaning_bn, category, region,
part_of_speech, register, offensiveness, usage_example_bn, usage_example_en, era, tags"""

E = []
def a(term, roman, literal, men, mbn, cat, region, pos='noun', reg='street', off=0, ex='', exen='', era='modern', tags=''):
    E.append(dict(term_bn=term, romanization=roman, literal_meaning=literal, meaning_en=men,
                  meaning_bn=mbn, category=cat, region=region, part_of_speech=pos, register=reg,
                  offensiveness=off, usage_example_bn=ex, usage_example_en=exen, era=era, tags=tags))

# ================= 1. REGIONAL — DHAKA (ঢাকাইয়া) =================
c, r = 'regional_dhaka', 'Dhaka (Old Dhaka / urban street)'
a('মামা', 'mama', 'maternal uncle', 'universal friendly address to any male peer or elder; also self-description as the "boss" of a situation', 'বন্ধুত্বপূর্ণ সম্বোধন; নিজেকে গুরু/খোদা দাবি করা', c, r, 'noun', 'informal', 0, 'কী অবস্থা মামা?', 'What\'s up, mama?', 'classic', 'address|friendly')
a('বাপ', 'bap', 'father', 'boss/legend; someone unbeatable', 'অসাধারণ দক্ষ ব্যক্তি; বস', c, r, 'noun', 'informal', 0, 'তুই একদম বাপ রে!', 'You are the absolute boss!', 'modern', 'praise')
a('পোলা', 'pola', 'boy/lad', 'guy, dude (urban)', 'ছেলে; বন্ধু বোঝাতে', c, r, 'noun', 'street', 0, 'ওই পোলাটা দেখ, কী করছে', 'Look at that guy, what is he doing', 'classic', 'reference')
a('ব্যাটা', 'byata', 'fellow/lad', 'fellow, bloke — often teasing or admonishing', 'বন্ধুসুলভ সম্বোধন; শাসনও করা যায়', c, r, 'noun', 'street', 0, 'কিরে ব্যাটা, কোথায় আইছস?', 'Hey dude, where have you been?', 'classic', 'address')
a('কিরে', 'kire', '(interjection)', 'hey! — blunt call-out to an equal', 'সমবয়সীকে ডাকার অশিষ্ট ধ্বনি', c, r, 'interjection', 'street', 0, 'কিরে, খবরদার!', 'Hey, watch out!', 'classic', 'address')
a('ল্যাওয়ারা', 'lawara', '(of low birth)', 'worthless person; good-for-nothing', 'মূল্যহীন, নিকৃষ্ট লোক', c, r, 'adjective', 'street', 2, 'ল্যাওয়ারা পোলা কাজে আসে না', 'A worthless guy is of no use', 'classic', 'insult')
a('ফালতু', 'faltu', '(from Eng. faulty)', 'useless, junk, extra', 'অপ্রয়োজনীয়; অকেজো', c, r, 'adjective', 'informal', 1, 'ফালতু কথা বাদ দে', 'Stop the useless talk', 'classic', 'dismissal')
a('টোকাই', 'tokai', '(one who snatches)', 'street urchin of Old Dhaka; snatcher', 'পুরান ঢাকার রাস্তার বাচ্চা; ছোবলমার', c, r, 'noun', 'street', 2, 'টোকাই দিয়ে মোবাইল নিয়া গেল', 'A tokai snatched the phone', 'classic', 'street_life')
a('মাস্তান', 'mastan', '(Persian: rogue)', 'muscleman, gangster, local goon', 'পেশাদার সন্ত্রাসী; মোক্তার', c, r, 'noun', 'street', 2, 'এলাকার মাস্তানরা চাঁদা নিচ্ছে', 'Local goons are collecting extortion', 'classic', 'crime')
a('মোক্তার', 'moktar', '(Urdu: agent)', 'area boss who brokers everything — from cricket matches to deals', 'নিয়ন্ত্রক দালাল; এলাকার মাদারি লোক', c, r, 'noun', 'street', 1, 'ওই মোক্তারের হাত থেকে বাঁচা', 'Surviving that fixer\'s grip', 'classic', 'street_power')
a('হালুম', 'halum', '(eastern dialect: brother-in-law word)', 'call-out expressing bravado or challenge; "come on!"', 'সাহস দেখানোর চিৎকার; চ্যালেঞ্জ', c, r, 'interjection', 'street', 1, 'হালুম কই হালুম!', 'Where is that bravado, halum!', 'modern', 'challenge')
a('মিয়া ভাই', 'miya bhai', 'mister brother', 'ironic respect for a show-off; sometimes slur against immigrants', 'মজা করে দেওয়া সম্বোধন; ক্ষেত্রবিশেষে অপমানজনক', c, r, 'phrase', 'street', 1, 'মিয়া ভাই খুব টাকাওয়ালা হইগেন', 'Miya bhai has become rich, huh', 'modern', 'irony')
a('গোল্লাছুট', 'gollachhut', '(call for a free run in street games)', 'gone; escaped; ended — "long gone!"', 'সুযোগ পেয়ে পালিয়ে যাওয়া; শেষ', c, r, 'interjection', 'street', 0, 'সে তো গোল্লাছুট বাবু!', 'He is long gone, buddy!', 'classic', 'escape')
a('জিগাই', 'jigai', 'to ask', 'to ask (Dhakaiya verb)', 'জিজ্ঞেস করা', c, r, 'verb', 'dialect', 0, 'একটা কথা জিগাই?', 'Can I ask something?', 'classic', 'verb')
a('বুঝলা', 'bujhla', 'did you understand', 'you got it? — street confirmation', 'বুঝলে? (রাস্তার ভাষায়)', c, r, 'verb', 'street', 0, 'বুঝলা বুঝলা, আর জিগাই না', 'Got it, got it, no more questions', 'classic', 'confirmation')
a('টাইটা যা', 'taita ja', 'go squeeze', 'mild curse: "go away, get lost"', 'ঘেঁষা-না-ঘেঁষা হালকা গালি', c, r, 'phrase', 'street', 2, 'টাইটা যা, কাজে আয় না', 'Get lost, you are useless', 'classic', 'mild_curse')
a('মাইরা খা', 'maira kha', 'eat after being beaten', 'mocking curse: "you deserve a beating"', 'পিট খেয়ে খেতে থাক হে গালি', c, r, 'phrase', 'street', 3, 'মাইরা খা, দাঁত ভাঙবো কিন্তু', 'Get beaten and eat, I will break your teeth', 'classic', 'curse')
a('খাইতে চাই', 'khaite chai', 'want to eat', '"I want a share" — hinted demand for a cut', 'বাট্টা বা অংশ চাওয়ার ইঙ্গিত', c, r, 'phrase', 'street', 1, 'সে সব সময় খাইতে চাই বলে', 'He always wants a cut', 'classic', 'demand')
a('পাগলামি পোলা', 'pagolami pola', 'madness boy', 'a wild, crazy dude', 'পাগলাটে ছেলে', c, r, 'phrase', 'street', 1, 'সে একদম পাগলামি পোলা', 'He is a total crazy dude', 'classic', 'character')
a('নাটক করো না', 'natak koro na', 'don\'t do drama', 'stop the drama/acting', 'অতিরিক্ত অভিনয় বন্ধ করো', c, r, 'phrase', 'informal', 0, 'নাটক করো না, সোজাসুজি বল', 'Stop the drama, speak straight', 'modern', 'dismissal')
a('আইনস্টাইন', 'Ainstein', 'Einstein', 'sarcastic "genius" for someone stating the obvious', 'ব্যঙ্গে জিনিয়াস সম্বোধন', c, r, 'noun', 'informal', 1, 'ও মামা, তুমি তো আইনস্টাইন!', 'Wow mama, you are Einstein!', 'modern', 'sarcasm')
a('চট্পটে', 'chotpotey', 'quick-quick', 'brisk, sharp, no-nonsense', 'কর্মচক্রে তৎপর; ঝরঝরে', c, r, 'adjective', 'informal', 0, 'ও খুব চট্পটে পোলা', 'He is a very brisk fellow', 'classic', 'praise')
a('ঠুঙ্গি', 'thungi', '(hanging shop)', 'tiny roadside hanging shop; meagre setup', 'রাস্তার ছোট ঝুলন্ত দোকান; ক্ষুদ্র আয়োজন', c, r, 'noun', 'dialect', 0, 'ঠুঙ্গির দোকান দিয়ে শুরু', 'Started with a tiny hanging shop', 'classic', 'street_economy')
a('দাদা', 'dada', 'elder brother', 'elder-brother honorific used for street seniors, also "boss" in Kolkata style', 'শ্রদ্ধার সম্বোধন; এলাকার বড় ভাই', c, r, 'noun', 'informal', 0, 'দাদা বলছেন যাও, যাও', 'Dada says go, go', 'classic', 'address')
a('শালা', 'shala', 'brother-in-law (hala)', 'mild insult between friends; "you rascal"', 'বন্ধুর মধ্যে হালকা গালি; ধৃষ্ট', c, r, 'noun', 'street', 2, 'শালা, বিশ্বাসঘাতক!', 'Rascal, traitor!', 'classic', 'mild_insult')
a('হালা', 'hala', 'brother-in-law (Dhakaiya form)', 'Dhakaiya everyday form of শালা; in Old Dhaka oddly neutral, even affectionate', 'পুরান ঢাকায় অনাপত্তিজনক সম্বোধন', c, r, 'noun', 'dialect', 1, 'হালা, কী অবস্থা?', 'Hala, how are things?', 'classic', 'address|dialectal_neutral')
a('চটকাইলা', 'chotkaila', 'one who shows off', 'show-off, flashy person', 'বাহভাব দেখানো লোক', c, r, 'noun', 'street', 1, 'চটকাইলা বন্ধু পেয়েছি', 'I got a show-off friend', 'classic', 'mockery')
a('বাহিরের লোক', 'bahirer lok', 'outside person', 'outsider; not one of us', 'বাইরের লোক', c, r, 'phrase', 'dialect', 0, 'সে তো বাহিরের লোক', 'He is an outsider', 'classic', 'belonging')
a('গেলা', 'gela', 'he went', 'Dhakaiya "he/she went" — often for someone ruined or gone', 'চলে গেল; ব্যস্ত হইগে (ঢাকাইয়া)', c, r, 'verb', 'dialect', 0, 'সে গেলা রে, খবর নাই', 'He is gone, no news', 'classic', 'dialect_verb')
a('কাইদা', 'kaida', 'what/how', 'Dhakaiya "what"', 'কী (ঢাকাইয়া)', c, r, 'interrogative', 'dialect', 0, 'কাইদা বলিস, কী খাইবা?', 'Tell me what, what will you eat?', 'classic', 'question')
a('মইরা যামু', 'maira jamu', 'die and go', 'exaggerated despair: "I am dead!"', 'মরে যাব রে (কাতর ব্যঙ্গ)', c, r, 'phrase', 'street', 1, 'পরীক্ষা খারাপ দিলাম, মইরা যামু', 'Exam went bad, I am dead', 'classic', 'exaggeration')

# ================= 2. REGIONAL — CHATTOGRAM (চট্টগ্রামীয়া) =================
c, r = 'regional_chattogram', 'Chattogram'
a('কেন মামা লাগব', 'ken mama lagbe', 'why will uncle be needed', 'iconic Chittagonian retort: "why would I owe you that?" — meme of refusal', 'বিখ্যাত চট্টগ্রামীয়া প্রত্যাখ্যান-বাক্য', c, r, 'phrase', 'informal', 0, 'টাকা ধার চাইবি? কেন মামা লাগব!', 'Want a loan? Ken mama lagbe!', 'modern', 'meme|refusal')
a('তালে বাইয়া যাইর', 'tale baiya jair', 'holding hand, let\'s go', 'Chittagonian "let\'s go together"', 'চলো, হাত ধরে যাই', c, r, 'phrase', 'dialect', 0, 'তালে বাইয়া যাইর বাজারে', 'Let\'s go to the bazaar together', 'classic', 'invitation')
a('মাইগা', 'maiga', 'girl', 'girl (informal/derogatory in some contexts)', 'মেয়ে (অশিষ্ট)', c, r, 'noun', 'street', 2, 'ওই মাইগারে দেখ', 'Look at that girl', 'classic', 'informal_reference')
a('বাইনশা', 'bainsha', 'brother-in-law word', 'Chattogram form of শালা; common mild insult', 'চট্টগ্রামীয় হালকা গালি', c, r, 'noun', 'street', 2, 'বাইনশা, কই যাস?', 'Bainsha, where are you off to?', 'classic', 'mild_insult')
a('আইয়ার', 'aiyar', '?', 'good-for-nothing fellow (Chittagonian)', 'নিরেট অলস লোক', c, r, 'noun', 'street', 2, '', '', 'classic', 'insult')
a('গামছা', 'gamcha', 'towel/cloth', 'towel-slung local youth stereotype', 'গামছা ঘাড়ে দেওয়া স্থানীয় ছেলে-স্টেরিওটাইপ', c, r, 'noun', 'informal', 0, '', '', 'classic', 'stereotype')
a('কাইডা', 'kaida', 'what', 'Chittagonian "what" (same as Dhakaiya)', 'কী (চট্টগ্রামীয়া)', c, r, 'interrogative', 'dialect', 0, 'কাইদা কোস?', 'What are you saying?', 'classic', 'question')
a('বুঝির না', 'bujhir na', 'do not understand', 'Chittagonian "doesn\'t understand"', 'বোঝে না', c, r, 'phrase', 'dialect', 0, 'সে কিছুই বুঝির না', 'He understands nothing', 'classic', 'understanding')
a('পেটুইয়া', 'petuya', 'belly-ful', 'glutton (Chittagonian)', 'পেটুক লোক', c, r, 'noun', 'dialect', 1, '', '', 'classic', 'gluttony')
a('জাইগা নাই', 'jaiga nai', 'no place', '"no room for you here" — dismissal', 'জায়গা নেই — প্রত্যাখ্যান', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'dismissal')
a('চুদান্জি', 'chudanji', '(vulgar root)', 'Chittagonian vulgar compound; severe insult', 'চট্টগ্রামীয়া কঠোর গালি', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('বইঙে', 'boinge', '(vulgar root)', 'Chittagonian vulgar term for a person; severe', 'চট্টগ্রামীয়া গালি', c, r, 'noun', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('ওত্তার মাইরে বাপ', 'ottar mairé bap', '(vulgar compound)', 'severe Chittagonian curse invoking mother', 'মাতৃ-সংলগ্ন কঠোর গালি', c, r, 'phrase', 'vulgar', 3, '', '', 'classic', 'severe_profanity')
a('খেতা পুইত্তাম', 'kheta puittam', '(vulgar compound)', 'severe Chittagonian vulgar phrase', 'চট্টগ্রামীয়া গালি', c, r, 'phrase', 'vulgar', 3, '', '', 'classic', 'severe_profanity')

# ================= 3. REGIONAL — SYLHET (সিলেটি) =================
c, r = 'regional_sylhet', 'Sylhet'
a('কিতা', 'kita', 'what', 'Sylheti "what" — hallmark of the dialect', 'কী (সিলেটি)', c, r, 'interrogative', 'dialect', 0, 'কিতা খবর?', 'What\'s the news?', 'classic', 'question')
a('কিতা খবর', 'kita khobor', 'what news', 'Sylheti greeting: "what\'s up?"', 'কী খবর? (সিলেটি অভ্যর্থনা)', c, r, 'phrase', 'informal', 0, 'কিতা খবর বান্ধবী?', 'What\'s up, friend?', 'classic', 'greeting')
a('কিতা গরু মামা', 'kita goru mama', 'what, uncle cow', 'famous Sylheti exclamation of disbelief — "no way!"', 'বিখ্যাত সিলেটি অবিশ্বাস-বাক্য', c, r, 'phrase', 'informal', 1, 'কিতা গরু মামা, এক্কিবাক্কা পাস করেছো?', 'Kita goru mama, you actually passed?', 'modern', 'meme|disbelief')
a('বালে বালে', 'bale bale', 'speak-speak', '"say it, say it" — teasing chorus in Sylheti banter', 'বল বল — ঠাট্টার চোঁট', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'banter')
a('বিয়া', 'biya', 'wedding', 'Sylheti wedding (বিয়ে)', 'বিয়ে (সিলেটি উচ্চারণ)', c, r, 'noun', 'dialect', 0, 'বিয়ার খাবার মইয়া দিয়া খায়া ফালাইবেন', 'At the wedding you will eat to your fill', 'classic', 'culture')
a('খাইবাই দিয়া জাবো', 'khaibai diya jabu', 'eat-drink and go', 'Sylheti hospitality cliché — "have something before you leave"', 'খেয়ে-দেয়ে যাবে যে (আপ্যায়ন)', c, r, 'phrase', 'dialect', 0, '', '', 'classic', 'hospitality')
a('গুয়া', 'gua', 'areca nut', 'betel nut — Sylheti cultural marker', 'সুপারি (সিলেটি)', c, r, 'noun', 'dialect', 0, '', '', 'classic', 'culture')
a('কইরা দিমু', 'koira dimu', 'cut and give', '"I\'ll cut you up" — Sylheti mock-threat', 'কেটে দেব — মজার হুমকি', c, r, 'phrase', 'street', 2, '', '', 'classic', 'mock_threat')
a('মইয়া', 'moya', '(particle)', 'Sylheti emphatic particle/booster in jokes', 'সিলেটি জোর-দ্যোতক', c, r, 'particle', 'dialect', 0, '', '', 'classic', 'emphasis')
a('বুঝিলে মিয়া', 'bujhile miya', 'understood, mister', 'Sylheti confirmation with flair', 'বুঝেছো তো মিয়া', c, r, 'phrase', 'informal', 0, '', '', 'classic', 'confirmation')
a('আইজ কাল', 'aiz kal', 'today-tomorrow', 'day or two (Sylheti looseness about time)', 'আজ-কাল (সময়ের অনিশ্চয়তা)', c, r, 'phrase', 'dialect', 0, '', '', 'classic', 'time')
a('দুর কর', 'dur kor', 'throw away', 'Sylheti "get rid of it"', 'দূর করে দাও', c, r, 'phrase', 'dialect', 0, '', '', 'classic', 'command')
a('হামাগুড়ি', 'hamaguri', 'crawling', 'crawling on all fours (also dialect oath image)', 'হামাগুড়ি দেওয়া', c, r, 'noun', 'dialect', 0, '', '', 'classic', 'body')
a('এদ্দা', 'edda', 'this', 'Sylheti "this"', 'এটা (সিলেটি)', c, r, 'determiner', 'dialect', 0, '', '', 'classic', 'demonstrative')

# ================= 4. REGIONAL — OTHER (অন্য আঞ্চলিক) =================
c, r = 'colloquial_dialectal', 'Noakhali / Barishal / Rangpur / Khulna / Mymensingh / Kolkata'
a('হালাম', 'halam', 'brother-in-law word', 'Noakhali/Faridpur-eastern form; everyday mild call in some eastern dialects, insult in others', 'পূর্বাঞ্চলীয় সম্বোধন/হালকা গালি', c, r, 'noun', 'dialect', 2, '', '', 'classic', 'dialect_insult')
a('ইতর', 'itor', 'lowborn', 'contemptuous: uncultured wretch (Cumilla region use: outsider)', 'নিকৃষ্ট; চট্টগ্রামাঞ্চলে বাইরের লোক বোঝাতে', c, r, 'adjective', 'street', 2, 'ইতর লোক!', 'You wretch!', 'classic', 'class_insult')
a('মাইয়া লাও', 'maiya lao', 'take it (Noakhali)', 'Noakhali emphatic "here, take it!"', 'নাও (নোয়াখালীয়া)', c, r, 'phrase', 'dialect', 0, '', '', 'classic', 'offer')
a('হাইরে', 'haire', 'oh dear', 'Mymensingh-style exclamation of dismay', 'হায় রে! (ময়মনসিংহীয়)', c, r, 'interjection', 'dialect', 0, '', '', 'classic', 'exclamation')
a('কেন বাপ', 'ken bap', 'why, father', 'Barishal-style incredulous address', 'কেন বাপ? (বরিশালীয়া বিস্ময়)', c, r, 'phrase', 'dialect', 0, '', '', 'classic', 'disbelief')
a('মুই', 'mui', 'I', 'regional "I" (Mymensingh/Noakhali)', 'আমি (আঞ্চলিক)', c, r, 'pronoun', 'dialect', 0, '', '', 'classic', 'pronoun')
a('চুদুর বুদুর', 'chudur budur', '(rhyming slang)', 'nonsense syllables; parliamentary slang for vulgar chatter (famous Speaker ruling)', 'সংসদে আলোচিত বিদ্রূপাত্মক অর্থহীন শব্দযুগল', c, r, 'noun', 'informal', 2, '', '', 'classic', 'parliamentary_meme')
a('মোসাই', 'mosai', 'master (Kolkata)', 'Kolkata colloquial: boss, master (often ironic)', 'কলকাতার বস সম্বোধন', c, r, 'noun', 'informal', 0, '', '', 'classic', 'kolkata')
a('প্যাঁচ খাওয়া', 'pyech khaoa', 'eat a coil', 'to get entangled in someone\'s trickery', 'চালাকিতে জটিল ফাঁদে পড়া', c, r, 'phrase', 'informal', 1, '', '', 'classic', 'trickery')

json.dump(E, open('/home/z/my-project/bangla-slang-dataset/data/raw/gold_part1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('part1 entries:', len(E))
from collections import Counter
print(Counter(e['category'] for e in E))
