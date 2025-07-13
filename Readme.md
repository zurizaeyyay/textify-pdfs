# Prerequisites

# download Tesseract OCR
Windows: https://github.com/UB-Mannheim/tesseract/wiki
Macos/linux: brew install tesseract or sudo apt install tesseract-ocr

NOTE: Be sure to install addition language if not converting English (or converting multiple languages)

# download Ghostscript
https://ghostscript.com/releases/gsdnld.html

or brew install ghostscript

# download ImageMagick (if background removal wanted)
    - Install the Win64 dynamic at 16bits HDR enabled (should be first option)
    https://imagemagick.org/script/download.php#windows

or on macos/linux
    - brew install imagemagick or sudo apt install imagemagick


Python Packages:
See requirements.txt

# Basic Usage

ocrmypdf input.pdf output.pdf


# Bulk Usage

python bulk0cr.py [input directory] [output directory] [options]...
python "pathtosrcfile\.\bulk0cr.py" -f "original notes" "results"

eg for arabic, running the script in current folder, skip existing text and removebackground
python bulkOcr.py -l ara -s . results --remove-background



# CLI Arguments
inputDir                Folder containing input .pdf files
outputDir               Folder for OCR’d output PDFs
-l --language           Tesseract language code (default: eng)
-s --skip               Skips OCR on pages that already have text (default: False)
-f --force              Force OCR on all pages, replacing existing text (default: False)
--remove-background     Strip backgrounds (lines, margins) before OCR. Image will output in greyscale
-j --jobs               Max parallel OCR jobs (defaults to either 1 or half cores if unset)