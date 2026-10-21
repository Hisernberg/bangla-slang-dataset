---
language:
- bn
license: apache-2.0
task_categories:
- translation
- text2text-generation
pretty_name: Bangla Dialect Normalization
configs:
- config_name: default
  data_files:
  - split: train
    path: train.jsonl
  - split: validation
    path: validation.jsonl
  - split: test
    path: test.jsonl
---

# Bangla Dialect Normalization Dataset

A parallel corpus mapping standard Bangla to five regional Bangla dialects,
built from the Vashantor dataset. Each row contains the same sentence in
standard Bangla and Banglish (romanized), alongside its dialect Bangla and
dialect Banglish equivalent, plus an English gloss.

## Regions covered
Barishal, Chittagong, Mymensingh, Noakhali, Sylhet

## Schema

| Field | Description |
|---|---|
| `standard_bangla` | Sentence in standard Bangla script |
| `standard_banglish` | Same sentence, romanized |
| `dialect_bangla` | Regional dialect translation, Bangla script |
| `dialect_banglish` | Regional dialect translation, romanized |
| `region` | Dialect region name |
| `english` | English gloss of the sentence |

## Splits
- `train`
- `validation`
- `test`

## Intended use
Dialect-aware ASR/NLP training, dialect normalization, and fine-tuning
LLMs for Bangladeshi regional dialect understanding.