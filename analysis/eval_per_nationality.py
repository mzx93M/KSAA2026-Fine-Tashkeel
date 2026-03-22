#!/usr/bin/env python3
"""Per-nationality error analysis on dev set for Fine-Tashkeel."""
import json
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from diac_evaluation import calculate_der, calculate_wer, calculate_ser

BASE = os.path.join(os.path.dirname(__file__), '..')
REF_PATH = os.path.join(BASE, 'Public_Data_TrainDev', 'dev input-output', 'Dev_output.json')
DEV_LIST = os.path.join(BASE, 'Public_Data_TrainDev', 'Dev', 'dev_list.tsv')
PRED_PATH = os.path.join(BASE, 'outputs', 'fine_tashkeel_dev_predictions.json')

# Normalize nationality labels
NAT_MAP = {
    'sudia': 'Saudi', 'Saudi': 'Saudi',
    'Egypt': 'Egypt',
    'Qatar': 'Qatar',
    'GzaEr': 'Gaza', 'Gazer': 'Gaza',
    'sudan': 'Sudan',
    'Bahriin': 'Bahrain',
    'Kwit': 'Kuwait',
    'Sriya': 'Syria',
    'Algeria': 'Algeria',
    'plastin': 'Palestine',
}

def main():
    with open(REF_PATH, 'r', encoding='utf-8') as f:
        references = json.load(f)
    ref_lookup = {r['id']: r['text_diacritized'] for r in references}

    with open(PRED_PATH, 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    pred_lookup = {p['id']: p['text_diacritized'] for p in predictions}

    # Parse dev_list.tsv for metadata
    metadata = {}
    with open(DEV_LIST, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            stem = row['stem']
            nat = NAT_MAP.get(row.get('nationality', ''), row.get('nationality', 'Unknown'))
            gender = row.get('gender', 'Unknown')
            metadata[stem] = {'nationality': nat, 'gender': gender}

    # Group samples by nationality
    nat_groups = {}
    gender_groups = {}
    for sample_id in ref_lookup:
        if sample_id not in pred_lookup:
            continue
        # Try to match sample_id to metadata stem
        matched_nat = 'Unknown'
        matched_gender = 'Unknown'
        for stem, meta in metadata.items():
            if stem in sample_id or sample_id.startswith(stem):
                matched_nat = meta['nationality']
                matched_gender = meta['gender']
                break

        nat_groups.setdefault(matched_nat, {'pred': [], 'ref': []})
        nat_groups[matched_nat]['pred'].append(pred_lookup[sample_id])
        nat_groups[matched_nat]['ref'].append(ref_lookup[sample_id])

        gender_groups.setdefault(matched_gender, {'pred': [], 'ref': []})
        gender_groups[matched_gender]['pred'].append(pred_lookup[sample_id])
        gender_groups[matched_gender]['ref'].append(ref_lookup[sample_id])

    # Compute per-nationality metrics
    print("\n=== Per-Nationality Results (Dev Set, Fine-Tashkeel) ===")
    print(f"{'Nationality':<15} {'Count':>6} {'DER(WCE)':>10} {'WER(WCE)':>10} {'SER(WCE)':>10} {'DER(w/oCE)':>10} {'WER(w/oCE)':>10}")
    print("-" * 80)

    nat_results = []
    for nat in sorted(nat_groups.keys()):
        g = nat_groups[nat]
        n = len(g['pred'])
        der_wce = calculate_der(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        wer_wce = calculate_wer(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        ser_wce = calculate_ser(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        der_woce = calculate_der(g['pred'], g['ref'], case_ending=False, no_diacritic=True)
        wer_woce = calculate_wer(g['pred'], g['ref'], case_ending=False, no_diacritic=True)
        print(f"{nat:<15} {n:>6} {der_wce:>9.2f}% {wer_wce:>9.2f}% {ser_wce:>9.2f}% {der_woce:>9.2f}% {wer_woce:>9.2f}%")
        nat_results.append({'nationality': nat, 'count': n, 'DER_WCE': der_wce, 'WER_WCE': wer_wce, 'SER_WCE': ser_wce, 'DER_woCE': der_woce, 'WER_woCE': wer_woce})

    print("\n=== Per-Gender Results ===")
    print(f"{'Gender':<15} {'Count':>6} {'DER(WCE)':>10} {'WER(WCE)':>10} {'SER(WCE)':>10}")
    print("-" * 50)
    for gender in sorted(gender_groups.keys()):
        g = gender_groups[gender]
        n = len(g['pred'])
        der = calculate_der(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        wer = calculate_wer(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        ser = calculate_ser(g['pred'], g['ref'], case_ending=True, no_diacritic=True)
        print(f"{gender:<15} {n:>6} {der:>9.2f}% {wer:>9.2f}% {ser:>9.2f}%")

    # Save
    out_csv = os.path.join(os.path.dirname(__file__), 'per_nationality_results.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=nat_results[0].keys())
        writer.writeheader()
        writer.writerows(nat_results)
    print(f"\nSaved to {out_csv}")

if __name__ == '__main__':
    main()
