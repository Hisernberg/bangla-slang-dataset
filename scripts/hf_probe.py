#!/usr/bin/env python3
"""V3: probe HF for open Bangla speech/lyrics datasets, pull transcripts via datasets-server."""
import os, json, requests, time

OUTDIR = "/home/z/my-project/bangla-slang-dataset/data/audio/speech_samples"
os.makedirs(OUTDIR, exist_ok=True)
HUB = "https://huggingface.co/api/datasets"
DSS = "https://datasets-server.huggingface.co"
HDR = {}
if os.environ.get("HF_TOKEN"):
    HDR["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"

def ok_splits(ds_id):
    try:
        r = requests.get(f"{DSS}/splits", params={"dataset": ds_id}, headers=HDR, timeout=60)
        if r.status_code != 200: return None
        sp = r.json().get("splits", [])
        return [(s["config"], s["split"]) for s in sp] or None
    except Exception:
        return None

def pull_rows(ds_id, cfg, split, length=100):
    r = requests.get(f"{DSS}/rows", params={"dataset": ds_id, "config": cfg, "split": split,
                                            "offset": 0, "length": length}, headers=HDR, timeout=120)
    if r.status_code != 200: return None
    return r.json().get("rows", [])

def main():
    found = {}
    for term in ["bengali asr", "bengali speech", "bangla speech", "bengali audio", "bangla lyrics"]:
        try:
            r = requests.get(HUB, params={"search": term, "limit": 30, "sort": "downloads"},
                             headers=HDR, timeout=40).json()
        except Exception as e:
            print(f"[hub-err] {term}: {e}"); continue
        for d in r:
            did = d.get("id", "")
            if not did: continue
            dl = d.get("downloads", 0)
            if did in found: continue
            sp = ok_splits(did)
            if not sp: continue
            cfg, split = sp[0]
            try:
                rows = pull_rows(did, cfg, split)
            except Exception:
                continue
            if not rows: continue
            sample_keys = list(rows[0]["row"].keys())
            found[did] = {"config": cfg, "split": split, "n": len(rows), "fields": sample_keys[:10], "downloads": dl}
            fn = did.replace("/", "__")
            with open(f"{OUTDIR}/{fn}_rows.json", "w") as f:
                json.dump(rows, f, ensure_ascii=False)
            print(f"[PULLED] {did} cfg={cfg} n={len(rows)} fields={sample_keys[:10]} dl={dl}", flush=True)
        time.sleep(1)
    with open(f"{OUTDIR}/hf_probe_manifest.json", "w") as f:
        json.dump(found, f, ensure_ascii=False, indent=1)
    print("DONE", json.dumps({k: v["n"] for k, v in found.items()}))

if __name__ == "__main__":
    main()
