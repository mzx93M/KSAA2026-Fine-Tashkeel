#!/usr/bin/env python3
"""Generate all figures for the KSAA-2026 Fine-Tashkeel paper."""
import csv
import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# Arabic text shaping
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_ARABIC_SHAPING = True
except ImportError:
    HAS_ARABIC_SHAPING = False
    print('  Warning: arabic_reshaper/python-bidi not installed, Arabic text may render incorrectly')


_reshaper_plain = None
_reshaper_diac = None

def shape_arabic(text, keep_diacritics=False):
    """Reshape and reorder Arabic text for correct matplotlib rendering."""
    if HAS_ARABIC_SHAPING:
        global _reshaper_plain, _reshaper_diac
        if keep_diacritics:
            if _reshaper_diac is None:
                _reshaper_diac = arabic_reshaper.ArabicReshaper(
                    configuration={'delete_harakat': False})
            reshaped = _reshaper_diac.reshape(text)
        else:
            if _reshaper_plain is None:
                _reshaper_plain = arabic_reshaper.ArabicReshaper()
            reshaped = _reshaper_plain.reshape(text)
        return get_display(reshaped)
    return text

# Paths
BASE = os.path.join(os.path.dirname(__file__), '..')
FIGURES_DIR = os.path.join(BASE, 'paper', 'figures')
NATIONALITY_CSV = os.path.join(BASE, 'analysis', 'per_nationality_results.csv')
DEV_CSV = os.path.join(BASE, 'analysis', 'dev_results_all_models.csv')
REF_PATH = os.path.join(BASE, 'Public_Data_TrainDev', 'dev input-output', 'Dev_output.json')
PRED_PATH = os.path.join(BASE, 'outputs', 'fine_tashkeel_dev_predictions.json')

sys.path.insert(0, os.path.join(BASE, 'src'))
from diac_evaluation import clear_line, get_diacritics_classes

# Find an Arabic-capable font
ARABIC_FONT = None
for candidate in ['Geeza Pro', 'Al Nile', 'Arial Unicode MS', '.SF Arabic']:
    matches = [f.fname for f in fm.fontManager.ttflist if f.name == candidate]
    if matches:
        ARABIC_FONT = fm.FontProperties(fname=matches[0])
        print(f'  Using Arabic font: {candidate}')
        break

# Style
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.15,
})

COLORS = {
    'primary': '#2563EB',
    'secondary': '#10B981',
    'accent': '#F59E0B',
    'danger': '#EF4444',
    'purple': '#8B5CF6',
    'gray': '#6B7280',
    'light_blue': '#DBEAFE',
    'light_green': '#D1FAE5',
    'dark_blue': '#1D4ED8',
}

# Dialect region color mapping
REGION_COLORS = {
    'Egypt': '#2563EB',        # Nile Valley
    'Sudan': '#3B82F6',        # Nile Valley
    'Palestine': '#10B981',    # Levantine
    'Syria': '#34D399',        # Levantine
    'Kuwait': '#F59E0B',       # Gulf
    'Qatar': '#FBBF24',        # Gulf
    'Saudi': '#F97316',        # Gulf
    'Bahrain': '#FB923C',      # Gulf
    'Algeria': '#EF4444',      # Maghrebi
}


def per_sentence_der(pred_text, ref_text, case_ending=True):
    """Compute DER for a single sentence."""
    pred_line = clear_line(pred_text)
    ref_line = clear_line(ref_text)
    pred_classes = get_diacritics_classes(pred_line, case_ending)
    ref_classes = get_diacritics_classes(ref_line, case_ending)
    if len(pred_classes) != len(ref_classes):
        min_len = min(len(pred_classes), len(ref_classes))
        pred_classes = pred_classes[:min_len]
        ref_classes = ref_classes[:min_len]
    equal = sum(1 for p, r in zip(pred_classes, ref_classes) if p == r and p != -1)
    not_equal = sum(1 for p, r in zip(pred_classes, ref_classes) if p != r and p != -1 and r != -1)
    total = equal + not_equal
    return (not_equal / total * 100) if total > 0 else 0.0


def fig1_system_diagram():
    """Generate pipeline diagram with Arabic examples."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')

    # Box styles
    input_style = dict(boxstyle="round,pad=0.5", facecolor=COLORS['light_blue'],
                       edgecolor=COLORS['primary'], linewidth=2)
    model_style = dict(boxstyle="round,pad=0.5", facecolor=COLORS['primary'],
                       edgecolor=COLORS['dark_blue'], linewidth=2)
    output_style = dict(boxstyle="round,pad=0.5", facecolor=COLORS['light_green'],
                        edgecolor=COLORS['secondary'], linewidth=2)
    label_style = dict(boxstyle="round,pad=0.35", facecolor='#F3F4F6',
                       edgecolor=COLORS['gray'], linewidth=1, linestyle='--')

    y_main = 2.6

    # Input box
    ax.text(1.5, y_main, 'Undiacritized\nTranscript', ha='center', va='center',
            fontsize=12, fontweight='bold', bbox=input_style)

    # Arrow 1
    ax.annotate('', xy=(3.5, y_main), xytext=(2.7, y_main),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.5))

    # Encoder box
    ax.text(4.5, y_main, 'Encoder', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white', bbox=model_style)

    # Arrow 2
    ax.annotate('', xy=(6.2, y_main), xytext=(5.5, y_main),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.5))

    # Decoder box
    ax.text(7.2, y_main, 'Decoder', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white', bbox=model_style)

    # Arrow 3
    ax.annotate('', xy=(8.9, y_main), xytext=(8.2, y_main),
                arrowprops=dict(arrowstyle='->', color=COLORS['gray'], lw=2.5))

    # Output box
    ax.text(10.2, y_main, 'Diacritized\nOutput', ha='center', va='center',
            fontsize=12, fontweight='bold', bbox=output_style)

    # Model label box (centered under encoder-decoder)
    ax.text(5.85, 1.35, 'Fine-Tashkeel\n(Seq2Seq Transformer)', ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['gray'], bbox=label_style)

    # Connecting lines from label to encoder-decoder
    ax.plot([4.5, 4.5], [2.05, 1.75], color=COLORS['gray'], lw=1, alpha=0.5)
    ax.plot([7.2, 7.2], [2.05, 1.75], color=COLORS['gray'], lw=1, alpha=0.5)
    ax.plot([4.5, 7.2], [1.75, 1.75], color=COLORS['gray'], lw=1, alpha=0.5)
    ax.plot([5.85, 5.85], [1.75, 1.6], color=COLORS['gray'], lw=1, alpha=0.5)

    # Arabic example text (reshaped for correct RTL rendering in matplotlib)
    arabic_input = shape_arabic('كتب الطالب الدرس')
    arabic_output = shape_arabic('كَتَبَ الطَّالِبُ الدَّرْسَ', keep_diacritics=True)
    font_kw = dict(fontproperties=ARABIC_FONT) if ARABIC_FONT else {}

    ax.text(1.5, 0.55, arabic_input, ha='center', va='center',
            fontsize=14, color=COLORS['primary'], **font_kw)
    ax.text(10.2, 0.55, arabic_output, ha='center', va='center',
            fontsize=14, color=COLORS['secondary'], **font_kw)

    # Small labels
    ax.text(1.5, 0.15, '(undiacritized)', ha='center', va='center',
            fontsize=8, color=COLORS['gray'], fontstyle='italic')
    ax.text(10.2, 0.15, '(fully diacritized)', ha='center', va='center',
            fontsize=8, color=COLORS['gray'], fontstyle='italic')

    out = os.path.join(FIGURES_DIR, 'system_diagram.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [1/6] system_diagram.png saved')


def fig2_nationality_bar():
    """Grouped bar chart of DER/WER by nationality with non-overlapping legends."""
    nationalities, counts, ders, wers = [], [], [], []
    with open(NATIONALITY_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nationalities.append(row['nationality'])
            counts.append(int(row['count']))
            ders.append(float(row['DER_WCE']))
            wers.append(float(row['WER_WCE']))

    # Sort by DER
    order = sorted(range(len(ders)), key=lambda i: ders[i])
    nationalities = [nationalities[i] for i in order]
    counts = [counts[i] for i in order]
    ders = [ders[i] for i in order]
    wers = [wers[i] for i in order]
    colors = [REGION_COLORS.get(n, COLORS['gray']) for n in nationalities]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = range(len(nationalities))
    width = 0.35

    bars_der = ax.bar([i - width/2 for i in x], ders, width, label='DER (%)',
                      color=colors, edgecolor='white', linewidth=0.5, alpha=0.85)
    bars_wer = ax.bar([i + width/2 for i in x], wers, width, label='WER (%)',
                      color=colors, edgecolor='white', linewidth=0.5, alpha=0.45)

    # Add count labels above bars
    for i, (n, c) in enumerate(zip(nationalities, counts)):
        ax.text(i, max(ders[i], wers[i]) + 1.0, f'n={c}', ha='center',
                fontsize=8, color=COLORS['gray'])

    ax.set_xlabel('Nationality')
    ax.set_ylabel('Error Rate (%)')
    ax.set_title('Per-Nationality DER and WER on Dev Set (Fine-Tashkeel)')
    ax.set_xticks(list(x))
    ax.set_xticklabels(nationalities, rotation=30, ha='right')
    ax.set_ylim(0, max(wers) + 6)
    ax.grid(axis='y', alpha=0.3)

    # Metric legend (top-right)
    metric_handles = [
        mpatches.Patch(facecolor='gray', alpha=0.85, label='DER (%)'),
        mpatches.Patch(facecolor='gray', alpha=0.40, label='WER (%)'),
    ]
    leg1 = ax.legend(handles=metric_handles, loc='upper right', fontsize=9,
                     framealpha=0.9)
    ax.add_artist(leg1)

    # Region legend (upper-center-right, below metric legend)
    regions = {
        'Nile Valley': '#2563EB', 'Levantine': '#10B981',
        'Gulf': '#F59E0B', 'Maghrebi': '#EF4444'
    }
    region_patches = [mpatches.Patch(color=c, label=r) for r, c in regions.items()]
    ax.legend(handles=region_patches, loc='upper center', fontsize=8,
              title='Region', title_fontsize=9, ncol=4, framealpha=0.9)

    out = os.path.join(FIGURES_DIR, 'nationality_bar.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [2/6] nationality_bar.png saved')


def fig3_der_distribution():
    """Histogram of per-sentence DER distribution on dev set."""
    with open(REF_PATH, 'r', encoding='utf-8') as f:
        references = json.load(f)
    ref_lookup = {r['id']: r['text_diacritized'] for r in references}

    with open(PRED_PATH, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    pred_lookup = {p['id']: p['text_diacritized'] for p in predictions}

    ders = []
    for sid in ref_lookup:
        if sid in pred_lookup:
            d = per_sentence_der(pred_lookup[sid], ref_lookup[sid], case_ending=True)
            ders.append(d)

    perfect = sum(1 for d in ders if d == 0.0)
    pct_perfect = perfect / len(ders) * 100

    fig, ax = plt.subplots(figsize=(7, 4.5))

    bins = [0, 0.01, 5, 10, 15, 20, 30, 50]
    labels = ['0%\n(Perfect)', '0-5%', '5-10%', '10-15%', '15-20%', '20-30%', '30-50%']
    counts_binned = []
    for i in range(len(bins) - 1):
        c = sum(1 for d in ders if bins[i] <= d < bins[i+1])
        counts_binned.append(c)

    bar_colors = [COLORS['secondary']] + [COLORS['primary']] * (len(labels) - 2) + [COLORS['danger']]
    bars = ax.bar(range(len(labels)), counts_binned, color=bar_colors,
                  edgecolor='white', linewidth=0.5)

    # Annotate counts above bars
    for i, (bar, count) in enumerate(zip(bars, counts_binned)):
        pct = count / len(ders) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

    # Highlight perfect predictions - arrow from top-right pointing to the green bar
    ax.annotate(f'{pct_perfect:.1f}% Perfect\nDiacritization',
                xy=(0, perfect), xytext=(2.5, perfect + 8),
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=1.5),
                fontsize=10, fontweight='bold', color=COLORS['secondary'])

    ax.set_xlabel('Per-Sentence DER Range')
    ax.set_ylabel('Number of Sentences')
    ax.set_title('Distribution of Per-Sentence DER on Dev Set (Fine-Tashkeel, n=260)')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(counts_binned) + 22)
    ax.grid(axis='y', alpha=0.3)

    out = os.path.join(FIGURES_DIR, 'der_distribution.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [3/6] der_distribution.png saved')


def fig4_model_comparison():
    """Horizontal bar chart comparing all models by blind test DER."""
    models = [
        ('Fine-Tashkeel', 'Seq2Seq', 'Infer.', 10.56),
        ('ASR-Tashkeel', 'Seq2Seq', 'Pipeline', 10.70),
        ('Shakkelha', 'Text-only', 'Infer.', 13.14),
        ('Shakkala', 'Text-only', 'Infer.', 19.70),
        ('CATT', 'Text-only', 'Infer.', 28.34),
        ('Tashkeel-700M', 'Text-only', 'FT', 34.04),
        ('FLAN-T5', 'Text-only', 'Infer.', 37.80),
        ('ArTST', 'ASR+Text', 'Infer.', 42.82),
        ('Seamless M4T', 'ASR+Text', 'Infer.', 43.01),
        ('CAMeL-MLE', 'Text-only', 'Infer.', 45.89),
        ('ByT5 Glonor', 'Text-only', 'Infer.', 46.96),
        ('ByT5 Glonor (FT)', 'Text-only', 'FT', 54.15),
        ('Whisper-Tashkeel (FT)', 'ASR+Text', 'FT', 54.61),
        ('Qwen-1.5', 'Text-only', 'Infer.', 62.56),
        ('Mishkal', 'Text-only', 'Infer.', 76.76),
        ('Whisper (large-v3)', 'ASR+Text', 'Infer.', 84.71),
        ('Tarteel Whisper', 'ASR+Text', 'Infer.', 84.93),
        ('Whisper Quran LoRA', 'ASR+Text', 'Infer.', 97.36),
        ('mT5-base', 'Text-only', 'Infer.', 99.74),
    ]

    # Sort by DER descending (so best appears at top in horizontal bar)
    models.sort(key=lambda x: x[3], reverse=True)

    names = [m[0] for m in models]
    ders = [m[3] for m in models]
    types = [m[1] for m in models]
    methods = [m[2] for m in models]

    type_colors = {
        'Seq2Seq': COLORS['primary'],
        'Text-only': COLORS['secondary'],
        'ASR+Text': COLORS['accent'],
    }
    method_alpha = {'Infer.': 0.85, 'Pipeline': 0.85, 'FT': 0.55}

    fig, ax = plt.subplots(figsize=(9, 7))
    bar_colors = [type_colors.get(t, COLORS['gray']) for t in types]
    alphas = [method_alpha.get(m, 0.85) for m in methods]

    bars = ax.barh(range(len(names)), ders, color=bar_colors, edgecolor='white',
                   linewidth=0.5)
    for bar, alpha in zip(bars, alphas):
        bar.set_alpha(alpha)

    # Labels: inside bar for large DER, outside for small
    for i, name in enumerate(names):
        der_val = ders[i]
        if name == 'Fine-Tashkeel':
            bars[i].set_edgecolor(COLORS['danger'])
            bars[i].set_linewidth(2.5)
            # Label outside for our system (small bar)
            ax.text(der_val + 1.2, i, f'{der_val}% (Ours)',
                    va='center', fontsize=9, fontweight='bold', color=COLORS['danger'])
        elif der_val > 70:
            # Label inside bar for long bars
            ax.text(der_val - 2, i, f'{der_val}%',
                    va='center', ha='right', fontsize=8, color='white', fontweight='bold')
        else:
            ax.text(der_val + 1.0, i, f'{der_val}%',
                    va='center', fontsize=8, color=COLORS['gray'])

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('DER (%) on Blind Test Set')
    ax.set_title('Model Comparison by Blind Test DER')
    ax.set_xlim(0, 105)
    ax.grid(axis='x', alpha=0.3)

    # Legend
    patches = [
        mpatches.Patch(color=COLORS['primary'], label='Seq2Seq'),
        mpatches.Patch(color=COLORS['secondary'], label='Text-only'),
        mpatches.Patch(color=COLORS['accent'], label='ASR+Text'),
        mpatches.Patch(facecolor='gray', alpha=0.85, label='Inference'),
        mpatches.Patch(facecolor='gray', alpha=0.45, label='Fine-tuned'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=9, framealpha=0.9)

    out = os.path.join(FIGURES_DIR, 'model_comparison.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [4/6] model_comparison.png saved')


def fig5_dev_test_divergence():
    """Scatter plot of dev DER vs blind test DER for each model."""
    # Only models with reliable dev evaluation (excludes ArTST, CATT,
    # Seamless M4T, Tarteel Whisper whose dev scores were artifacts of
    # an evaluation library that post-processed predictions)
    models = [
        ('Fine-Tashkeel', 8.10, 10.56, 'Seq2Seq'),
        ('Shakkelha', 10.26, 13.14, 'Text-only'),
        ('Shakkala', 11.64, 19.70, 'Text-only'),
        ('FLAN-T5', 24.37, 37.80, 'Text-only'),
        ('CAMeL-MLE', 28.71, 45.89, 'Text-only'),
        ('ByT5 Glonor', 15.28, 46.96, 'Text-only'),
        ('Qwen-1.5', 33.75, 62.56, 'Text-only'),
        ('Mishkal', 17.37, 76.76, 'Text-only'),
        ('Whisper Quran LoRA', 8.35, 97.36, 'ASR+Text'),
        ('mT5-base', 82.17, 99.74, 'Text-only'),
        # Fine-tuned
        ('Tashkeel-700M (FT)', 22.08, 34.04, 'Text-only'),
        ('ByT5 Glonor (FT)', 23.12, 54.15, 'Text-only'),
        ('Whisper-Tashkeel (FT)', 46.05, 54.61, 'ASR+Text'),
    ]

    type_colors = {
        'Seq2Seq': COLORS['primary'],
        'Text-only': COLORS['secondary'],
        'ASR+Text': COLORS['accent'],
    }

    fig, ax = plt.subplots(figsize=(7, 6))

    # Diagonal line (perfect consistency)
    ax.plot([0, 100], [0, 100], 'k--', alpha=0.3, linewidth=1)

    # Shade the "stable" region (bottom-left)
    ax.fill_between([0, 25], [0, 0], [25, 25], alpha=0.06, color=COLORS['secondary'])
    ax.text(20, 3, 'Stable\nregion', fontsize=9, color=COLORS['secondary'], alpha=0.6,
            ha='center', fontstyle='italic')

    for name, dev, test, mtype in models:
        color = type_colors.get(mtype, COLORS['gray'])
        if name == 'Fine-Tashkeel':
            ax.scatter(dev, test, c=color, marker='*', s=250, zorder=5,
                       edgecolors=COLORS['danger'], linewidth=2)
            ax.annotate('Fine-Tashkeel\n(Ours)', xy=(dev, test),
                        xytext=(dev + 12, test + 5),
                        fontsize=9, fontweight='bold', color=COLORS['danger'],
                        arrowprops=dict(arrowstyle='->', color=COLORS['danger'], lw=1.5))
        else:
            ax.scatter(dev, test, c=color, marker='o', s=60, zorder=3,
                       edgecolors='white', linewidth=0.5, alpha=0.8)

    ax.set_xlabel('Dev DER (%)')
    ax.set_ylabel('Blind Test DER (%)')
    ax.set_title('Dev vs. Blind Test DER Divergence')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)

    patches = [
        mpatches.Patch(color=COLORS['primary'], label='Seq2Seq'),
        mpatches.Patch(color=COLORS['secondary'], label='Text-only'),
        mpatches.Patch(color=COLORS['accent'], label='ASR+Text'),
    ]
    ax.legend(handles=patches, loc='center left', fontsize=9, framealpha=0.9,
              bbox_to_anchor=(0.0, 0.55))

    out = os.path.join(FIGURES_DIR, 'dev_test_divergence.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [5/6] dev_test_divergence.png saved')


def fig6_text_vs_multimodal():
    """Grouped bar comparing text-only vs ASR+Text model categories."""
    categories = ['Text-only\n(Inference)', 'ASR+Text\n(Inference)',
                  'Text-only\n(Fine-tuned)', 'ASR+Text\n(Fine-tuned)']
    avg_ders = [44.15, 70.57, 44.10, 54.61]
    best_ders = [10.56, 42.82, 34.04, 54.61]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(categories))
    width = 0.35

    bars_avg = ax.bar([i - width/2 for i in x], avg_ders, width,
                      label='Average DER (%)', color=COLORS['accent'], alpha=0.65,
                      edgecolor='white', linewidth=0.5)
    bars_best = ax.bar([i + width/2 for i in x], best_ders, width,
                       label='Best DER (%)', color=COLORS['primary'],
                       edgecolor='white', linewidth=0.5)

    # Annotate values above bars
    for bar, val in zip(bars_avg, avg_ders):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9, color='#B45309')
    for bar, val in zip(bars_best, best_ders):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9,
                fontweight='bold', color=COLORS['primary'])

    ax.set_ylabel('DER (%)')
    ax.set_title('Text-only vs. ASR+Text Models on Blind Test')
    ax.set_xticks(list(x))
    ax.set_xticklabels(categories)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_ylim(0, max(avg_ders) + 15)
    ax.grid(axis='y', alpha=0.3)

    # Key finding annotation - positioned in open space above the first group
    ax.annotate('Text-only inference\nachieves best DER (10.6%)',
                xy=(0.175, best_ders[0] + 1),
                xytext=(0.5, 55),
                fontsize=10, fontweight='bold', color=COLORS['primary'],
                ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=1.5),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=COLORS['primary'], alpha=0.95))

    out = os.path.join(FIGURES_DIR, 'text_vs_multimodal.png')
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  [6/6] text_vs_multimodal.png saved')


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    print('Generating figures for KSAA-2026 Fine-Tashkeel paper...')
    fig1_system_diagram()
    fig2_nationality_bar()
    fig3_der_distribution()
    fig4_model_comparison()
    fig5_dev_test_divergence()
    fig6_text_vs_multimodal()
    print(f'\nAll 6 figures saved to {FIGURES_DIR}')


if __name__ == '__main__':
    main()
