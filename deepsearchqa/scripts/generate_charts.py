#!/usr/bin/env python3
"""Generate PNG charts for the DeepSearchQA benchmark report.

Usage:
    cd deepsearchqa/scripts
    python generate_charts.py

Outputs 3 PNGs to ../charts/
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Paths ──
SCRIPT_DIR = Path(__file__).resolve().parent
CHARTS_DIR = SCRIPT_DIR.parent / "charts"
DATA_DIR = SCRIPT_DIR.parent / "data" / "feb-2026"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Colors ──
ORANGE = "#e85d04"
NAVY = "#1a1a2e"
GREEN = "#2d6a4f"
YELLOW = "#b08600"
RED = "#9d0208"
BG = "#fafafa"
FG = "#111111"
FG_SECONDARY = "#555555"
BORDER_LIGHT = "#e5e5e5"

# ── Load data ──
with open(DATA_DIR / "results.json") as f:
    results = json.load(f)


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
    leaderboard = [
        ("Grep Deep Research", 84.5),
        ("Perplexity Deep Research", 81.9),
        ("Google Deep Research", 80.4),
        ("Moonshot K2.5", 77.1),
        ("Anthropic Opus 4.5", 76.1),
        ("Parallel Ultra2x", 72.6),
        ("OpenAI GPT-5.2 (xHigh)", 71.3),
        ("Parallel Ultra", 68.5),
        ("Gemini Deep Research Agent", 66.1),
        ("GPT-5 Pro", 65.2),
        ("Parallel Pro", 62.0),
        ("OpenAI GPT 5.2 Pro", 61.0),
        ("GPT-5", 59.4),
        ("Gemini 3 Pro Preview", 56.6),
        ("o3 Deep Research", 44.2),
        ("o4 mini Deep Research", 40.4),
    ]

    # Reverse for bottom-to-top plotting
    names = [x[0] for x in leaderboard][::-1]
    scores = [x[1] for x in leaderboard][::-1]
    colors = [ORANGE if n == "Grep Deep Research" else NAVY for n in names]

    fig, ax = plt.subplots(figsize=(10, 8))
    style_ax(ax, "DeepSearchQA — Unofficial Leaderboard (FC %)")

    bars = ax.barh(range(len(names)), scores, color=colors, height=0.7,
                    edgecolor="none")

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10, fontweight="500")
    ax.set_xlim(30, 92)
    ax.set_xlabel("Fully Correct (%)", fontsize=11, color=FG_SECONDARY)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))

    # Value labels
    for bar, score, name in zip(bars, scores, names):
        weight = "bold" if name == "Grep Deep Research" else "normal"
        ax.text(score + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}%", va="center", ha="left",
                fontsize=9, fontweight=weight, color=FG)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "leaderboard.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  leaderboard.png")


# ═══════════════════════════════════════════════════════
# 2. CATEGORY PERFORMANCE — horizontal bar chart
# ═══════════════════════════════════════════════════════
def generate_category_performance():
    from collections import defaultdict
    cat_stats = defaultdict(lambda: {"total": 0, "fc": 0})
    for r in results:
        cat = r["category"]
        cat_stats[cat]["total"] += 1
        if r["concise_f1"] == 1.0:
            cat_stats[cat]["fc"] += 1

    categories = []
    for cat, s in cat_stats.items():
        pct = 100.0 * s["fc"] / s["total"] if s["total"] > 0 else 0
        categories.append((cat, pct, s["total"], s["fc"]))
    categories.sort(key=lambda x: x[1], reverse=True)

    names = [c[0] for c in categories][::-1]
    pcts = [c[1] for c in categories][::-1]
    ns = [c[2] for c in categories][::-1]

    def bar_color(pct):
        if pct >= 85:
            return GREEN
        elif pct >= 75:
            return YELLOW
        else:
            return RED

    colors = [bar_color(p) for p in pcts]

    fig, ax = plt.subplots(figsize=(10, 8))
    style_ax(ax, "Performance by Category — Concise Answer FC %")

    bars = ax.barh(range(len(names)), pcts, color=colors, height=0.7,
                    edgecolor="none")

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlim(0, 108)
    ax.set_xlabel("Fully Correct (%)", fontsize=11, color=FG_SECONDARY)

    for i, (bar, pct, n) in enumerate(zip(bars, pcts, ns)):
        ax.text(pct + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{pct:.1f}%  (n={n})", va="center", ha="left",
                fontsize=9, color=FG)

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=GREEN, label="\u2265 85%"),
        Patch(facecolor=YELLOW, label="75\u201385%"),
        Patch(facecolor=RED, label="< 75%"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9,
              framealpha=0.9)

    plt.tight_layout()
    fig.savefig(CHARTS_DIR / "category_performance.png", dpi=150,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  category_performance.png")


# ── Run all ──
if __name__ == "__main__":
    print("Generating charts...")
    generate_leaderboard()
    generate_category_performance()
    print(f"Done. Charts saved to {CHARTS_DIR}")
