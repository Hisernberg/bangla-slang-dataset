#!/usr/bin/env python3
"""V3: Telegram — scrape public t.me/s/<channel> previews of Bangla meme channels."""
import json, re, time, requests, html

OUT = "/home/z/my-project/v3_raw"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

CANDIDATES = [
    "banglamemes", "bangla_memes", "bdmemes", "dhakamemes", "banglameme",
    "memesbangla", "bangladesh_memes", "meme_bangladesh", "chittagongmemes",
    "sylheti_memes", "dhakameme", "banglamemez", "bikikok", "deshermemes",
    "trollbd", "troll_bd", "funnybangla", "banglafunny", "memesofbangladesh",
]

MSG_RE = re.compile(r'<div class="tgme_widget_message_text js-message_text"[^>]*>(.*?)</div>', re.S)
TAG_RE = re.compile(r"<[^>]+>")

def scrape_channel(ch):
    r = requests.get(f"https://t.me/s/{ch}", headers=UA, timeout=25)
    if r.status_code != 200 or "js-message_text" not in r.text:
        return []
    msgs = []
    for raw in MSG_RE.findall(r.text):
        txt = html.unescape(TAG_RE.sub(" ", raw))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) >= 3:
            msgs.append({"channel": ch, "text": txt, "source_url": f"https://t.me/{ch}"})
    return msgs

def main():
    all_msgs, ok = [], []
    for ch in CANDIDATES:
        try:
            msgs = scrape_channel(ch)
            if msgs:
                all_msgs.extend(msgs)
                ok.append(f"{ch}({len(msgs)})")
                print(f"[ok] {ch}: {len(msgs)} messages", flush=True)
            else:
                print(f"[skip] {ch}", flush=True)
        except Exception as e:
            print(f"[err] {ch}: {e}", flush=True)
        time.sleep(1.2)
    with open(f"{OUT}/telegram_messages.jsonl", "w") as f:
        for m in all_msgs:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(f"DONE channels={ok} messages={len(all_msgs)}")

if __name__ == "__main__":
    main()
