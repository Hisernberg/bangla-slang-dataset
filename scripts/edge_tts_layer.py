#!/usr/bin/env python3
"""V3: Edge-TTS — generate Bengali audio layer for Kothar Rong gold entries."""
import asyncio, csv, json, os, subprocess, sys
import edge_tts

REPO = "/home/z/my-project/bangla-slang-dataset"
OUTDIR = f"{REPO}/data/audio/kothar_rong_tts"
os.makedirs(OUTDIR, exist_ok=True)
TARGET = 230
VOICES = ["bn-BD-NabanitaNeural", "bn-BD-PradeepNeural"]
SEM = asyncio.Semaphore(4)

def has_bn(s):
    return any("\u0980" <= c <= "\u09FF" for c in s)

def pick_entries():
    rows = list(csv.DictReader(open(f"{REPO}/data/final/bangla_slang_master.csv")))
    eligible = [r for r in rows if has_bn(r["term_bn"])
                and (r["popularity"] in ("3", "4", "5") or r["tier"] == "1")]
    by_cat = {}
    for r in eligible:
        by_cat.setdefault(r["category"], []).append(r)
    for c in by_cat:
        by_cat[c].sort(key=lambda r: (-(int(r["popularity"]) if r["popularity"] else 1), r["tier"] != "1"))
    picked, cats = [], list(by_cat)
    i = 0
    while len(picked) < TARGET:
        added = False
        for c in cats:
            if i < len(by_cat[c]):
                picked.append(by_cat[c][i]); added = True
                if len(picked) >= TARGET: break
        if not added: break
        i += 1
    return picked

async def gen(r, voice, idx):
    fn = f"kr_tts_{r['id']}_{idx:03d}.mp3"
    path = f"{OUTDIR}/{fn}"
    for attempt in range(3):
        try:
            async with SEM:
                c = edge_tts.Communicate(r["term_bn"], voice)
                await c.save(path)
            if os.path.getsize(path) > 1000:
                return {"id": r["id"], "term_bn": r["term_bn"],
                        "romanization": r["romanization"], "meaning_en": r["meaning_en"],
                        "category": r["category"], "region": r["region"],
                        "voice": voice, "file": f"data/audio/kothar_rong_tts/{fn}",
                        "source": "microsoft-edge-tts", "license": "generated (no copyright)"}
        except Exception as e:
            await asyncio.sleep(2 * (attempt + 1))
    return None

def ffprobe_dur(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                              "-of", "csv=p=0", path], capture_output=True, text=True, timeout=15)
        return out.stdout.strip()
    except Exception:
        return ""

async def main():
    picked = pick_entries()
    print(f"selected {len(picked)} entries across {len(set(r['category'] for r in picked))} categories")
    tasks = [gen(r, VOICES[i % len(VOICES)], i) for i, r in enumerate(picked)]
    results = await asyncio.gather(*tasks)
    ok = [x for x in results if x]
    for rec, path in zip(ok, [f"{OUTDIR}/{x['file'].split('/')[-1]}" for x in ok]):
        rec["duration_s"] = ffprobe_dur(path)
    with open(f"{OUTDIR}/tts_manifest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ok[0].keys()))
        w.writeheader(); w.writerows(ok)
    with open(f"{OUTDIR}/tts_manifest.json", "w") as f:
        json.dump(ok, f, ensure_ascii=False, indent=1)
    print(f"DONE generated={len(ok)}/{len(picked)}")

if __name__ == "__main__":
    asyncio.run(main())
