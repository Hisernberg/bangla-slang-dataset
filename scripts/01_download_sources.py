#!/usr/bin/env python3
"""Download raw slang data from Kaggle, HuggingFace, and GitHub repos."""
import os, json, urllib.request, ssl, gzip, io

RAW = "/home/z/my-project/bangla-slang-dataset/data/raw"
os.makedirs(RAW, exist_ok=True)
ctx = ssl.create_default_context()

KG = os.environ["KAGGLE_API_TOKEN"]
HF = os.environ["HF_TOKEN"]
GH = os.environ["GITHUB_TOKEN"]

def get(url, headers=None, binary=False):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0 bangla-slang-collector"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")

results = []

# 1. Kaggle: suspicious-bengali-text-slang
try:
    data = get("https://www.kaggle.com/api/v1/datasets/download/mizan116/suspicious-bengali-text-slang",
               {"Authorization": f"Bearer {KG}"}, binary=True)
    path = os.path.join(RAW, "kaggle_suspicious_bengali_slang.zip")
    open(path, "wb").write(data)
    results.append(("kaggle_suspicious", len(data), "ok"))
except Exception as e:
    results.append(("kaggle_suspicious", 0, f"ERR {e}"))

# 2. HF: Vulgar Lexicon Chittagonian
for owner in ["TanjimKIT", "kit-nlp"]:
    try:
        data = get(f"https://huggingface.co/datasets/{owner}/Vulgar_Lexicon_of_Chittagonian_Dialect_of_Bangla_or_Bengali/resolve/main/Vulgar%20Word.csv",
                   {"Authorization": f"Bearer {HF}"})
        path = os.path.join(RAW, f"hf_chittagong_vulgar_{owner}.csv")
        open(path, "w", encoding="utf-8").write(data)
        results.append((f"hf_chittagong_{owner}", len(data), "ok"))
    except Exception as e:
        results.append((f"hf_chittagong_{owner}", 0, f"ERR {e}"))

# 3. GitHub raw files
gh_files = [
    ("Sigmakib2/Nirmol", "datasets/Nirmol-v1-dataset.csv", "gh_nirmol_v1.csv"),
    ("Sigmakib2/Nirmol", "nirmol.json", "gh_nirmol.json"),
    ("Sigmakib2/Nirmol", "prefixes_suffixes.json", "gh_nirmol_affixes.json"),
    ("amirulsizan/deshi-slang", "data/profanity_dataset.jsonl", "gh_deshi_slang.jsonl"),
    ("amirulsizan/deshi-slang", "data/labels_map.csv", "gh_deshi_labels.csv"),
    ("amirulsizan/deshi-slang", "data/profanity_raw.txt", "gh_deshi_raw.txt"),
    ("anurag-panda-dev/KelaScript", "README.md", "gh_kelascript_readme.md"),
    ("kuntalojha/slangs", "README.md", "gh_slangs_readme.md"),
]
for repo, fpath, outname in gh_files:
    try:
        data = get(f"https://raw.githubusercontent.com/{repo}/HEAD/{fpath}",
                   {"Authorization": f"token {GH}"})
        open(os.path.join(RAW, outname), "w", encoding="utf-8").write(data)
        results.append((outname, len(data), "ok"))
    except Exception as e:
        results.append((outname, 0, f"ERR {e}"))

for name, size, status in results:
    print(f"{status:6} {size:>9}  {name}")
