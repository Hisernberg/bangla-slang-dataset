#!/usr/bin/env python3
"""v3.2 gold addendum: anglicism_borrowings — 30 new master entries (KS-3288..).
Bangla-script anglicisms in live 2024-26 BD usage, not yet in master. Full 20-field schema."""

import json

def E(term_bn, roman, lit, en, bn, pos, reg, off, ex_bn, ex_en, era, tags, pop):
    return {"term_bn": term_bn, "romanization": roman, "literal_meaning": lit,
            "meaning_en": en, "meaning_bn": bn, "category": "anglicism_borrowings",
            "region": "Nationwide (social media)", "part_of_speech": pos, "register": reg,
            "offensiveness": str(off), "usage_example_bn": ex_bn, "usage_example_en": ex_en,
            "era": era, "tags": tags, "popularity": str(pop), "confidence": "high",
            "tier": "1", "source_type": "gold_curated_v32",
            "source_url": "https://github.com/Hisernberg/bangla-slang-dataset"}

ENTRIES = [
E("রিজ","rizz","charisma","romantic charm and game; the skill of winning someone over","রোমান্টিক আকর্ষণ-কৌশল; কারও মন জয়ের দক্ষতা","noun","very informal",0,"রিজ লেভেল নিয়ে এখন গ্রুপে টুর্নামেন্ট চলে","Rizz-level tournaments now run in our group chat","2023-2026","anglicism,genz,romance",5),
E("ডেলুলু","delulu","delusional","self-aware delusional hope, esp. about a crush","আত্মমগ্ন বাতিক-আশাবাদ, বিশেষত ক্রাশ নিয়ে","adjective","very informal",0,"এক রিপ্লাই পেয়েই পুরো ডেলুলু হয়ে গেছে","One reply and he's fully delulu","2023-2026","anglicism,genz,romance",4),
E("মিড","mid","mediocre","disappointingly average despite the hype","হাইপ সত্ত্বেও মোটামুটি-পর্যায়ের বাজে অভিজ্ঞতা","adjective","very informal",1,"সবাই প্রশংসা করে, সিরিজটা কিন্তু পুরো মিড","Everyone praised it, but the series is pure mid","2022-2026","anglicism,genz,review",5),
E("নো ক্যাপ","no cap","no lie","emphatic 'I'm not lying / for real'","জোর দিয়ে বলা 'মিথ্যা বলছি না'","phrase","very informal",0,"চাটগাঁইয়া বিরিয়ানিটা সেরা, নো ক্যাপ","The Chittagong biryani is the best, no cap","2022-2026","anglicism,genz",5),
E("ক্যাপ মারা","cap mara","to cap","to lie or make a fake claim (ক্যাপ = lie)","মিথ্যা বলা বা জাল দাবি করা","verb phrase","very informal",1,"স্ক্রিনশট আছে, তুই ক্যাপ মারিস না ভাই","I have the screenshot, don't cap bro","2022-2026","anglicism,genz,verbalized",4),
E("লকড ইন","locked in","locked in","fully focused, locked onto a goal","পুরো মন দিয়ে লক্ষ্যে আটকে যাওয়া","adjective","very informal",0,"ফাইনালের আগের রাতে পুরো লকড ইন","Fully locked in the night before finals","2023-2026","anglicism,genz,campus",4),
E("কুকিং করা","cooking kora","cooking","doing something impressive; 'let him cook' = let him work","দুর্দান্ত কিছু করে যাওয়া; 'চালাতে দাও' অর্থে","verb phrase","very informal",0,"ভাই একটা স্ট্র্যাটেজি বানাইতেছে, কুক করতে দাও","He's building a strategy, let him cook","2023-2026","anglicism,gaming,genz",4),
E("ওপি","OP","overpowered","too strong to be fair (game move, player, even a song's beat)","অতিরিক্ত শক্তিশালী, অন্যায্য রকম ভালো","adjective","very informal",0,"এই গানের সিনথ-লাইনটা সত্যিই ওপি","That synth line is genuinely OP","2020-2026","anglicism,gaming,music",5),
E("গোটেড","goated","goated","legendary, greatest of all time","সর্বকালের সেরা, কিংবদন্তি","adjective","very informal",0,"টেবিল টেনিসে ক্যান্টিন মামা পুরো গোটেড","Canteen mama is goated at table tennis","2022-2026","anglicism,gaming,sports",3),
E("এনপিসি ভাইব","NPC baib","NPC vibe","behaving like a background character: same responses, no originality","দর্শক-চরিত্রের মতো আচরণ: একঘেয়ে, নিজস্বতা-শূন্য","noun phrase","very informal",1,"সব ট্রেন্ডে একই কমেন্ট-পুরো এনপিসি ভাইব","Same comment on every trend—pure NPC vibe","2023-2026","anglicism,meme,gaming",3),
E("সিগমা মালে","sigma male","sigma male","ironic lone-wolf grind persona","রসিক অর্থে একাকী কঠোর-পরিশ্রমী পুরুষ-ভাব","noun phrase","very informal",1,"পার্টিতে না গিয়ে জিমে-সিগমা মালে মোড","Skipping parties for the gym—sigma male mode","2022-2026","anglicism,genz,meme",4),
E("অরা পয়েন্ট","aura point","aura point","invisible coolness points gained/lost by actions","কাজের ভিত্তিতে বাড়া-কমা অদৃশ্য ক্যারিশমা-পয়েন্ট","noun phrase","very informal",0,"লেট হয়ে ঢুকে দুধ উল্টে মাইনাস একশো অরা পয়েন্ট","Late entry plus spilled milk: minus hundred aura points","2024-2026","anglicism,genz,meme",3),
E("ব্রেইনরট","brainrot","brainrot","internet content that melts your brain; also the meme-language it creates","মাথা গলিয়ে দেওয়া ইন্টারনেট-কনটেন্ট; সেই মিম-ভাষাও","noun","informal",0,"রাত তিনটা পর্যন্ত ব্রেইনরট রিলস দেখছি","Watching brainrot reels till 3am","2023-2026","anglicism,internet,genz",4),
E("রেশিও খাওয়া","ratio khaoa","to eat a ratio","getting ratioed: replies dunk on your post harder than the post itself","পোস্টের চেয়ে উল্টো জবাব বেশি ভাইরাল হয়ে মার খাওয়া","verb phrase","very informal",1,"বোকা পোস্ট করে পুরো রেশিও খেয়েছে","Posted something dumb and got ratioed hard","2022-2026","anglicism,social_media,verbalized",3),
E("রেড ফ্ল্যাগ","red flag","red flag","warning sign in someone's character, esp. dating","চরিত্রের বিপদ-সংকেত, বিশেষত সম্পর্কে","noun phrase","informal",0,"প্রথম কথাতেই পুরো রেড ফ্ল্যাগ","Full red flag from the very first chat","2021-2026","anglicism,romance,genz",5),
E("গ্রিন ফ্ল্যাগ","green flag","green flag","good sign: considerate, safe, emotionally mature","ভালো লক্ষণ: বিবেচক, নিরাপদ, আবেগগতভাবে পরিণত","noun phrase","informal",0,"মন খারাপ বুঝে কল দেয়-খাঁটি গ্রিন ফ্ল্যাগ","Calls when you're down—true green flag","2021-2026","anglicism,romance,genz",4),
E("ইক খাওয়া","ick khaoa","catch the ick","sudden turn-off from one small behavior","একটা ছোট আচরণেই হঠাৎ বিরক্তি-ঘৃণা লেগে যাওয়া","verb phrase","informal",0,"চুইংগাম খুলে ফেলাতেই ইক খেয়ে গেলাম","He spat the gum out and I caught the ick","2022-2026","anglicism,romance,verbalized",3),
E("বেঞ্চিং","benching","benching","keeping someone on the bench as a backup option","কাউকে বিকল্প-খেলোয়াড় হিসেবে সাইডে রাখা","noun","informal",1,"উত্তর দেয় কিন্তু প্ল্যান নেয় না-খাঁটি বেঞ্চিং","Replies but never plans—classic benching","2021-2026","anglicism,romance",4),
E("ব্রেডক্রাম্বিং","breadcrumbing","breadcrumbing","dripping tiny bits of attention to keep someone hooked","আঁটড়ে রাখতে মুঠো-মুঠো মনোযোগ ফেলা","noun","informal",1,"রাত দুইটায় 'ঘুমাচ্ছ?'-খাঁটি ব্রেডক্রাম্বিং","2am 'you up?' texts—pure breadcrumbing","2021-2026","anglicism,romance",3),
E("সিচুয়েশনশিপ","situationship","situationship","undefined romance stuck between friendship and commitment","বন্ধুত্ব ও সম্পর্কের মাঝখানে আটকে থাকা অস্পষ্ট রোম্যান্স","noun","informal",0,"দুই বছর সিচুয়েশনশিপ, স্ট্যাটাস এখনো এম্পটি","Two years of situationship, status still empty","2021-2026","anglicism,romance,genz",5),
E("লাভ বম্বিং","love bombing","love bombing","overwhelming affection used to control someone","নিয়ন্ত্রণের জন্য ভালোবাসার বোমাবর্ষণ","noun","informal",1,"এক সপ্তাহে তিনশ মেসেজ-খাঁটি লাভ বম্বিং","Three hundred texts in a week—love bombing","2022-2026","anglicism,romance",3),
E("শিপ করা","ship kora","to ship","to root for a romantic pairing (people or fictional)","জোড়াকে (মানুষ বা কাল্পনিক) একসাথে দেখতে চাওয়া","verb phrase","informal",0,"এই দুই চরিত্রকে আমি পুরো শিপ করি","I totally ship these two characters","2020-2026","anglicism,fandom,verbalized",4),
E("ম্যানিফেস্ট করা","manifest kora","to manifest","to will a goal into existence by focused belief","একাগ্র বিশ্বাসে কিছু বাস্তবায়নের চেষ্টা করা","verb phrase","informal",0,"পড়ার বদলে রেজাল্ট ম্যানিফেস্ট করছে","Manifesting results instead of studying","2022-2026","anglicism,genz,verbalized",4),
E("গ্যাসলাইট করা","gaslight kora","to gaslight","to manipulate someone into doubting their own memory/reality","কাউকে তার নিজের স্মৃতি-বাস্তবতা নিয়ে সন্দেহে ফেলা","verb phrase","informal",1,"'তুমি নিজেই বলেছিলে' বলে পুরো গ্যাসলাইট করছে","'You said it yourself'—full gaslighting","2022-2026","anglicism,romance,workplace,verbalized",4),
E("গেটকিপ করা","gatekeep kora","to gatekeep","to withhold a gem (place, song, tip) to keep it exclusive","স্বতন্ত্র রাখতে দুর্লভ জিনিস (জায়গা/টিপস) গোপন রাখা","verb phrase","informal",0,"এই চা-স্টলের লোকেশন এতদিন গেটকিপ করেছিলে?","You gatekept this tea-stall location for months?","2022-2026","anglicism,genz,verbalized",3),
E("ট্রমা ডাম্প","trauma dump","trauma dump","suddenly unloading a heavy personal story on someone","হঠাৎ ভারী ব্যক্তিগত দুঃখের গল্প ঢেলে দেওয়া","noun","informal",1,"প্রথম মিটিংতেই পুরো জীবনী-খাঁটি ট্রমা ডাম্প","Whole life story at the first meeting—trauma dump","2022-2026","anglicism,genz",3),
E("রোমান এম্পায়ার","roman empire","roman empire","a topic you think about constantly (from the meme)","প্রায়ই ভাবতে থাকা বিষয় (মিম-উৎস)","noun phrase","very informal",0,"৯৭-এর ক্রিকেট সিরিজ আমার রোমান এম্পায়ার","The '97 cricket series is my roman empire","2023-2026","anglicism,meme,genz",2),
E("টাচ গ্রাস","touch grass","touch grass","'log off and go outside' retort to over-online behavior","অতিরিক্ত অনলাইন আচরণের জবাবে 'বাইরে যাও'","phrase","very informal",1,"সারাদিন র‍্যাংক পুশ? ভাই টাচ গ্রাস মার","Rank-pushing all day? Touch grass bro","2022-2026","anglicism,gaming,genz",4),
E("ক্রনিকলি অনলাইন","chronically online","chronically online","so internet-brained that real life feels alien","চরম ইন্টারনেট-ব্যাধিতে বাস্তব জীবন অচেনা মনে হওয়া","adjective","informal",1,"রিয়েল লাইফে লাইক-কাউন্ট করে-ক্রনিকলি অনলাইন","Counts likes in real life—chronically online","2022-2026","anglicism,internet,genz",3),
E("ডুমস্ক্রল","doomscroll","doomscroll","endless scrolling through distressing feeds","অস্বস্তিকর ফিডে অন্তহীন স্ক্রল করা","verb","informal",0,"রাত তিনটা পর্যন্ত ডুমস্ক্রল, সকালে দুঃখ","Doomscrolled till 3am, regret by morning","2021-2026","anglicism,internet,genz",4),
E("ফোমো খাওয়া","fomo khaoa","to eat FOMO","suffering the fear of missing out on an event/plan","অনুষ্ঠান-পরিকল্পনা মিস করার ভয়ে ভোগা","verb phrase","informal",0,"গ্রুপ ট্যুরে না গিয়ে ফোমো খেলাম","Skipped the group tour and ate full FOMO","2020-2026","anglicism,genz,verbalized",4),
]

if __name__ == "__main__":
    json.dump(ENTRIES, open("/home/z/my-project/harvest_v31/gold_v32.json", "w"), ensure_ascii=False, indent=1)
    print(f"gold_v32: {len(ENTRIES)} entries -> harvest_v31/gold_v32.json")
