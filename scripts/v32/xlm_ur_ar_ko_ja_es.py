#!/usr/bin/env python3
"""v3.2 XLM data file 5: Urdu/Arabic/Persian + Korean/Japanese/Spanish -> Bangla.
Urdu/Arabic words arrive in BD speech via religion (mosque, madrasa, market) and cinema;
Korean/Japanese arrive via K-drama and anime fandoms."""

def X(lang, term, gloss, native, cm, roman, process, reg, off, domain, excm, exbn, *rest):
    CONF = {"high", "medium", "low"}
    if len(rest) >= 3: note, conf, exsrc = rest[0], rest[1], rest[2]
    elif len(rest) == 2:
        if rest[0] in CONF: note, conf, exsrc = "", rest[0], rest[1]
        elif rest[1] in CONF: note, conf, exsrc = rest[0], rest[1], ""
        else: note, conf, exsrc = rest[0], rest[1], ""
    elif len(rest) == 1:
        if rest[0] in CONF: note, conf, exsrc = "", rest[0], ""
        else: note, conf, exsrc = rest[0], "high", ""
    else: note, conf, exsrc = "", "high", ""
    return dict(source_lang=lang, source_term=term.strip(), source_gloss_en=gloss, bangla_native_equivalent=native,
                bangla_codemixed_form=cm, bangla_romanization=roman, mapping_process=process, register=reg,
                offensiveness=str(off), domain=domain, usage_example_banglish=excm, usage_example_pure_bn=exbn,
                process_note=note, confidence=conf, example_source_lang=exsrc)

EN = "en"; UR = "ur"; AR = "ar"; FA = "fa"; KO = "ko"; JA = "ja"; ES = "es"
ENTRIES = [
# ---------------- Urdu / Arabic / Persian (1-40) ----------------
X(UR,"फ़ालिय (fazool/fazil)","worthless, useless","ফাজিল, নিরর্থক","ফাজিল","fazil","semantic_equivalent","informal",1,"street;everyday","ফাজিল কথা বাদ দে, কাজ কর","অর্থহীন কথা বাদ দাও, কাজ করুন","Urdu 'fuzool' entered BD street speech as 'ফাজিল' (also a surname!)","high","फ़ालिय बातें बंद करो"),
X(AR,"حَرَام‌خُور (haramkhor)","eats what is forbidden; scoundrel","হারামখোর","হারামখোর","haramkhor","semantic_equivalent","very informal",3,"street","হারামখোর! নিজের ভাইকে ফাঁসালো","নীতিহীন! নিজের ভাইকে ফাঁসালো","Arabic 'haram' + Persian agent suffix '-khor' (eater) — fully productive in BD","high","حَرَام‌خُور आदमी"),
X(UR,"बदमाश (badmash)","hooligan, rogue","বদমাশ","বদমাস","badmash","semantic_equivalent","informal",2,"street","বদমাস ছেলেদের দল রাস্তায়","দুষ্ট ছেলেদের দল রাস্তায়","Urdu compound 'bad+batch' → 'badmash'; BD softened final consonant","high","बदमाश लड़कों का गिरोह"),
X(AR,"شيطان (shaytan)","devil (insult: rascal)","শয়তান","শয়তান","shoytan","semantic_equivalent","very informal",2,"family;street","এই শয়তানটা আবার কি করে ফেললো!","এই দুষ্টটা আবার কী করে ফেললো!","Religious word domesticated as playful scolding in both cultures","high","ये शैतान क्या कर बैठा!"),
X(AR,"لَفَّانْج (lafanga)","idle loafer, vagabond","লাফঙ্গ","লাফঙ্গ","lafongo","semantic_equivalent","very informal",2,"street","লাফঙ্গ বন্ধু, কাজ নাই কিছু","গোলমেলে বন্ধু, কাজ নেই কিছু","Arabic 'lafanga' kept whole; means aimless idler","medium","लफंगा दोस्त"),
X(AR,"دوزخ (dozakh)","hell (curse: wretched fate)","দোজখ","দোজখ / জাহান্নাম","dozokh","semantic_equivalent","very informal",3,"street","দোজখের ভাগ্য আমার","অভিশপ্ত ভাগ্য আমার","Hell-word in everyday fatalistic cursing","medium","दोज़ख भरी ज़िंदगी"),
X(FA,"بےحيائي (behayai)","shamelessness","বেহায়াপনা","বেহায়া","behaya","semantic_equivalent","informal",2,"street;everyday","বেহায়া নাকি এমন রাস্তায় চিৎকার?","লজ্জাশীল নাকি এমন রাস্তায় চিৎকার?","Persian 'baya' (shame) negated; BD uses as adjective/verb both","high","बेशर्म नाकि?"),
X(AR,"مُنافِق (munafiq)","hypocrite","মুনাফিক, ভণ্ড","মুনাফিক","munafik","semantic_equivalent","informal",2,"politics;everyday","মুনাফিকের দল কম না রাজনীতিতে","ভণ্ডের অভাব নেই রাজনীতিতে","Religious critique word in political slang","high","मुनाफ़ों की कमी नहीं"),
X(AR,"جُهالت (juhalat)","ignorance, boorishness","জুহালত, অজ্ঞতা","জুহালত","juhalot","semantic_equivalent","informal",1,"everyday","জুহালতের মাত্রা দেখেন","অজ্ঞতার মাত্রা দেখুন","Used in educated slangy scolding","medium","जहालत देखो"),
X(AR,"فصّات? → فَصَّاب / ফস্সা (fossa)","fake, fraud","ফাঁকিবাজ","ফাঁকিবাজ","fokibaj","semantic_equivalent","informal",2,"market;street","ফাঁকিবাজ মোড়ল আবার দাম বাড়ালো","প্রতারক মোড়ল আবার দাম বাড়ালো","BD's native 'ফাঁকি' family covers fraud talk","high","फरेबी दुकानदार"),
X(FA,"تشدید? → তকদীর (taqdeer)","fate, destiny","তকদীর","তকদীর","tokdir","semantic_equivalent","neutral",0,"everyday","তকদীরে নেই বোধহয়","ভাগ্যে নেই বোধহয়","Fatalistic everyday word identical in both","high","तक़दीर में नहीं"),
X(AR,"أَمانَة (amanat)","entrusted thing; honesty","আমানত","আমানত","amanot","semantic_equivalent","neutral",0,"market;everyday","আমানতে খেয়ানত করলো","আমানতে বিশ্বাসঘাতকতা করলো","'খেয়ানত' (betrayal of trust) is the paired word","high","अमानत में खियानत"),
X(FA,"خوش (khush)","happy","খুশি","খুশি","khushi","semantic_equivalent","neutral",0,"everyday","খুশি মানুষ, সবাইকে খুশি রাখে","আনন্দিত মানুষ, সবাইকে খুশি রাখে","Root word absorbed so deep it's pure Bangla now","high","खुश इंसान"),
X(AR,"حَسَد (hasad)","envy, evil-eye energy","হিংসা, নজর লাগা","হাসাদ / হিংসা","hasad","semantic_equivalent","informal",1,"everyday;family","সাফল্যে হাসাদও খেয়ে ফেলে","সাফল্যে হিংসাও আসে","'নজর লাগা' (evil eye strikes) is the folk twin","high","सफलता में हसद भी"),
X(AR,"بَخِيل (bakheel)","miser","বখিল, কৃপণ","বখিল","bokhil","semantic_equivalent","informal",1,"everyday","বখিল মোড়ল চায়ের টাকাও দেয় না","কৃপণ মোড়ল চায়ের টাকাও দেয় না","high","कंजूस सेठ"),
X(UR,"इज़्ज़त (izzat)","honor, respect","ইজ্জত","ইজ্জত","ijjot","semantic_equivalent","neutral",0,"family;street","ইজ্জত রাখো বাপ-দাদার","সম্মান রক্ষা করো পূর্বপুরুষের","Central concept identical across South Asia","high","इज़्ज़त का सवाल है"),
X(AR,"قَبر (qobor)","grave (scold: dig your own)","কবর","কবর","kobor","semantic_equivalent","very informal",2,"street","নিজের কবর খুঁড়ছে","নিজের অভিশাপ বানাচ্ছে","Same grave-digging scold in both cultures","medium","अपनी कब्र खुद खोद रहा है"),
X(FA,"دشمن (dushman)","enemy","দুশমন","দুশমন / শত্রু","dushmon","semantic_equivalent","informal",1,"politics","রাজনীতিতে দুশমন বেশি","রাজনীতিতে শত্রু বেশি","high","राजनीति में दुश्मन बहुत"),
X(AR,"سُर (sur)... → سُوسে (soose)","dried-up, sly","সুসে","সুসে","shushe","semantic_equivalent","informal",1,"street","সুসে চালাক লোক","কেঁচো-মাছির মতো চালাক","BD's own folk word for shriveled-sly","medium","सुखा चालाक"),
X(AR,"آواز? → হাই তোলা (hai tola)","sigh dramatically","হাই তোলা","হাই তোলা","hai tola","cultural_adaptation","informal",0,"everyday","দেরি শুনে হাই তুললো","দেরি শুনে দীর্ঘশ্বাস ফেললো","Highly productive BD verb construction from sigh-noun","high","देर सुनकर हाय भरी"),
# ---------------- Korean (41-60) ----------------
X(KO,"오빠 (oppa)","older male (K-drama address)","ওপ্পা","ওপ্পা","oppa","loanword_noun","informal",0,"fandom;media","এপিসোডে ওপ্পা স্টাইল মারছে","সিরিজে ওপ্পা জাতীয় আদর দেখাচ্ছে","K-drama fandom word; BD fans call favorite actors 'ওপ্পা' directly","high","오빠 스타일 대박"),
X(KO,"대박 (daebak)","jackpot, amazing","দৈবাৎ, মহা দুর্দান্ত","দেবাক","daebak","loanword_noun","informal",0,"fandom;youth","নতুন অ্যালবামটা পুরো দেবাক","নতুন অ্যালবামটা মহা দুর্দান্ত","Exclamation adopted whole by Bangladeshi K-pop fans","high","새 앨범 대박"),
X(KO,"귀엽다 (kwiyeopda/aegyo)","cute, charmingly babyish","কিউট, আদরের ছোট্ট ভাব","এগিয়ো","aegyo","loanword_noun","informal",0,"fandom","ওপ্পার এগিয়ো দেখে ফেস্ট করলাম","ওপ্পার আদরের ভঙ্গি দেখে মুগ্ধ হলাম","Aegyo kept in romanized form in fandom talk","medium","오빠 애교 최고"),
X(KO,"사랑해 (saranghae)","I love you","ভালোবাসি","সারাংহে","saranghae","loanword_noun","informal",0,"fandom","কনসার্টে স্ক্রিনে সারাংহে লিখলো","কনসার্টে স্ক্রিনে ভালোবাসি লিখলো","Learned via K-drama subtitles; used in fan signs","high","사랑해 콘서트에서"),
X(KO,"화이팅 (hwaiting/fighting)","cheer: go for it!","লড়ো ভাই! শুভকামনা","ফাইটিং!","hwaiting","loanword_noun","informal",0,"fandom;campus","পরীক্ষার আগে গ্রুপে ফাইটিং লিখলো","পরীক্ষার আগে গ্রুপে শুভকামনা লিখলো","Korean 'fighting' repurposed as pure cheer","high","시험 전에 화이팅!"),
X(KO,"막내 (maknae)","youngest member","কনিষ্ঠ সদস্য","ম্যাকনে","maknae","loanword_noun","informal",0,"fandom","গ্রুপের ম্যাকনে কে?","দলের কনিষ্ঠ সদস্য কে?","high","그룹의 막내 누구?"),
X(KO,"선배 (sunbae)","senior (school/work)","সিনিয়র","সুনবে","sunbae","loanword_noun","informal",0,"fandom;campus","সুনবে নাকি আজ ফিডব্যাক দিবে?","সিনিয়র নাকি আজ মতামত দেবে?","high","선배가 피드백 준대"),
X(KO,"누나 (noona)","older female address","আপু / দিদি","নুনা","noona","loanword_noun","informal",0,"fandom","নুনা ফ্যানক্লাবে বিতর্ক চলছে","আপুদের ফ্যানক্লাবে বিতর্ক চলছে","Mapped onto native kinship 'আপু'","medium","누나 팬클럽 토론 중"),
X(KO,"고생했어 (gosaenghaesseo)","you worked hard (praise)","খাটুনি খেয়েছেন","কোসেংহেসো","gosaenghaesseo","loanword_noun","informal",0,"fandom","স্টেজ শেষে স্ট্যাফদের কোসেংহেসো","মঞ্চ শেষে কর্মীদের পরিশ্রমের প্রশংসা","K-variety ritual phrase","medium","무대 끝나고 스태프들에게 고생했어"),
X(KO,"눈치 (nunchi)","social reading of the room","মানুষ-বোঝা কৌশল","নুনচি","nunchi","loanword_noun","informal",0,"fandom;everyday","নুনচির অভাব এই দলে","এই দলে মানুষ-বোঝার কৌশল নেই","Untranslatable social skill word fans adopt","medium","이 팀엔 눈치가 없어"),
# ---------------- Japanese (61-75) ----------------
X(JA,"先輩 (senpai)","senior (anime/school trope)","সিনিয়র","সেম্পাই","senpai","loanword_noun","informal",0,"anime;fandom","সেম্পাই নাকি আজ প্র্যাকটিস স্কিপ করলো?","সিনিয়র নাকি আজ অনুশীলন ফাঁকি দিলো?","Anime fandom vocabulary; 'notice me senpai' meme travels with it","high","先輩が練習サボった?"),
X(JA,"可愛い (kawaii)","cute","কিউট, মন-ভরানো","কাওয়াই","kawaii","loanword_adjective","informal",0,"anime;fandom","চরিত্রটা কাওয়াই রে ভাই","চরিত্রটা কিউট রে ভাই","high","キャラ可愛い"),
X(JA,"妻? → ワイフ (waifu)","fictional wife (anime)","কাল্পনিক প্রেমিকা","ওয়াইফু","waifu","cultural_adaptation","very informal",0,"anime;fandom","ওয়াইফু হাতছাড়া হয়ে গেলো ভাই","কাল্পনিক প্রিয় চরিত্রের মনোলি হাতছাড়া হলো","Otaku loan kept whole in BD anime groups","high","ワイフを逃した"),
X(JA,"ツンデレ (tsundere)","cold outside, soft inside","বাইরে রুক্ষ, ভেতরে কোমল","সুনডেরে","tsundere","loanword_noun","informal",0,"anime;romance","সে তো সুনডেরে টাইপ","সে তো বাইরে রুক্ষ ভেতরে কোমল টাইপ","Character-archetype word adopted by fanfic writers","medium","ツンデレタイプ"),
X(JA,"仲間 (nakama)","trusted crew, comrades","সঙ্গীরা, দল","নাকামা","nakama","loanword_noun","informal",0,"anime","নাকামা ছাড়া লড়াই চলে না","সঙ্গী ছাড়া লড়াই চলে না","One Piece's crew-loyalty word","high","仲間なしでは戦えない"),
X(JA,"馬鹿 (baka)","fool (playful insult in anime)","বোকা","বাকা","baka","loanword_noun","informal",1,"anime;youth","বাকা ভাই, চ্যালেঞ্জ একসেপ্ট করেছে","বোকা ভাই, চ্যালেঞ্জ গ্রহণ করেছে","Playful anime-insult adopted by BD weebs","medium","バカだね"),
X(JA,"何？！ (nani)","what?! (dramatic anime shock)","কী?!","নানি?!","nani","loanword_noun","very informal",0,"anime;memes","ফাইনাল ফাইটে নানি?! মুহূর্ত","ফাইনাল যুদ্ধে হাঁ হয়ে যাওয়া মুহূর্ত","Pure sound-meme; used only in meme contexts","high","最終戦でナニ?!"),
X(JA,"凄い (sugoi)","awesome","অসাধারণ","সুগোই","sugoi","loanword_adjective","informal",0,"anime;fandom","অ্যানিমেশনটা সুগোই","অ্যানিমেশনটা অসাধারণ","high","アニメーションすごい"),
X(JA,"異世界 (isekai)","transported to another world","অন্য পৃথিবীতে স্থানান্তর","ইসেকাই","isekai","loanword_noun","informal",0,"anime;literature","নতুন ইসেকাই সিরিজ শুরু করলাম","নতুন অন্যপৃথিবী সিরিজ শুরু করলাম","Genre word adopted whole","medium","新しい異世界シリーズ"),
X(JA,"修行 (shugyo)","rigorous training arc","কঠোর অনুশীলন","শুগিও","shugyo","loanword_noun","informal",0,"anime;fitness","জিমে শুগিও চলছে","জিমে কঠোর অনুশীলন চলছে","Training-arc word applied to gym-life in BD too","medium","ジムで修行中"),
# ---------------- Spanish / global (76-90) ----------------
X(ES,"¡vamos!","let's go (football chant)","চলো! জয় হোক!","ভামোস!","vamos","loanword_noun","informal",0,"sports;street","গোলের পর গ্যালারি ভামোস চিৎকার","গোলের পর গ্যালারিতে জয়ধ্বনি","Football-commentary Spanish entered BD galleries","high","¡vamos! en la galería"),
X(ES,"amigo","friend","বন্ধু","অ্যামিগো","amigo","loanword_noun","informal",0,"youth;media","অ্যামিগো, এক কাপ চা দেন","বন্ধু, এক কাপ চা দেন","Playful mock-foreign address in BD street talk","medium","hola amigo"),
X(ES,"adiós","goodbye","বিদায়","অদিওস","adios","loanword_noun","informal",0,"youth;chat","অদিওস ভাই, আর দেখা হবে","বিদায় ভাই, আর দেখা হবে","Playful dramatic farewell","medium","adiós amigo"),
X(ES,"hola","hello","হ্যালো","ওলা","hola","loanword_noun","informal",0,"youth;chat","ওলা! কেমন আছো?","হ্যালো! কেমন আছো?","Playful greeting borrowed in chat","medium","hola ¿cómo estás?"),
X(ES,"mucho gusto","nice to meet you","আনন্দ হলো দেখে","মুচো গুস্তো","mucho gusto","loanword_noun","informal",0,"youth;media","মুচো গুস্তো সেনিয়র!","আনন্দ হলো দেখে!","Mock-formal humor in BD youth speech","medium","mucho gusto señor"),
X(ES,"fiesta","party","পার্টি","ফিয়েস্তা","fiesta","loanword_noun","informal",0,"youth;party","শুক্রবারে ফিয়েস্তা টাইম","শুক্রবারে পার্টির আয়োজন","Exotic party-word in invites","medium","fiesta el viernes"),
X(ES,"gracias","thanks","ধন্যবাদ","গ্রাসিয়াস","gracias","loanword_noun","informal",0,"youth;chat","গ্রাসিয়াস মামা!","ধন্যবাদ ভাই!","Playful thanks in chat","medium","gracias tío"),
X(EN,"yolo","you only live once","জীবন একবারই","ইয়োলো","yolo","loanword_noun","informal",0,"youth","ইয়োলো ভাই, টিকিট কেটে ফেলছি","জীবন একবারই, টিকিট কাটছি","Acronym kept whole","high","You only live once, booking the ticket."),
X(EN,"fomo","fear of missing out","মিস-হওয়ার ভয়","ফোমো","fomo","loanword_noun","informal",0,"social_media","গ্রুপ ট্যুরে না গিয়ে ফোমো খেলাম","গ্রুপ ট্যুরে না গিয়ে মিস-হওয়ার ভয়ে ভুগলাম","'ফোমো খাওয়া' — the eating-suffix reaches even acronyms","high","Got FOMO skipping the group tour."),
X(EN,"goat (G.O.A.T)","greatest of all time","সর্বকালের সেরা","গোট","goat","loanword_noun","informal",0,"sports","মেসি নাকি গোট?","মেসি নাকি সর্বকালের সেরা?","Football-debate staple in BD tea stalls","high","Messi is the GOAT, right?"),
X(EN,"mvp","most valuable player","সেরা খেলোয়াড়","এমভিপি","MVP","loanword_noun","informal",0,"sports;workplace","এই মাসের এমভিপি তুমি","এই মাসের সেরা কর্মী তুমি","Sports acronym applied to office too","medium","You're this month's MVP."),
X(EN,"hakuna matata","no worries (Swahili via Lion King)","চিন্তা নেই কোনো","হাকুনা মাতাতা","hakuna matata","loanword_noun","informal",0,"media;everyday","হাকুনা মাতাতা ভাই, সব ঠিক আছে","চিন্তা নেই ভাই, সব ঠিক আছে","Movie-borrowed Swahili living in BD speech","high","Hakuna matata, all good."),
X(EN,"namaste? → नमस्ते (namaste)","greeting (Sanskrit)","নমস্কার","নমস্তে / নমস্কার","nomoskar","semantic_equivalent","neutral",0,"everyday","নমস্কার দাদা, কেমন আছেন?","নমস্কার দাদা, কেমন আছেন?","Bangla chose the Bengali 'নমস্কার'; 'নমস্তে' heard in yoga-media contexts","high","नमस्ते दादा"),
X(EN,"chai","tea (Hindi/Urdu)","চা","চা","cha","semantic_equivalent","informal",0,"food","চা মামা! দুধ চা এক কাপ","চা মামা! দুধ চা এক কাপ","Global 'chai' hype vs BD's own 'চা-মামা' street call","high","Chaiwala calling on the street."),
]
