#!/usr/bin/env python3
"""Evaluate all dev predictions against ground truth and produce a ranked table."""
import json
import glob
import os
import sys
import csv

# Add parent dir to path for diac_evaluation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from diac_evaluation import compute_metrics

BASE = os.path.join(os.path.dirname(__file__), '..')
REF_PATH = os.path.join(BASE, 'Public_Data_TrainDev', 'dev input-output', 'Dev_output.json')
PRED_DIR = os.path.join(BASE, 'outputs')

def main():
    with open(REF_PATH, 'r', encoding='utf-8') as f:
        references = json.load(f)

    pred_files = sorted(glob.glob(os.path.join(PRED_DIR, '*_dev_predictions.json')))

    results = []
    for pf in pred_files:
        model_name = os.path.basename(pf).replace('_dev_predictions.json', '')
        try:
            with open(pf, 'r', encoding='utf-8') as f:
                predictions = json.load(f)
            metrics = compute_metrics(predictions, references)
            results.append({
                'model': model_name,
                'DER_wce_incl0': metrics['DER_case_yes_nodiac_yes'],
                'WER_wce_incl0': metrics['WER_case_yes_nodiac_yes'],
                'SER_wce_incl0': metrics['SER_case_yes_nodiac_yes'],
                'DER_woce_incl0': metrics['DER_case_no_nodiac_yes'],
                'WER_woce_incl0': metrics['WER_case_no_nodiac_yes'],
                'SER_woce_incl0': metrics['SER_case_no_nodiac_yes'],
                'DER_wce_excl0': metrics['DER_case_yes_nodiac_no'],
                'WER_wce_excl0': metrics['WER_case_yes_nodiac_no'],
                'SER_wce_excl0': metrics['SER_case_yes_nodiac_no'],
                'DER_woce_excl0': metrics['DER_case_no_nodiac_no'],
                'WER_woce_excl0': metrics['WER_case_no_nodiac_no'],
                'SER_woce_excl0': metrics['SER_case_no_nodiac_no'],
                'n_samples': metrics['n_samples'],
            })
        except Exception as e:
            print(f"ERROR processing {model_name}: {e}", file=sys.stderr)

    # Sort by DER (WCE, Incl 0) - the official metric
    results.sort(key=lambda x: x['DER_wce_incl0'])

    # Print ranked table
    print(f"\n{'Rank':<5} {'Model':<30} {'DER':>8} {'WER':>8} {'SER':>8}  |  {'DER(w/o CE)':>12} {'WER(w/o CE)':>12}")
    print("-" * 100)
    for i, r in enumerate(results, 1):
        print(f"{i:<5} {r['model']:<30} {r['DER_wce_incl0']:>7.2f}% {r['WER_wce_incl0']:>7.2f}% {r['SER_wce_incl0']:>7.2f}%  |  {r['DER_woce_incl0']:>11.2f}% {r['WER_woce_incl0']:>11.2f}%")

    # Save to CSV
    out_csv = os.path.join(os.path.dirname(__file__), 'dev_results_all_models.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved to {out_csv}")

if __name__ == '__main__':
    main()
