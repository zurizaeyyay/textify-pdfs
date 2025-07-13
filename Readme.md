# Prerequisites

# download Tesseract OCR
Windows: https://github.com/UB-Mannheim/tesseract/wiki
Macos/linux: brew install tesseract or sudo apt install tesseract-ocr

NOTE: Be sure to install addition language if not converting English (or converting multiple languages)

# download Ghostscript
https://ghostscript.com/releases/gsdnld.html

or brew install ghostscript

Python Packages:
See requirements.txt

# Basic Usage

ocrmypdf input.pdf output.pdf


# Bulk Usage

python bulk0cr.py [input directory] [output directory] -l eng -s -f

eg for arabic, running the script in current folder, skip existing text and force overwrite

python bulkOcr.py . results -l ara -s -f


# CLI Arguments
inputDir        Folder containing input .pdf files
outputDir       Folder for OCR’d output PDFs
-l --language   Tesseract language code (default: eng)
-s --skip       Skips OCR on pages that already have text (default: False)
-f --force      Force OCR on all pages, replacing existing text (default: False)
-j --jobs       Max parallel OCR jobs (defaults to CPU‑1 if unset)