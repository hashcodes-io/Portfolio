# Master’s Thesis

## Evelink-H — Master’s Thesis: Grounding Event Mentions to Wikipedia (Harder Problems)
**Author:** Muhammad Hashaam Ahsan — M.Sc. Intelligent Adaptive Systems, University of Hamburg  
**Date:** April 29, 2024  
**Code / data:** https://github.com/semantic-systems/EvelinkH.

---

![paper](https://img.shields.io/badge/paper-2024-blue) ![type](https://img.shields.io/badge/type-Master%27s%20Thesis-lightgrey) ![topic](https://img.shields.io/badge/topic-event%20linking-yellow)

---

## TLDR (For HR & non-technical readers)
- **What is it about?** It is about *event linking* — linking textual event mentions to the correct Wikipedia page, specifically focusing on the *hard* cases sub-events, events described in subsection-only, repeating or ambiguous event titles.
- **Why it matters?** Improves reader context and downstream NLP tasks (search, summarization, QA) by accurately grounding events to canonical pages.
- **Takeaway:** The work extends an existing SOTA LLM-Based (Evelink) model with richer candidate representations and engineering to scale precomputation; it yields consistent retrieval/recall gains and demonstrates full-stack ML engineering from data prep to evaluation. 

---

## Introduction
This thesis tackles event linking by enriching candidate Wikipedia representations with **subsection titles** and **sub-event** information, then evaluating where this extra context helps in a two-stage Evelink pipeline (Bi-Encoder retrieval + Cross-Encoder re-ranking). Results show that adding richer candidate context to the **retrieval** stage yields the most consistent improvements in recall and accuracy across in-domain (Wikipedia) and out-of-domain (New York Times) evaluations — all while addressing real engineering trade-offs around precomputation and resource cost. 

---

## Key results 
> See the thesis for full tables & experiments (Tables 2–7).

- **Bi-Encoder retrieval recall (Wikipedia - Verb Seen):** baseline → **84.28%** ; enriched Bi-Encoder → **88.26%** (≈ **+3.98** percentage points). 
- **Out-of-domain (NYT - Verb Unseen Form) recall:** baseline → **51.35%** ; enriched Bi-Encoder → **55.40%** (≈ **+4.05** pp).
- **Overall accuracy (Wikipedia/ NYT):** modest but consistent gains (example: select Verb+Nominal split improves from ~88.65% → ~89.87% and ~48.63% → ~51.50% in reported settings). 
- **Compute & engineering footprint:** naive precompute estimate ≈ 555 hours; parallel pipeline reduced practical wall-time to ≈ 240 hours. Training both encoders reported ~68 hours on 2× RTX A6000 GPUs. 

---

## What I changed (technical summary)
1. **Richer candidate representation**  
   - Added section/subsection titles and extracted sub-events from Wikipedia pages to candidate meta-data. This fills context gaps where event mentions refer to subsections or sub-events not obvious from the page title alone. 

2. **Two-stage evaluation & ablation**  
   - Evaluated four configurations: extra info on neither encoder, on Bi-Encoder only, on Cross-Encoder only, and on both. The **Bi-Encoder only** enrichment consistently yields the largest recall gains — indicating retrieval is the bottleneck. 

3. **Large-scale precomputation**  
   - Built a pipeline to precompute enriched representations for millions of titles to keep inference practical; documented trade-offs and parallelization strategy.

---

## How to reproduce (practical, copy-paste commands)
> These commands are a *recommended quick plan* — consult the repo for exact script names and full parameter lists. The thesis contains exact scripts and configurations.

```bash
# 1. clone repository
git clone https://github.com/semantic-systems/EvelinkH
cd EvelinkH

# 2. prepare python env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. (heavy) precompute enriched candidate representations
#    Use --parallel or cluster options if available
python scripts/precompute_candidates.py --out data/candidates_precomputed --parallel

# 4. train Bi-Encoder (example config)
python train_bi_encoder.py --config configs/bi_base.yaml --out models/bi_encoder

# 5. generate top-k candidates for Cross-Encoder re-ranking
python scripts/generate_candidates_for_cross.py --k 30 --candidates data/candidates_precomputed \
  --out data/topk_for_cross

# 6. train Cross-Encoder
python train_cross_encoder.py --config configs/cross_base.yaml --out models/cross_encoder

# 7. evaluate
python evaluate.py --models models/ --eval data/eval_splits
