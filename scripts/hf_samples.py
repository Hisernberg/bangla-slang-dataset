#!/usr/bin/env python3
"""V3: HuggingFace datasets-server — CV mirror + FLEURS + Kathbath Bengali samples."""
import json, os, requests

REPO = "/home/z/my-project/bangla-slang-dataset"
OUTDIR = f"{REPO}/data/audio/speech_samples"
os.makedirs(OUTDIR, exist_ok=True)
DS = "https://datasets-server.huggingface.co"

TARGETS = [
    {"name": "fleurs_bn", "dataset": "google/fleurs", "config": "bn_bd", "split": "train",
     "text_field": "transcription"},
    {"name": "kathbath_bn", "dataset": "ai4bharat/Kathbath", "config": "bengali", "split": "train",
     "text_field": "sentence"},
    {"name": "common_voice_bn", "dataset": "mozilla-foundation/common_voice_17_0", "config": "bn",
     "split": "train", "text_field": "sentence"},
]

def get(url, tries=4):
    headers = {}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"
    for i in range(tries):
        r = requests.get(url, timeout=90, headers=headers)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 404:
            return None
        if "busier" in r.text.lower() or r.status_code in (429, 503, 500):
            import time
            time.sleep(15 * (i + 1))
            continue
    return None

def main():
    manifests = {}
    for t in TARGETS:
        name, ds = t["name"], t["dataset"]
        try:
            sp = get(f"{DS}/splits?dataset={requests.utils.quote(ds, safe='')}")
            if sp is None:
                print(f"[skip] {name}: dataset not found/split error")
                continue
            cfgs = [s["config"] for s in sp.get("splits", [])]
            cfg = t["config"] if t["config"] in cfgs else (cfgs[0] if cfgs else "")
            if not cfg:
                print(f"[skip] {name}: no configs"); continue
            rows = get(f"{DS}/rows?dataset={requests.utils.quote(ds, safe='')}"
                       f"&config={requests.utils.quote(cfg, safe='')}&split={t['split']}&offset=0&length=100")
            if not rows or "rows" not in rows:
                print(f"[skip] {name}: rows unavailable"); continue
            recs = []
            for r in rows["rows"]:
                row = r["row"]
                audio = row.get("audio") or {}
                recs.append({
                    "text": row.get(t["text_field"], ""),
                    "audio_url": audio.get("[uri]", ""),
                    "audio_bytes": audio if isinstance(audio, list) else None,
                    "dataset": ds, "config": cfg, "split": t["split"],
                })
            # fallback: audio field may be dict with blob/uri variants
            with open(f"{OUTDIR}/{name}_transcripts.json", "w") as f:
                json.dump(recs, f, ensure_ascii=False, indent=1)
            manifests[name] = {"dataset": ds, "config": cfg, "n_transcripts": len(recs)}
            print(f"[ok] {name} cfg={cfg}: {len(recs)} rows", flush=True)
            # inspect first row keys once
            if rows["rows"]:
                print(f"     fields: {list(rows['rows'][0]['row'].keys())[:12]}", flush=True)
        except Exception as e:
            print(f"[err] {name}: {e}")
    with open(f"{OUTDIR}/speech_samples_manifest.json", "w") as f:
        json.dump(manifests, f, ensure_ascii=False, indent=1)
    print("DONE", manifests)

if __name__ == "__main__":
    main()
