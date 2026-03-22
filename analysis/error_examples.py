#!/usr/bin/env python3
"""Find best/worst prediction examples and categorize error types."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from diac_evaluation import calculate_der, calculate_wer, clear_line, get_diacritics_classes

BASE = os.path.join(os.path.dirname(__file__), '..')
REF_PATH = os.path.join(BASE, 'Public_Data_TrainDev', 'dev input-output', 'Dev_output.json')
PRED_PATH = os.path.join(BASE, 'outputs', 'fine_tashkeel_dev_predictions.json')

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

def main():
    with open(REF_PATH, 'r', encoding='utf-8') as f:
        references = json.load(f)
    ref_lookup = {r['id']: r['text_diacritized'] for r in references}

    with open(PRED_PATH, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    pred_lookup = {p['id']: p['text_diacritized'] for p in predictions}

    # Compute per-sentence DER (with and without case ending)
    sentence_scores = []
    for sid in ref_lookup:
        if sid not in pred_lookup:
            continue
        der_wce = per_sentence_der(pred_lookup[sid], ref_lookup[sid], case_ending=True)
        der_woce = per_sentence_der(pred_lookup[sid], ref_lookup[sid], case_ending=False)
        sentence_scores.append({
            'id': sid,
            'der_wce': der_wce,
            'der_woce': der_woce,
            'case_ending_impact': der_wce - der_woce,
            'pred': pred_lookup[sid],
            'ref': ref_lookup[sid],
        })

    # Sort by DER
    sentence_scores.sort(key=lambda x: x['der_wce'])

    # Perfect predictions
    perfect = [s for s in sentence_scores if s['der_wce'] == 0.0]
    print(f"\n=== Perfect Predictions (DER=0%): {len(perfect)} / {len(sentence_scores)} ===")
    for s in perfect[:5]:
        print(f"  ID: {s['id']}")
        print(f"  Text: {s['ref'][:80]}...")

    # Worst predictions
    print(f"\n=== Worst Predictions (Top 10 by DER) ===")
    for s in sentence_scores[-10:]:
        print(f"  ID: {s['id']}  DER(WCE): {s['der_wce']:.1f}%  DER(w/oCE): {s['der_woce']:.1f}%  CE Impact: {s['case_ending_impact']:.1f}%")
        print(f"    REF: {s['ref'][:100]}")
        print(f"    PRD: {s['pred'][:100]}")
        print()

    # Case ending analysis
    ce_impacts = [s['case_ending_impact'] for s in sentence_scores]
    avg_ce = sum(ce_impacts) / len(ce_impacts) if ce_impacts else 0
    high_ce = [s for s in sentence_scores if s['case_ending_impact'] > 10]
    print(f"\n=== Case Ending Impact Analysis ===")
    print(f"Average CE impact on DER: {avg_ce:.2f}%")
    print(f"Sentences with >10% CE impact: {len(high_ce)} / {len(sentence_scores)}")

    # DER distribution
    bins = [0, 5, 10, 15, 20, 30, 50, 100]
    print(f"\n=== DER Distribution ===")
    for i in range(len(bins)-1):
        count = sum(1 for s in sentence_scores if bins[i] <= s['der_wce'] < bins[i+1])
        pct = count / len(sentence_scores) * 100
        print(f"  {bins[i]:>3}%-{bins[i+1]:>3}%: {count:>4} sentences ({pct:.1f}%)")

if __name__ == '__main__':
    main()
