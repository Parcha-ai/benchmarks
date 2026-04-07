#!/usr/bin/env python3
"""Generate PNG charts for the DRACO benchmark report.

Usage:
    cd draco/scripts
    python generate_charts.py

Outputs PNGs to ../charts/
"""

import json
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import numpy as np

# ── Paths ──
SCRIPT_DIR = Path(__file__).resolve().parent
CHARTS_DIR = SCRIPT_DIR.parent / "charts"
DATA_DIR = SCRIPT_DIR.parent / "data" / "feb-2026"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Colors (matching deepsearchqa style) ──
ORANGE = "#e85d04"      # GREP accent
NAVY = "#1a1a2e"        # Other systems
GREEN = "#2d6a4f"
YELLOW = "#b08600"
RED = "#9d0208"
BG = "#fafafa"
FG = "#111111"
FG_SECONDARY = "#555555"
BORDER_LIGHT = "#e5e5e5"

# System-specific colors for multi-system charts
SYSTEM_COLORS = {
    "Grep Deep Research":       ORANGE,
    "Perplexity DR (Opus 4.6)": "#4ECDC4",
    "Perplexity DR (Opus 4.5)": "#3BA99E",
    "Gemini DR":                "#FFB300",
    "OpenAI DR (o3)":           "#EF5350",
    "OpenAI DR (o4-mini)":      "#AB47BC",
    "Claude Opus 4.6":          "#42A5F5",
    "Claude Opus 4.5":          "#78909C",
}

# ── Load data ──
with open(DATA_DIR / "results.json") as f:
    results = json.load(f)

# ── Paper data (Table 8: Normalized scores by system) ──
DOMAINS = [
    "Finance", "Shopping/Product Comparison", "Academic", "Technology",
    "General Knowledge", "UX Design", "Law", "Medicine",
    "Needle in a Haystack", "Personalized Assistant",
]

PAPER_NORMALIZED = {
    "Perplexity DR (Opus 4.6)": {
        "overall": 70.5,
        "Finance": 71.0, "Shopping/Product Comparison": 64.7, "Academic": 82.8,
        "Technology": 63.1, "General Knowledge": 66.3, "UX Design": 62.4,
        "Law": 90.2, "Medicine": 80.5, "Needle in a Haystack": 58.1,
        "Personalized Assistant": 63.8,
    },
    "Perplexity DR (Opus 4.5)": {
        "overall": 67.2,
        "Finance": 56.3, "Shopping/Product Comparison": 63.1, "Academic": 80.2,
        "Technology": 66.6, "General Knowledge": 70.8, "UX Design": 60.3,
        "Law": 86.0, "Medicine": 73.6, "Needle in a Haystack": 68.4,
        "Personalized Assistant": 68.5,
    },
    "Gemini DR": {
        "overall": 59.0,
        "Finance": 49.4, "Shopping/Product Comparison": 53.8, "Academic": 72.7,
        "Technology": 56.8, "General Knowledge": 59.6, "UX Design": 50.8,
        "Law": 83.5, "Medicine": 58.8, "Needle in a Haystack": 62.8,
        "Personalized Assistant": 61.9,
    },
    "OpenAI DR (o3)": {
        "overall": 52.1,
        "Finance": 42.1, "Shopping/Product Comparison": 44.7, "Academic": 73.5,
        "Technology": 46.3, "General Knowledge": 51.5, "UX Design": 51.9,
        "Law": 66.7, "Medicine": 65.0, "Needle in a Haystack": 54.5,
        "Personalized Assistant": 49.4,
    },
    "OpenAI DR (o4-mini)": {
        "overall": 41.9,
        "Finance": 41.1, "Shopping/Product Comparison": 36.3, "Academic": 54.1,
        "Technology": 40.8, "General Knowledge": 44.1, "UX Design": 36.5,
        "Law": 62.3, "Medicine": 44.2, "Needle in a Haystack": 35.1,
        "Personalized Assistant": 31.6,
    },
    "Claude Opus 4.6": {
        "overall": 59.8,
        "Finance": 48.5, "Shopping/Product Comparison": 51.9, "Academic": 72.0,
        "Technology": 53.2, "General Knowledge": 67.0, "UX Design": 54.3,
        "Law": 88.6, "Medicine": 72.5, "Needle in a Haystack": 66.2,
        "Personalized Assistant": 55.2,
    },
    "Claude Opus 4.5": {
        "overall": 46.7,
        "Finance": 37.1, "Shopping/Product Comparison": 38.1, "Academic": 56.3,
        "Technology": 41.1, "General Knowledge": 52.2, "UX Design": 35.0,
        "Law": 75.0, "Medicine": 65.9, "Needle in a Haystack": 57.4,
        "Personalized Assistant": 45.0,
    },
}

# Table 13: Normalized scores by rubric axis
PAPER_AXIS_NORMALIZED = {
    "Perplexity DR (Opus 4.6)": {"Factual Accuracy": 67.9, "Breadth & Depth": 66.0, "Presentation": 90.3, "Citation": 64.6},
    "Perplexity DR (Opus 4.5)": {"Factual Accuracy": 62.9, "Breadth & Depth": 73.1, "Presentation": 84.9, "Citation": 62.5},
    "Gemini DR":                 {"Factual Accuracy": 54.9, "Breadth & Depth": 59.9, "Presentation": 87.1, "Citation": 51.5},
    "OpenAI DR (o3)":            {"Factual Accuracy": 51.4, "Breadth & Depth": 51.4, "Presentation": 63.2, "Citation": 45.8},
    "OpenAI DR (o4-mini)":       {"Factual Accuracy": 39.7, "Breadth & Depth": 38.7, "Presentation": 58.1, "Citation": 42.5},
    "Claude Opus 4.6":           {"Factual Accuracy": 57.9, "Breadth & Depth": 57.3, "Presentation": 73.8, "Citation": 56.2},
    "Claude Opus 4.5":           {"Factual Accuracy": 46.7, "Breadth & Depth": 35.7, "Presentation": 65.4, "Citation": 42.1},
}

# ── Compute GREP data from results.json ──
grep_overall = results["summary"]["overall_normalized_score"]

grep_domains = {}
for d_entry in results["summary"]["by_domain"]:
    grep_domains[d_entry["domain"]] = d_entry["normalized_score"]

grep_axes = {}
for a_entry in results["summary"]["by_axis"]:
    grep_axes[a_entry["axis"]] = a_entry["normalized_score"]

grep_questions = results["questions"]


def style_ax(ax, title=None):
    """Apply consistent styling to an axis."""
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER_LIGHT)
    ax.spines["bottom"].set_color(BORDER_LIGHT)
    ax.tick_params(colors=FG_SECONDARY, labelsize=10)
    if title:
        ax.set_title(title, fontsize=16, fontweight="bold", color=NAVY,
                      pad=16, loc="left")


# ═══════════════════════════════════════════════════════
# 1. LEADERBOARD — horizontal bar chart
# ═══════════════════════════════════════════════════════
def generate_leaderboard():
    systems = [
        ("Grep Deep Research", grep_overall),
        ("Perplexity DR (Opus 4.6)", 70.5),
        ("Perplexity DR (Opus 4.5)", 67.2),
        ("Claude Opus 4.6 (no DR)", 59.8),
        ("Gemini Deep Research", 59.0),
        ("OpenAI DR (o3)", 52.1),
        ("Claude Opus 4.5 (no DR)", 46.7),
        ("OpenAI DR (o4-mini)", 41.9),
    ]
    systems.sort(key=lambda x: x[1], reverse=True)

    names = [x[0] for x in systems][::-1]
    scores = [x[1] for x in systems][::-1]
    colors = [ORANGE if "Grep" in n else NAVY for n in names]

    fig, ax = plt.subplots(figsize=(10, 7))
    style_ax(ax, "DRACO Benchmark — Overall Normalized Scores (%)")

    bars = ax.barh(range(len(names)), scores, color=colors, height=0.7,
                    edgecolor="none")

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10, fontweight="500")
    ax.set_xlim(30, 90)
    ax.set_xlabel("Normalized Score (%)", fontsize=11, color=FG_SECONDARY)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))

    for bar, score, name in zip(bars, scores, names):
        weight = "bold" if "Grep" in name else "normal"
        ax.text(score + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}%", va="center", ha="left",
                fontsize=9, fontweight=weight, color=FG)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "leaderboard.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  leaderboard.png")


# ═══════════════════════════════════════════════════════
# 2. DOMAIN PERFORMANCE — per-domain bars, all systems
# ═══════════════════════════════════════════════════════
def generate_domain_performance():
    """Grouped horizontal bar chart: GREP vs all systems per domain."""
    sorted_domains = sorted(DOMAINS, key=lambda d: -grep_domains.get(d, 0))

    all_systems = [
        ("Grep Deep Research", {d: grep_domains.get(d, 0) for d in DOMAINS}),
        ("Perplexity DR (Opus 4.6)", PAPER_NORMALIZED["Perplexity DR (Opus 4.6)"]),
        ("Perplexity DR (Opus 4.5)", PAPER_NORMALIZED["Perplexity DR (Opus 4.5)"]),
        ("Gemini DR", PAPER_NORMALIZED["Gemini DR"]),
        ("OpenAI DR (o3)", PAPER_NORMALIZED["OpenAI DR (o3)"]),
        ("OpenAI DR (o4-mini)", PAPER_NORMALIZED["OpenAI DR (o4-mini)"]),
        ("Claude Opus 4.6", PAPER_NORMALIZED["Claude Opus 4.6"]),
        ("Claude Opus 4.5", PAPER_NORMALIZED["Claude Opus 4.5"]),
    ]
    sys_colors = [SYSTEM_COLORS[s[0]] for s in all_systems]

    n_sys = len(all_systems)
    n_dom = len(sorted_domains)

    fig, axes_arr = plt.subplots(2, 5, figsize=(20, 10))
    axes_flat = axes_arr.flatten()

    short_sys_names = ["GREP", "Perp\n(4.6)", "Perp\n(4.5)", "Gemini", "o3", "o4-\nmini", "Opus\n4.6", "Opus\n4.5"]
    x = np.arange(n_sys)

    for dom_idx, domain in enumerate(sorted_domains):
        ax = axes_flat[dom_idx]
        values = [sys_data[domain] for _, sys_data in all_systems]

        bars = ax.bar(x, values, width=0.78, color=sys_colors, edgecolor="none")

        for i, (bar, val) in enumerate(zip(bars, values)):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.8,
                    f"{val:.0f}", ha="center", va="bottom",
                    fontsize=7, fontweight="bold", color=FG)

        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 25))
        ax.set_xticks(x)
        ax.set_xticklabels(short_sys_names, fontsize=6.5, color=FG_SECONDARY,
                           rotation=0, ha="center")

        short = domain.replace("Shopping/Product Comparison", "Shopping/Product") \
                      .replace("Needle in a Haystack", "Needle/Haystack") \
                      .replace("Personalized Assistant", "Personal Assistant") \
                      .replace("General Knowledge", "General Knowledge")
        style_ax(ax, None)
        ax.set_title(short, fontsize=9, fontweight="bold", color=NAVY, pad=6)
        ax.grid(axis="y", color=BORDER_LIGHT, linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)

    legend_patches = [mpatches.Patch(color=c, label=n)
                      for n, c in zip([s[0] for s in all_systems], sys_colors)]
    fig.legend(handles=legend_patches, loc="lower center", ncol=4,
               fontsize=9, frameon=False, handlelength=1.5, columnspacing=2,
               bbox_to_anchor=(0.5, -0.02))

    fig.suptitle("DRACO — Normalized Scores by Domain", fontsize=16,
                 fontweight="bold", color=NAVY, x=0.02, ha="left", y=0.99)

    plt.tight_layout(rect=[0, 0.05, 1, 0.96])
    fig.savefig(CHARTS_DIR / "domain_performance.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  domain_performance.png")


# ═══════════════════════════════════════════════════════
# 3. GREP vs PERPLEXITY — domain-by-domain comparison
# ═══════════════════════════════════════════════════════
def generate_grep_vs_perplexity():
    """Side-by-side: GREP vs Perplexity (best of 4.5/4.6) per domain."""
    sorted_domains = sorted(DOMAINS, key=lambda d: -grep_domains.get(d, 0))

    grep_vals = [grep_domains.get(d, 0) for d in sorted_domains]
    perp_vals = [max(PAPER_NORMALIZED["Perplexity DR (Opus 4.6)"][d],
                     PAPER_NORMALIZED["Perplexity DR (Opus 4.5)"][d])
                 for d in sorted_domains]

    x = np.arange(len(sorted_domains))
    w = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    style_ax(ax, "Grep vs Perplexity — Domain by Domain")

    bars1 = ax.bar(x - w / 2, grep_vals, width=w, color=ORANGE,
                   label="Grep Deep Research", edgecolor="none")
    bars2 = ax.bar(x + w / 2, perp_vals, width=w, color=NAVY,
                   label="Perplexity DR (best)", edgecolor="none")

    for i, (g, p) in enumerate(zip(grep_vals, perp_vals)):
        delta = g - p
        marker = "+" if delta > 0 else ""
        color = GREEN if delta > 0 else RED
        ax.text(i, max(g, p) + 1.5, f"{marker}{delta:.1f}pp", ha="center",
                va="bottom", fontsize=8, fontweight="bold", color=color)

    short_names = [
        d.replace("Shopping/Product Comparison", "Shopping/\nProduct")
         .replace("Needle in a Haystack", "Needle in\nHaystack")
         .replace("Personalized Assistant", "Personalized\nAssistant")
         .replace("General Knowledge", "General\nKnowledge")
        for d in sorted_domains
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, fontsize=8.5, color=FG)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Normalized Score (%)", fontsize=11, color=FG_SECONDARY)
    ax.grid(axis="y", color=BORDER_LIGHT, linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10, frameon=False, loc="upper right")

    domains_won = sum(1 for g, p in zip(grep_vals, perp_vals) if g > p)
    win_text = f"Grep wins {domains_won}/10 domains"
    ax.text(0.5, 0.02, win_text, transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=ORANGE, ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=BG,
                      edgecolor=ORANGE, linewidth=2))

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "grep_vs_perplexity.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  grep_vs_perplexity.png")


# ═══════════════════════════════════════════════════════
# 4. RUBRIC AXIS BREAKDOWN — grouped bars per axis
# ═══════════════════════════════════════════════════════
def generate_axis_breakdown():
    """4 subplots, one per rubric axis, all systems."""
    axis_names = ["Factual Accuracy", "Breadth & Depth", "Presentation", "Citation"]

    all_systems = [
        ("Grep Deep Research", grep_axes),
        ("Perplexity DR (Opus 4.6)", PAPER_AXIS_NORMALIZED["Perplexity DR (Opus 4.6)"]),
        ("Perplexity DR (Opus 4.5)", PAPER_AXIS_NORMALIZED["Perplexity DR (Opus 4.5)"]),
        ("Gemini DR", PAPER_AXIS_NORMALIZED["Gemini DR"]),
        ("OpenAI DR (o3)", PAPER_AXIS_NORMALIZED["OpenAI DR (o3)"]),
        ("OpenAI DR (o4-mini)", PAPER_AXIS_NORMALIZED["OpenAI DR (o4-mini)"]),
        ("Claude Opus 4.6", PAPER_AXIS_NORMALIZED["Claude Opus 4.6"]),
        ("Claude Opus 4.5", PAPER_AXIS_NORMALIZED["Claude Opus 4.5"]),
    ]
    sys_colors = [SYSTEM_COLORS[s[0]] for s in all_systems]

    short_names = ["GREP", "Perp\n(4.6)", "Perp\n(4.5)", "Gemini", "o3", "o4-\nmini", "Opus\n4.6", "Opus\n4.5"]
    x = np.arange(len(all_systems))

    fig, axes_arr = plt.subplots(1, 4, figsize=(18, 6), sharey=True)

    for ax_idx, axis_name in enumerate(axis_names):
        ax = axes_arr[ax_idx]
        values = [sys_data[axis_name] for _, sys_data in all_systems]

        bars = ax.bar(x, values, width=0.72, color=sys_colors, edgecolor="none")

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 1,
                    f"{val:.1f}", ha="center", va="bottom",
                    fontsize=7.5, fontweight="bold", color=FG)

        ax.set_ylim(0, 105)
        ax.set_yticks(range(0, 101, 20))
        ax.set_xticks(x)
        ax.set_xticklabels(short_names, fontsize=7, color=FG_SECONDARY)
        style_ax(ax, None)
        ax.set_title(axis_name, fontsize=11, fontweight="bold", color=NAVY, pad=10)
        ax.grid(axis="y", color=BORDER_LIGHT, linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)

    axes_arr[0].set_ylabel("Normalized Score (%)", fontsize=11, color=FG_SECONDARY)

    fig.suptitle("DRACO — Scores by Rubric Axis", fontsize=16,
                 fontweight="bold", color=NAVY, x=0.02, ha="left", y=0.99)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(CHARTS_DIR / "axis_breakdown.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  axis_breakdown.png")


# ═══════════════════════════════════════════════════════
# 5. DOMAIN HEATMAP — table-style visualization
# ═══════════════════════════════════════════════════════
def generate_domain_heatmap():
    """Heatmap table of normalized scores: systems x domains."""
    sys_order = [
        "Grep Deep Research",
        "Perplexity DR (Opus 4.6)", "Perplexity DR (Opus 4.5)",
        "Gemini DR", "OpenAI DR (o3)", "OpenAI DR (o4-mini)",
        "Claude Opus 4.6", "Claude Opus 4.5",
    ]

    data = {}
    data["Grep Deep Research"] = {d: grep_domains.get(d, 0) for d in DOMAINS}
    for sys_name in sys_order[1:]:
        data[sys_name] = {d: PAPER_NORMALIZED[sys_name].get(d, 0) for d in DOMAINS}

    n_sys = len(sys_order)
    n_dom = len(DOMAINS)

    matrix = np.zeros((n_sys, n_dom))
    for i, sys_name in enumerate(sys_order):
        for j, dom in enumerate(DOMAINS):
            matrix[i, j] = data[sys_name].get(dom, 0)

    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list(
        "grep", ["#FFFFFF", "#FFF3E0", "#FFE0B2", "#FFB74D", ORANGE], N=256
    )

    fig, ax = plt.subplots(figsize=(16, 5.5))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=30, vmax=95)

    short_domains = [
        d.replace("Shopping/Product Comparison", "Shopping/\nProduct")
         .replace("Needle in a Haystack", "Needle in\nHaystack")
         .replace("Personalized Assistant", "Personalized\nAssistant")
         .replace("General Knowledge", "General\nKnowledge")
        for d in DOMAINS
    ]

    ax.set_xticks(range(n_dom))
    ax.set_xticklabels(short_domains, fontsize=8, color=FG, rotation=0, ha="center")
    ax.set_yticks(range(n_sys))
    ax.set_yticklabels(sys_order, fontsize=9, color=FG)

    for i in range(n_sys):
        for j in range(n_dom):
            val = matrix[i, j]
            col_max = matrix[:, j].max()
            weight = "bold" if val == col_max else "normal"
            text_color = "#FFFFFF" if val > 78 else FG
            ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                    fontsize=8, fontweight=weight, color=text_color)

    # Highlight GREP row
    ax.axhline(y=0.5, color=ORANGE, linewidth=2)
    ax.axhline(y=-0.5, color=ORANGE, linewidth=2)

    ax.set_title("DRACO — Normalized Scores by Domain (all systems)",
                 fontsize=14, fontweight="bold", color=NAVY, loc="left", pad=15)
    ax.tick_params(axis="x", which="both", bottom=False, top=True,
                   labeltop=True, labelbottom=False)

    for spine in ax.spines.values():
        spine.set_color(BORDER_LIGHT)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "domain_heatmap.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  domain_heatmap.png")


# ═══════════════════════════════════════════════════════
# 6. SCORE DISTRIBUTION — histogram
# ═══════════════════════════════════════════════════════
def generate_score_distribution():
    """Histogram of per-question normalized scores."""
    scores = [q["normalized_score"] for q in grep_questions]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: histogram
    bins = np.arange(0, 105, 5)
    ax1.hist(scores, bins=bins, color=ORANGE, edgecolor="#FFFFFF", linewidth=0.5,
             alpha=0.9)
    mean_val = np.mean(scores)
    median_val = np.median(scores)
    ax1.axvline(x=mean_val, color=NAVY, linestyle="--", linewidth=1.5,
                label=f"Mean: {mean_val:.1f}%")
    ax1.axvline(x=median_val, color=FG_SECONDARY, linestyle=":", linewidth=1.5,
                label=f"Median: {median_val:.1f}%")
    style_ax(ax1, "Score Distribution (100 questions)")
    ax1.set_xlabel("Normalized Score (%)", fontsize=10, color=FG_SECONDARY)
    ax1.set_ylabel("Number of Questions", fontsize=10, color=FG_SECONDARY)
    ax1.legend(fontsize=9, frameon=False)

    # Right: bucket breakdown
    buckets = {"90-100%": 0, "80-89%": 0, "70-79%": 0,
               "60-69%": 0, "50-59%": 0, "<50%": 0}
    for s in scores:
        if s >= 90: buckets["90-100%"] += 1
        elif s >= 80: buckets["80-89%"] += 1
        elif s >= 70: buckets["70-79%"] += 1
        elif s >= 60: buckets["60-69%"] += 1
        elif s >= 50: buckets["50-59%"] += 1
        else: buckets["<50%"] += 1

    bucket_names = list(buckets.keys())
    bucket_vals = list(buckets.values())

    def bucket_color(pct_range):
        if pct_range.startswith("90") or pct_range.startswith("80"):
            return GREEN
        elif pct_range.startswith("70") or pct_range.startswith("60"):
            return YELLOW
        else:
            return RED

    b_colors = [bucket_color(b) for b in bucket_names]

    bars = ax2.barh(range(len(bucket_names)), bucket_vals, color=b_colors,
                    height=0.6, edgecolor="none")
    for i, (bar, val) in enumerate(zip(bars, bucket_vals)):
        ax2.text(val + 0.3, i, str(val), va="center", ha="left",
                 fontsize=11, fontweight="bold", color=FG)

    ax2.set_yticks(range(len(bucket_names)))
    ax2.set_yticklabels(bucket_names, fontsize=10)
    ax2.invert_yaxis()
    style_ax(ax2, "Score Buckets")
    ax2.set_xlabel("Number of Questions", fontsize=10, color=FG_SECONDARY)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "score_distribution.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  score_distribution.png")


# ═══════════════════════════════════════════════════════
# 7. AXIS DELTA — GREP vs Perplexity per rubric axis
# ═══════════════════════════════════════════════════════
def generate_axis_delta():
    """Delta chart: GREP minus Perplexity (best) per axis."""
    axes_names = ["Factual Accuracy", "Breadth & Depth", "Presentation", "Citation"]
    weights = [52.1, 21.7, 14.1, 12.1]

    grep_vals = [grep_axes[a] for a in axes_names]
    perp_best = [
        max(PAPER_AXIS_NORMALIZED["Perplexity DR (Opus 4.6)"][a],
            PAPER_AXIS_NORMALIZED["Perplexity DR (Opus 4.5)"][a])
        for a in axes_names
    ]
    deltas = [g - p for g, p in zip(grep_vals, perp_best)]

    fig, ax = plt.subplots(figsize=(10, 5))
    style_ax(ax, "Grep vs Perplexity (best) — Delta by Rubric Axis")

    labels = [f"{a}\n({w}% weight)" for a, w in zip(axes_names, weights)]
    delta_colors = [GREEN if d > 0 else RED for d in deltas]

    bars = ax.barh(range(len(labels)), deltas, color=delta_colors,
                   height=0.5, edgecolor="none")
    for i, (bar, delta, g, p) in enumerate(zip(bars, deltas, grep_vals, perp_best)):
        side = "left" if delta >= 0 else "right"
        offset = 0.5 if delta >= 0 else -0.5
        ax.text(delta + offset, i,
                f"{delta:+.1f}pp  (GREP {g:.1f}% vs {p:.1f}%)",
                va="center", ha=side, fontsize=9, fontweight="bold", color=FG)

    ax.axvline(x=0, color=FG, linewidth=1)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=BORDER_LIGHT, linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "axis_delta.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  axis_delta.png")


# ── Run all ──
if __name__ == "__main__":
    print("Generating DRACO charts...")
    generate_leaderboard()
    generate_domain_performance()
    generate_grep_vs_perplexity()
    generate_axis_breakdown()
    generate_domain_heatmap()
    generate_score_distribution()
    generate_axis_delta()
    print(f"Done. Charts saved to {CHARTS_DIR}")
