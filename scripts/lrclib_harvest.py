#!/usr/bin/env python3
"""V3: LRCLIB — harvest Bangla song lyrics (rock/hip-hop = slang-rich). No key needed."""
import json, time, requests

OUT = "/home/z/my-project/v3_raw"
UA = {"User-Agent": "KotharRongDataset/3.0 (academic slang research; contact: ELITE Research Lab)"}

QUERIES = ["বাংলা গান", "bangla song", "Artcell", "Aurthohin", "Warfaze", "Shironamhin",
           "Meghdol", "Arbovirus", "Black Zang", "bangla rap", "bangla hip hop",
           "Mayabini", "Hasimukh", "bangla funny song", "মায়াবিনি"]
CAP_PER_QUERY = 8

def search(params, tries=4):
    for i in range(tries):
        r = requests.get("https://lrclib.net/api/search", params=params, headers=UA, timeout=30)
        if r.status_code == 200:
            return r.json()
        wait = int(r.headers.get("Retry-After", 8 * (i + 1)))
        print(f"  [backoff {r.status_code}] waiting {wait}s", flush=True)
        time.sleep(min(wait, 60))
    return []

def main():
    out, seen = [], set()
    for artist in QUERIES:
        recs = search({"q": artist})
        kept = 0
        for rec in recs:
            if kept >= CAP_PER_QUERY: break
            if rec.get("instrumental"): continue
            plain = rec.get("plainLyrics") or ""
            if len(plain) < 80: continue
            key = (rec.get("artistName", ""), rec.get("trackName", ""))
            if key in seen: continue
            seen.add(key)
            out.append({"artist": rec.get("artistName", ""), "title": rec.get("trackName", ""),
                        "album": rec.get("albumName", ""), "duration_s": rec.get("duration"),
                        "lang": "bn", "has_synced": bool(rec.get("syncedLyrics")),
                        "plain_lyrics": plain, "source": "lrclib.net", "query_artist": artist})
            kept += 1
        print(f"[lrclib] {artist}: {kept} tracks with lyrics", flush=True)
        time.sleep(2.5)
    with open(f"{OUT}/lrclib_lyrics.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"DONE tracks={len(out)} chars={sum(len(r['plain_lyrics']) for r in out)}")

if __name__ == "__main__":
    main()
