# Grep Benchmarks

Public benchmark results for [Grep](https://grep.ai) — an AI-powered deep research platform by Parcha.

![Grep: #1 across all major deep research benchmarks](deepresearch-bench/charts/01_hero_three_benchmarks.png)

## Benchmarks

### [DRACO](draco/) — February 2026

Evaluation on Perplexity's [DRACO](https://www.perplexity.ai/hub/blog/draco) benchmark: 100 open-ended research tasks across 10 domains, scored on 3,934 weighted rubric criteria by Gemini-2.5-Pro.

| Metric | Value |
|--------|-------|
| **Normalized Score** | **78.6%** |
| Domains Won (vs Perplexity) | 9 / 10 |
| Rubric Axes Led | 4 / 4 |

Grep ranks **#1** overall, ahead of Perplexity DR (70.5%), Gemini DR (59.0%), and OpenAI DR o3 (52.1%). Leads all 4 rubric axes: Factual Accuracy (+7.5pp), Breadth & Depth (+7.2pp), Presentation (+3.0pp), Citation (+14.5pp).

### [DeepSearchQA](deepsearchqa/) — February 2026

Evaluation on Google's [DeepSearchQA](https://arxiv.org/abs/2505.15420) benchmark: 896 multi-step research questions across 17 fields, independently reproduced by Kaggle.

| Metric | Value |
|--------|-------|
| **Adjusted FC (pass@1)** | **84.5%** (757 / 896) |
| Automated FC | 83.4% (747 / 896) |
| Avg F1 (concise) | 0.915 |

Grep ranks **#1** on the unofficial leaderboard, ahead of Perplexity Deep Research (81.9%), Moonshot K2.5 (77.1%), and the Kaggle-verified #1 Gemini Deep Research Agent (66.1%).

### [DeepResearch Bench](deepresearch-bench/) — April 2026

Evaluation on 100 PhD-level research queries using the [RACE](https://arxiv.org/abs/2504.13477) scoring framework (Gemini-2.5-Pro judge, comparative scoring against expert-written references).

| Dimension | Score |
|-----------|:-----:|
| **Overall** | **56.27** |
| Comprehensiveness | 56.79 |
| Insight | 58.98 |
| Instruction Following | 53.49 |
| Readability | 53.50 |

Grep ranks **#1** on the [leaderboard](https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard), ahead of Cellcog Max (56.13), nvidia-aiq (55.95), and Cellcog (55.31).

---

*Parcha Labs Inc — [grep.ai](https://grep.ai)*
