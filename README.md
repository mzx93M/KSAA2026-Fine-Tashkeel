# Fine-Tashkeel at KSAA-2026: A Comprehensive Evaluation of Seq2Seq and Multimodal Approaches for Automatic Diacritization of Arabic Speech Dictation

<p align="center">
<img src="https://placehold.co/800x200/e8f5e9/2e7d32?text=Fine-Tashkeel+Arabic+Diacritization" alt="Arabic Text Diacritization">
</p>

This repository contains the official code and results for **Fine-Tashkeel**, our submission to **Task 2** of the **[KSAA-2026 Shared Task](https://www.codabench.org/competitions/11859/)** on Automatic Diacritization of Speech Dictation. We systematically evaluated **18 diacritization models** across Seq2Seq, token classification, decoder LLM, and ASR architectures, achieving **5th place** on the official leaderboard (DER 10.56%, WER 34.47%).

#### By: [Hassan Barmandah](https://scholar.google.com/citations?user=2VzOr0kAAAAJ&hl=en), [Fatimah Emad Eldin](https://scholar.google.com/citations?user=CfX6eA8AAAAJ&hl=ar), [Omer Nacar](https://scholar.google.com/citations?user=pezf5FYAAAAJ&hl=en) — NAMAA Community (with Umm Al-Qura University, Trouve Labs, Tuwaiq Academy)

[![Code](https://img.shields.io/badge/GitHub-Code-blue)](https://github.com/HasanBGit/KSAA2026-Fine-Tashkeel)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)](LICENSE)

---

## Model Description

This project treats diacritization as a **character-level sequence-to-sequence translation task**, mapping undiacritized text to its diacritized form. We evaluated **18 diverse models** spanning four architectural paradigms:

- **Text-only Seq2Seq**: Fine-Tashkeel (ByT5), Shakkelha, Shakkala
- **Text-only Classifiers**: ByT5 (glonor), FLAN-T5, Qwen-1.5, Mishkal, CAMeL-MLE
- **ASR+Text Multimodal**: Seamless M4T, ArTST, Whisper variants (large-v3, Tarteel, Quran LoRA)
- **Fine-tuned**: Tashkeel-700M, ByT5 (fine-tuned), Whisper-Tashkeel (fine-tuned)

Our best submission uses **Fine-Tashkeel** — a ByT5-based Seq2Seq model — in a zero-shot inference setting. A key finding is that text-only approaches substantially outperform multimodal ASR+Text models on this task.

### Key Contributions

* **Ranking & Performance**: **5th out of 7 teams** (DER 10.56%, WER 34.47%), competitive with the organizer's fine-tuned baseline (DER 9.91%) despite requiring no task-specific training
* **Systematic Comparison**: Evaluated 18 models across 4 architecture families — text-only Seq2Seq consistently outperforms off-the-shelf multimodal systems
* **Error Analysis**: Per-nationality breakdown across 9 Arabic dialects reveals significant variation (DER 3.70% for Egyptian vs. 13.73% for Algerian Arabic)
* **Multimodal Failure Analysis**: Demonstrated that ASR models (Whisper, ArTST) fail on diacritization due to task mismatch, domain gap, and error propagation

---

## 🚀 How to Use

You can use the Fine-Tashkeel model directly with the `transformers` library. The following example demonstrates inference on Arabic text.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load Fine-Tashkeel
model_name = "basharalrfooh/Fine-Tashkeel"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

# Diacritize Arabic text
text = "السلام عليكم ورحمة الله وبركاته"
inputs = tokenizer(text, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_length=512, num_beams=4)
diacritized = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(diacritized)
# Output: السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ
```

---

## ⚙️ Dataset

The dataset consists of approximately five hours of Arabic speech audio collected via **VoiceWall**, a crowdsourcing audio platform developed by the King Salman Global Academy for Arabic Language. Recordings were obtained from male and female speakers covering Modern Standard Arabic (MSA) and dialectal Arabic speech. All utterances are short (max 9 seconds) to support accurate speech-text alignment. The data underwent automatic validation and manual review to ensure audio quality, transcription accuracy, and diacritic consistency.

> **Important**: The use of any external data beyond the officially released training data is **prohibited**. The use of large language models (LLMs) is **strictly prohibited** — only small-scale models are allowed.

| Split | Samples | Duration | Gender (M/F) |
| :--- | :---: | :---: | :---: |
| **Train** | 2,327 | ~4.5h | 1,423 / 904 |
| **Dev** | 260 | ~0.5h | 161 / 99 |
| **Test** | 328 | ~0.5h | 222 / 104 |

### Nationality Distribution

| Nationality | Train | Dev | Test |
| :--- | :---: | :---: | :---: |
| Egypt | 1,026 | 114 | 173 |
| Saudi Arabia | 357 | 41 | 85 |
| Algeria | 239 | 28 | — |
| Qatar | 209 | 24 | 34 |
| Sudan | 189 | 19 | 10 |
| Bahrain | 114 | 13 | 8 |
| Kuwait | 109 | 12 | 2 |
| Palestine | 68 | 8 | 2 |
| Syria | 16 | 1 | 1 |
| Gaza | — | — | 13 |

---

## 📊 Evaluation Results

### Official Leaderboard (Blind Test)

The primary metric is **WER** (with case ending, including no diacritic). All values are percentages (%).

| Rank | Team | DER | WER | SER |
| :---: | :--- | :---: | :---: | :---: |
| 1st | meshal | 6.87 | 23.26 | 66.16 |
| 2nd | nadaadelmousa | 7.04 | 24.39 | 71.65 |
| 3rd | naif_alharthi | 7.51 | 25.34 | 73.48 |
| 4th | nahian_abu | 8.23 | 30.37 | 80.79 |
| **5th** | **Hassan (Ours)** | **10.56** | **34.47** | **79.88** |
| 6th | omarnj10 | 27.94 | 44.05 | 98.78 |
| 7th | astral_fate | 31.67 | 84.50 | 99.70 |

### Internal Model Comparison (Blind Test)

All 18 models evaluated, ranked by DER (%); links point to the base model or library used:

| Model | Link | Type | Method | DER | WER | SER |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Fine-Tashkeel** | [basharalrfooh/Fine-Tashkeel](https://huggingface.co/basharalrfooh/Fine-Tashkeel) | **Seq2Seq** | **Inference** | **10.56** | **34.47** | **79.88** |
| ASR-Tashkeel | Seamless M4T + Fine-Tashkeel | Seq2Seq | Pipeline | 10.70 | — | — |
| Shakkelha | [AliOsm/shakkelha](https://github.com/AliOsm/shakkelha) | Text-only | Inference | 13.14 | 39.47 | 83.84 |
| Shakkala | [Barqawiz/Shakkala](https://github.com/Barqawiz/Shakkala) | Text-only | Inference | 19.70 | 56.37 | 96.95 |
| CATT | [abjadai/catt](https://github.com/abjadai/catt) | Text-only | Inference | 28.34 | 48.17 | 100.00 |
| Tashkeel-700M | [Etherll/Tashkeel-700M](https://huggingface.co/Etherll/Tashkeel-700M) | Text-only | Fine-tune | 34.04 | 57.88 | 99.09 |
| FLAN-T5 | [Abdou/arabic-tashkeel-flan-t5-small](https://huggingface.co/Abdou/arabic-tashkeel-flan-t5-small) | Text-only | Inference | 37.80 | 59.64 | 100.00 |
| ArTST | [MBZUAI/artst_asr_v3](https://huggingface.co/MBZUAI/artst_asr_v3) | ASR+Text | Inference | 42.82 | 65.94 | 85.06 |
| Seamless M4T | [facebook/seamless-m4t-v2-large](https://huggingface.co/facebook/seamless-m4t-v2-large) | ASR+Text | Inference | 43.01 | 56.57 | 100.00 |
| CAMeL-MLE | [camel-tools](https://github.com/CAMeL-Lab/camel_tools) | Text-only | Inference | 45.89 | 82.39 | 100.00 |
| ByT5 Glonor | [glonor/byt5-arabic-diacritization](https://huggingface.co/glonor/byt5-arabic-diacritization) | Text-only | Inference | 46.96 | 69.64 | 100.00 |
| Whisper-Tashkeel | [openai/whisper-small](https://huggingface.co/openai/whisper-small) + Fine-Tashkeel | ASR+Text | Fine-tune | 54.61 | 67.68 | 99.39 |
| ByT5 Glonor | [glonor/byt5-arabic-diacritization](https://huggingface.co/glonor/byt5-arabic-diacritization) | Text-only | Fine-tune | 54.15 | 77.57 | 100.00 |
| Qwen-1.5 | [Bisher/...Qwen2.5-1.5B](https://huggingface.co/Bisher/train_run-Qwen2.5-1.5B-Instruct-fadel-full-arabic-diacritization) | Text-only | Inference | 62.56 | 75.75 | 97.87 |
| Mishkal | [linuxscout/mishkal](https://github.com/linuxscout/mishkal) | Text-only | Inference | 76.76 | 90.49 | 99.39 |
| Whisper (large-v3) | [openai/whisper-large-v3](https://huggingface.co/openai/whisper-large-v3) | ASR+Text | Inference | 84.71 | 99.60 | 100.00 |
| Tarteel Whisper | [tarteel-ai/whisper-base-ar-quran](https://huggingface.co/tarteel-ai/whisper-base-ar-quran) | ASR+Text | Inference | 84.93 | 85.08 | 100.00 |
| Whisper Quran LoRA | [openai/whisper-base](https://huggingface.co/openai/whisper-base) + LoRA | ASR+Text | Inference | 97.36 | 99.98 | 100.00 |
| mT5-base | [google/mt5-base](https://huggingface.co/google/mt5-base) | Text-only | Inference | 99.74 | 99.97 | 100.00 |

### Text-only vs. Multimodal

| Category | Avg. DER | Best DER |
| :--- | :---: | :---: |
| Text-only (Inference) | 44.15 | 10.56 |
| ASR+Text (Inference) | 70.57 | 42.82 |
| Text-only (Fine-tuned) | 44.10 | 34.04 |
| ASR+Text (Fine-tuned) | 54.61 | 54.61 |

### Per-Nationality Breakdown (Fine-Tashkeel, Dev Set)

| Nationality | N | DER (WCE) | WER (WCE) | SER (WCE) | DER (w/o CE) | WER (w/o CE) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Egypt | 114 | 3.70 | 9.01 | 42.98 | 4.88 | 15.62 |
| Palestine | 8 | 4.71 | 12.66 | 75.00 | 14.67 | 55.70 |
| Kuwait | 12 | 5.75 | 14.86 | 50.00 | 15.49 | 53.38 |
| Syria | 1 | 5.65 | 12.50 | 100.00 | 16.03 | 62.50 |
| Qatar | 24 | 8.74 | 20.45 | 87.50 | 19.63 | 58.47 |
| Saudi Arabia | 41 | 10.49 | 28.67 | 90.24 | 18.17 | 60.37 |
| Sudan | 19 | 10.86 | 30.08 | 89.47 | 17.20 | 57.32 |
| Bahrain | 13 | 11.17 | 34.87 | 92.31 | 18.98 | 61.18 |
| Algeria | 28 | 13.73 | 35.05 | 92.86 | 20.79 | 62.70 |
| **Overall** | **260** | **8.10** | **20.46** | **67.31** | **13.86** | **43.66** |

---

## 📁 Repository Structure

```
KSAA2026-Fine-Tashkeel/
├── LICENSE
├── README.md
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── diacritization.py          # Shared utilities: metrics, post-processing, ensemble
│   └── diac_evaluation.py         # Official evaluation metrics (DER/WER/SER)
├── analysis/
│   ├── dev_results_all_models.csv  # Full dev set evaluation (31 model variants)
│   ├── per_nationality_results.csv # Per-nationality breakdown
│   ├── eval_dev_all_models.py      # Evaluation script for all models
│   ├── eval_per_nationality.py     # Per-nationality analysis
│   ├── error_examples.py           # Error analysis for Fine-Tashkeel
│   └── generate_figures.py         # Publication-ready figures
└── notebooks/
    ├── 00_submission_creator.ipynb  # Results aggregation & submission
    ├── 01–25 ...                   # 38 notebooks total
    └── 25_apply_fine_tashkeel.ipynb # Final submission application
```

---

## 📓 Notebooks

The `notebooks/` directory contains **38 Jupyter notebooks** covering training (11 notebooks) and inference (27 notebooks) for all 18 models evaluated.

### Inference Notebooks

| # | Notebook | Model | Link | Type | Notes |
|---|----------|-------|------|------|-------|
| 00 | `00_submission_creator.ipynb` | Results Aggregator | — | Utility | Collects all predictions, computes metrics, creates submissions |
| 01 | `01_infer_fine_tashkeel.ipynb` | Fine-Tashkeel | [basharalrfooh/Fine-Tashkeel](https://huggingface.co/basharalrfooh/Fine-Tashkeel) | Seq2Seq | ByT5 byte-level — **our best model** |
| 02 | `02_infer_mushkil_arat5.ipynb` | Mushkil | [riotu-lab/mushkil](https://huggingface.co/riotu-lab/mushkil) | Seq2Seq | AraT5v2-based |
| 03 | `03_infer_flan_t5_tashkeel.ipynb` | FLAN-T5 Arabic Tashkeel | [Abdou/arabic-tashkeel-flan-t5-small](https://huggingface.co/Abdou/arabic-tashkeel-flan-t5-small) | Seq2Seq | Instruction-tuned T5 |
| 04 | `04_infer_catt_tashkeel.ipynb` | CATT | `pip install git+https://github.com/abjadai/catt.git` | Seq2Seq | Character-level Transformer |
| 05 | `05_infer_arat5_base.ipynb` | AraT5-base | [UBC-NLP/AraT5-base](https://huggingface.co/UBC-NLP/AraT5-base) | Seq2Seq | Arabic-specific T5 |
| 06 | `06_infer_arabert_token.ipynb` | AraBERT | [aubmindlab/bert-base-arabertv2](https://huggingface.co/aubmindlab/bert-base-arabertv2) | Token Cls. | BERT-based |
| 07 | `07_infer_marbert.ipynb` | MARBERT / AraT5-MSA | [UBC-NLP/AraT5-msa-base](https://huggingface.co/UBC-NLP/AraT5-msa-base) | Seq2Seq | MSA-specific |
| 08 | `08_infer_sadeed.ipynb` | Sadeed / Qwen | [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | Decoder LLM | Small Arabic LLM |
| 09 | `09_infer_whisper_multimodal.ipynb` | Whisper + Fine-Tashkeel | [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) | ASR+Seq2Seq | Multimodal pipeline |
| 10 | `10_infer_tarteel_whisper_quran.ipynb` | Tarteel Whisper Quran | [tarteel-ai/whisper-base-ar-quran](https://huggingface.co/tarteel-ai/whisper-base-ar-quran) | ASR | Quranic Arabic |
| 11 | `11_infer_mt5_arabic.ipynb` | mT5-base | [google/mt5-base](https://huggingface.co/google/mt5-base) | Seq2Seq | Multilingual T5 |
| 11 | `11_infer_diac_text_asr.ipynb` | Diac Text + ASR | [rufaelfekadu/diac-transformer-...](https://huggingface.co/rufaelfekadu/diac-transformer-text-asr-tashkeela-clartts-kssa) | ASR+Text | Combined pipeline |
| 12 | `12_infer_byt5_glonor.ipynb` | ByT5 | [glonor/byt5-arabic-diacritization](https://huggingface.co/glonor/byt5-arabic-diacritization) | Seq2Seq | ByT5 0.3B params |
| 13 | `13_infer_ensemble_voting.ipynb` | Ensemble (Majority Voting) | — | Ensemble | Character-level voting |
| 14 | `14_infer_ensemble_weighted.ipynb` | Ensemble (WER-Weighted) | — | Ensemble | Weighted by model WER |
| 15 | `15_infer_postprocess_rules.ipynb` | Post-processing Rules | — | Post-proc. | Linguistic rule-based refinement |
| 16 | `16_infer_qwen_diacritization.ipynb` | Qwen Diacritization | [Bisher/train_run-Qwen2.5-1.5B-Instruct-fadel-full-arabic-diacritization](https://huggingface.co/Bisher/train_run-Qwen2.5-1.5B-Instruct-fadel-full-arabic-diacritization) | Decoder LLM | Fine-tuned on Fadel dataset |
| 17 | `17_infer_whisper_quran_lora.ipynb` | Whisper Quran LoRA | [tarteel-ai/whisper-base-ar-quran](https://huggingface.co/tarteel-ai/whisper-base-ar-quran) | ASR | LoRA adapter (fallback) |
| 18 | `18_infer_seamless_m4t.ipynb` | Seamless M4T | [facebook/seamless-m4t-v2-large](https://huggingface.co/facebook/seamless-m4t-v2-large) | ASR+Text | Multilingual multimodal |
| 19 | `19_infer_artst_asr.ipynb` | ArTST v3 | [MBZUAI/artst_asr_v3](https://huggingface.co/MBZUAI/artst_asr_v3) | ASR | SpeechT5-based |
| 20 | `20_infer_shakkala.ipynb` | Shakkala | [Barqawiz/Shakkala](https://github.com/Barqawiz/Shakkala) | Text-only | LSTM-based (via arabic_vocalizer) |
| 21 | `21_infer_shakkelha.ipynb` | Shakkelha | [AliOsm/shakkelha](https://github.com/AliOsm/shakkelha) | Text-only | RNN-based (via arabic_vocalizer) |
| 22 | `22_infer_camel_mle.ipynb` | CAMeL-MLE | [CAMeL-Lab/camel_tools](https://github.com/CAMeL-Lab/camel_tools) | Text-only | MLE morphological analyzer |
| 23 | `23_infer_mishkal.ipynb` | Mishkal | [linuxscout/mishkal](https://github.com/linuxscout/mishkal) | Text-only | Rule-based diacritization |
| 24 | `24_infer_asr_tashkeel.ipynb` | ASR-Tashkeel | Seamless M4T + Fine-Tashkeel | ASR+Seq2Seq | Combined ASR pipeline |
| 25 | `25_apply_fine_tashkeel.ipynb` | Fine-Tashkeel | [basharalrfooh/Fine-Tashkeel](https://huggingface.co/basharalrfooh/Fine-Tashkeel) | Seq2Seq | Final submission application |

### Training Notebooks

| # | Notebook | Model |
|---|----------|-------|
| 01 | `01_train_fine_tashkeel.ipynb` | Fine-Tashkeel fine-tuning |
| 02 | `02_train_artst_asr.ipynb` | ArTST ASR fine-tuning |
| 03 | `03_train_catt_tashkeel.ipynb` | CATT fine-tuning |
| 04 | `04_train_mushkil_arat5.ipynb` | Mushkil/AraT5 fine-tuning |
| 05 | `05_train_fine_tashkeel.ipynb` | Fine-Tashkeel (alt. config) |
| 06 | `06_train_tashkeel_700m.ipynb` | Tashkeel-700M fine-tuning |
| 07 | `07_train_byt5_glonor.ipynb` | ByT5 glonor fine-tuning |
| 08 | `08_train_artst_v3.ipynb` | ArTST v3 fine-tuning |
| 09 | `09_train_whisper_tashkeel.ipynb` | Whisper-Tashkeel fine-tuning |
| 10 | `10_train_catt_whisper_fusion.ipynb` | CATT+Whisper fusion |
| 24 | `24_train_infer.ipynb` | Combined train+infer pipeline |

### Model Types

**Seq2Seq Models** — Text-to-text models mapping undiacritized to diacritized text:
- ByT5-based: Fine-Tashkeel, glonor/byt5-arabic-diacritization
- T5-based: AraT5, mT5, FLAN-T5, Mushkil
- Character-level: CATT

**ASR Models** — Speech recognition models outputting diacritized transcriptions:
- Whisper-based: Tarteel Quran, Whisper LoRA, Whisper large-v3
- SpeechT5-based: ArTST v3
- Multilingual: Seamless M4T

**Token Classification** — Predict diacritic class per character/token:
- AraBERT

**Decoder LLMs** — Instruction-following models:
- Qwen2.5 (Bisher's fine-tuned), Sadeed

### Metrics

| Metric | Description | Primary? |
|--------|-------------|----------|
| **WER** | Word Error Rate — word wrong if any diacritic incorrect | **YES** |
| **DER** | Diacritic Error Rate — per-character accuracy | No |
| **SER** | Sentence Error Rate — sentence wrong if any error | No |

Metrics are computed with and without I'rab (case endings), and including/excluding positions with no diacritic.

### Output Format

```json
[
  {"id": "utt_00123", "text_diacritized": "النص المُشَكَّل هنا"},
  {"id": "utt_00124", "text_diacritized": "هَذا نَصٌّ مُشَكَّلٌ آخَر"}
]
```

---

## ⚠️ Limitations

* **Zero-Shot Only**: We did not successfully fine-tune Fine-Tashkeel on the shared task data due to convergence issues, relying on zero-shot inference
* **Text-Only**: As a text-only approach, the system cannot leverage acoustic cues that could disambiguate homographs
* **Nationality Bias**: Performance varies significantly across nationalities (DER 3.70% Egyptian vs. 13.73% Algerian), reflecting training data distribution
* **Dev-Test Divergence**: Some models show strong dev set performance that does not transfer to the blind test, likely due to the small dev set size (260 samples)
* **Dataset Scale**: Evaluation is limited to the relatively small VoiceWall dataset (~5 hours); generalization to other domains remains untested

---

## 🙏 Acknowledgements

We thank the **King Salman Global Academy for Arabic Language** for providing the VoiceWall dataset and organizing the shared task. We also acknowledge the baseline implementations provided by the organizers, and the developers of Fine-Tashkeel, CATT, Shakkelha, Shakkala, and all open-source models evaluated in this work.

### Related Links

* [KSAA-2026 Shared Task (CodaBench)](https://www.codabench.org/competitions/11859/)
* [OSACT7 Workshop at LREC 2026](https://lrec2026.info/)
* [Fine-Tashkeel Model](https://huggingface.co/basharalrfooh/Fine-Tashkeel)

---

## 📜 Citation

If you use this work, please cite the paper:

```bibtex
@inproceedings{barmandah2026finetashkeel,
    title={{Fine-Tashkeel at KSAA-2026: A Comprehensive Evaluation of Seq2Seq and Multimodal Approaches for Automatic Diacritization of Arabic Speech Dictation}},
    author={Barmandah, Hassan and Eldin, Fatimah Emad and Nacar, Omer},
    year={2026},
    booktitle={Proceedings of LREC 2026},
    note={KSAA-2026 Shared Task, OSACT7 Workshop}
}
```

---

## 📄 License

This project is licensed under the Apache 2.0 License.
