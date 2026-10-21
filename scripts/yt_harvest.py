#!/usr/bin/env python3
"""V3 harvest: YouTube Data API v3 — Bangla video search + comments mining."""
import os, json, csv, time, requests, sys

YT_KEY = os.environ.get("YT_KEY", "")
OUT = "/home/z/my-project/v3_raw"
API = "https://www.googleapis.com/youtube/v3"

QUERIES = [
    "বাংলা ফানি ভিডিও", "bangla funny video", "বাংলা স্ট্যান্ড আপ কমেডি",
    "bangla stand up comedy", "চট্টগ্রাম বুলি", "সিলেটি কমেডি",
    "নোয়াখালী ভাষা", "dhaka street interview", "bangla roasting video",
    "bangla prank", "ঢাকার ভাষা", "bangla meme compilation",
    "bangla rap song", "বাংলা র‍্যাপ", "bangladesh cricket fans chant",
    "বাংলা নাটক মজার দৃশ্য",
]

def search(q, pages=1):
    vids = []
    token = ""
    for _ in range(pages):
        p = {"part": "snippet", "q": q, "type": "video", "maxResults": 25,
             "regionCode": "BD", "relevanceLanguage": "bn", "key": YT_KEY}
        if token: p["pageToken"] = token
        r = requests.get(f"{API}/search", params=p, timeout=30).json()
        for it in r.get("items", []):
            if it["id"].get("videoId"):
                s = it["snippet"]
                vids.append({"videoId": it["id"]["videoId"], "query": q,
                             "title": s["title"], "channel": s["channelTitle"],
                             "published": s["publishedAt"]})
        token = r.get("nextPageToken", "")
        if not token: break
        time.sleep(0.3)
    return vids

def details(ids):
    out = []
    for i in range(0, len(ids), 50):
        p = {"part": "statistics,snippet", "id": ",".join(ids[i:i+50]), "key": YT_KEY}
        r = requests.get(f"{API}/videos", params=p, timeout=30).json()
        for it in r.get("items", []):
            st = it.get("statistics", {})
            out.append({"videoId": it["id"],
                        "views": int(st.get("viewCount", 0)),
                        "likes": int(st.get("likeCount", 0)),
                        "comments": int(st.get("commentCount", 0)),
                        "duration": it["snippet"].get("duration", ""),
                        "tags": "|".join(it["snippet"].get("tags", [])[:8])})
        time.sleep(0.3)
    return out

def comments(vid, limit=60):
    out, token, n = [], "", 0
    while n < limit:
        p = {"part": "snippet", "videoId": vid, "maxResults": 100,
             "textFormat": "plainText", "key": YT_KEY}
        if token: p["pageToken"] = token
        r = requests.get(f"{API}/commentThreads", params=p, timeout=30)
        if r.status_code != 200: break
        for it in r.json().get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]
            out.append({"videoId": vid, "text": s["textDisplay"],
                        "likes": s["likeCount"], "author": s["authorDisplayName"][:40]})
        n += 100
        token = r.json().get("nextPageToken", "")
        if not token: break
        time.sleep(0.2)
    return out

def main():
    all_vids, seen = [], set()
    for q in QUERIES:
        try:
            for v in search(q):
                if v["videoId"] not in seen:
                    seen.add(v["videoId"]); all_vids.append(v)
            print(f"[search] {q}: total unique {len(all_vids)}", flush=True)
        except Exception as e:
            print(f"[search-err] {q}: {e}", flush=True)
        time.sleep(0.4)
    with open(f"{OUT}/yt_videos_raw.json", "w") as f:
        json.dump(all_vids, f, ensure_ascii=False)

    ids = [v["videoId"] for v in all_vids]
    det = details(ids)
    detmap = {d["videoId"]: d for d in det}
    with open(f"{OUT}/yt_video_details.json", "w") as f:
        json.dump(det, f, ensure_ascii=False)

    # pick top by views for comment mining (max 30 videos)
    top = sorted(det, key=lambda d: -d["views"])[:30]
    all_c, done = [], set()
    for d in top:
        vid = d["videoId"]
        if vid in done or d.get("comments", 0) == 0: continue
        try:
            cs = comments(vid)
            all_c.extend(cs)
            done.add(vid)
            print(f"[comments] {vid} views={d['views']}: {len(cs)} comments", flush=True)
        except Exception as e:
            print(f"[comments-err] {vid}: {e}", flush=True)
        time.sleep(0.3)
    with open(f"{OUT}/yt_comments.jsonl", "w") as f:
        for c in all_c:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # merged video table
    with open(f"{OUT}/yt_videos.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["videoId", "title", "channel", "published", "views", "likes",
                    "n_comments", "duration", "tags", "query"])
        for v in all_vids:
            d = detmap.get(v["videoId"], {})
            w.writerow([v["videoId"], v["title"], v["channel"], v["published"],
                        d.get("views", 0), d.get("likes", 0), d.get("comments", 0),
                        d.get("duration", ""), d.get("tags", ""), v["query"]])
    print(f"DONE videos={len(all_vids)} comments={len(all_c)}", flush=True)

if __name__ == "__main__":
    if not YT_KEY:
        sys.exit("YT_KEY missing")
    main()
