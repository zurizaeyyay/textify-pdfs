# Background Info
I had several old S-Note files (Samsung notes in their weird xml/priopritary format).

I wanted to back them up in sensible format.

They were simple enough to convert to PDF through Samsung's S-Note program, 
but all the text was input as images in the result PDF's

To fix that i developed this python script to convert image pdfs using Tesseract and also removing the yellow page backgrounds from the PDF's using ImageMagick
The result is a clean PDF note with selectable text and no background. Created in bulk.

Possible extensions:

- Use numpy during the preprossessing step in combination or instead of Imagemagic for better results across varying pdfs

- For extremly large PDF's split into parts first and process in parallel before merging into final processed PDF.


# Prerequisites

# Download Tesseract OCR
Windows: https://github.com/UB-Mannheim/tesseract/wiki

Macos/linux: brew install tesseract or sudo apt install tesseract-ocr

NOTE: Be sure to install addition language if not converting English (or converting multiple languages)

# Download Ghostscript
https://ghostscript.com/releases/gsdnld.html

or brew install ghostscript

# Download ImageMagick (if background removal wanted)
- Install the Win64 dynamic at 16bits HDR enabled (should be first option)

https://imagemagick.org/script/download.php#windows

or on macos/linux

- brew install imagemagick or sudo apt install imagemagick

# Install Python Packages:

See requirements.txt


# Basic Usage

ocrmypdf input.pdf output.pdf


# Bulk Usage

python bulk0cr.py [options]... [input directory] [output directory]

    python "pathtosrcfile\.\bulk0cr.py" -f "original notes" "results"


eg for arabic, running the script in current folder, skip existing text and removebackground

    python bulkOcr.py -l ara -s  --remove-background . results




# CLI Arguments
(Note: input and output directory should be at the end of command)

    inputDir                Folder containing input .pdf files
    
    outputDir               Folder for OCR’d output PDFs
    
    -l --language           Tesseract language code (default: eng)
    
    -s --skip               Skips OCR on pages that already have text (default: False)
    
    -f --force              Force OCR on all pages, replacing existing text (default: False)
    
    --remove-background     Strip backgrounds (lines, margins) before OCR. 
    
        NOTE: Image will output in greyscale. Convertion will also be much slower
        "--force" option is recommended if removing background
    
    -j --jobs               Max parallel OCR jobs (defaults to either 1 or half cores if unset)
