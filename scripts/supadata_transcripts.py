#!/usr/bin/env python3
"""V3: Supadata — pull Bangla YouTube transcripts for high-value videos."""
import os, csv, json, requests, time

KEY = os.environ.get("SUPADATA_KEY", "")
OUT = "/home/z/my-project/v3_raw"
PRIO_HINTS = ["stand up", "কমেডি", "street interview", "roasting", "prank",
              "মজার দৃশ্য", "বুলি", "ভাষা", "funny", "ফানি"]

def pt_seconds(d):
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m: return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s

def main():
    with open(f"{OUT}/yt_videos.csv") as f:
        rows = list(csv.DictReader(f))
    # prioritize: matched query hints OR high views; relax duration window
    cand = []
    for r in rows:
        q = r["query"].lower()
        secs = pt_seconds(r["duration"])
        hint = any(h.lower() in q for h in PRIO_HINTS)
        if secs and not (120 <= secs <= 2700): continue
        if int(r["views"]) < 10000: continue
        if hint or int(r["views"]) > 2000000:
            cand.append((1 if hint else 0, int(r["views"]), r))
    cand.sort(key=lambda t: (-t[0], -t[1]))
    picked, seen = [], set()
    for _, _, r in cand:
        if r["videoId"] in seen: continue
        seen.add(r["videoId"]); picked.append(r)
        if len(picked) >= 8: break
    print(f"selected {len(picked)} videos (candidates {len(cand)})")
    out = []
    for r in picked:
        try:
            resp = requests.get("https://api.supadata.ai/v1/youtube/transcript",
                                params={"videoId": r["videoId"]},
                                headers={"x-api-key": KEY}, timeout=60).json()
            segs = resp.get("content") or []
            text = " ".join(s.get("text", "") for s in segs if s.get("text"))
            rec = {"videoId": r["videoId"], "title": r["title"], "channel": r["channel"],
                   "lang": resp.get("lang"), "duration_s": pt_seconds(r["duration"]),
                   "n_segments": len(segs), "text": text, "source_url": f"https://youtube.com/watch?v={r['videoId']}"}
            out.append(rec)
            print(f"[ok] {r['videoId']} lang={resp.get('lang')} chars={len(text)} — {r['title'][:50]}", flush=True)
        except Exception as e:
            print(f"[err] {r['videoId']}: {e}", flush=True)
        time.sleep(1.5)
    with open(f"{OUT}/supadata_transcripts.jsonl", "w") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"DONE transcripts={len(out)} total_chars={sum(len(r['text']) for r in out)}")

if __name__ == "__main__":
    main()
