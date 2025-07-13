#!/usr/bin/env python3
import os
import glob
import time
import argparse
import multiprocessing
import tempfile
import subprocess

from pypdf import PdfReader
import ocrmypdf

# --- Thresholds for parallel OCR ---
PAGE_THRESHOLD = 10           # pages above which we consider parallel OCR
SIZE_THRESHOLD = 5 * 1024**2  # bytes above which we consider parallel OCR


def shouldUseParallel(pdfPath: str,
                      pageThreshold: int = PAGE_THRESHOLD,
                      sizeThreshold: int = SIZE_THRESHOLD):
    """
    Return True if PDF is large enough to warrant parallel OCR.
    Defaults: ≥10 pages or ≥5 MB.
    """
    try:
        reader = PdfReader(pdfPath)
        pageCount = len(reader.pages)
        fileSize = os.path.getsize(pdfPath)
        return (pageCount >= pageThreshold) or (fileSize >= sizeThreshold)
    except Exception:
        # If we can’t read it, just do single‑threaded
        return False

def removePdfBackground(inputPdf: str):
    """
    Use ImageMagick to strip faint backgrounds (lines/margins) from a PDF.
    Returns path to the cleaned temporary PDF.
    """
    baseName = os.path.splitext(os.path.basename(inputPdf))[0]
    tempDir = tempfile.gettempdir()
    cleanedPdf = os.path.join(tempDir, f"cleaned_{baseName}.pdf")
    # ImageMagick command:
    cmd = [
        "magick","-density", "500", inputPdf, # high density for better quality text
        "-colorspace", "Gray", # convert to grayscale, quicker happens anyway
        "-alpha", "off",
        "-blur", "0x2", # slight blur to help with jagged text
        "-threshold", "55%",
        cleanedPdf
    ]
    subprocess.run(cmd, check=True)
    return cleanedPdf



def bulkConvertPdfs(inputDir: str,
                    outputDir: str,
                    language: str = "eng",
                    maxJobs: int = None,
                    forceOverwrite: bool = False,
                    skipText: bool = True,
                    removeBackground: bool = False):
    
    # Ensure output directory exists
    os.makedirs(outputDir, exist_ok=True)
    pdfPaths = glob.glob(os.path.join(inputDir, "*.pdf"))
    total = len(pdfPaths)

    # Go through each PDF
    for idx, pdfPath in enumerate(pdfPaths, start=1):
        fileName = os.path.basename(pdfPath)
        outPath = os.path.join(outputDir, fileName)
        startTime = time.time()
        
        # Preprocess: optionally remove background if --remove-background is set
        processedPath = pdfPath
        cleanedPath = None
        if removeBackground:
            try:
                cleanedPath = removePdfBackground(pdfPath)
                processedPath = cleanedPath
                print(f"[{idx}/{total}] 🧹 Background removed for {fileName}")
            except Exception as e:
                print(f"[{idx}/{total}] ❌ Background removal failed: {e}")
                processedPath = pdfPath

        
        # Decide threading
        useParallel = bool(maxJobs and shouldUseParallel(pdfPath))
        jobs = maxJobs if useParallel else 1

        # Build OCR parameters based on flags
        ocr_params = {
            "language": language,
            "output_type": "pdf",   # you can also use "pdfa" for PDF/A
            "jobs": jobs}
        
        # Choose OCR mode: skip, force, or redo (default)
        if skipText and forceOverwrite:
            print("Warning: --skip and --force are mutually exclusive. Using --force instead.")
            ocr_params["force_ocr"] = True
        elif skipText:
            ocr_params["skip_text"] = True
        elif forceOverwrite:
            ocr_params["force_ocr"] = True
        else:
            ocr_params["redo_ocr"] = True  # Default behavior
            
        try:
            ocrmypdf.ocr(processedPath, outPath, **ocr_params)
            
            elapsed = time.time() - startTime
            mode = f"{jobs} jobs" if jobs > 1 else "single-thread"
            print(f"[{idx}/{total}] ✅ {fileName} ({mode}) in {elapsed:.1f}s")
        except Exception as e:
            print(f"[{idx}/{total}] ❌ {fileName}: {e}")
            
        # Cleanup temporary cleaned PDF
        if cleanedPath:
            try:
                os.remove(cleanedPath)
            except:
                pass
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bulk OCR PDFs into searchable PDFs, preserving drawings/images.")
    parser.add_argument("inputDir", help="Folder containing input .pdf files")
    parser.add_argument("outputDir", help="Folder for OCR’d output PDFs")
    parser.add_argument("-l", "--language",
                        default="eng", help="Tesseract language code (default: eng)")
    parser.add_argument("-s", "--skip", action="store_true",
                        help="Skip OCR on pages that already have text")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force OCR on all pages, replacing existing text")
    parser.add_argument(
        "--remove-background",
        action="store_true",
        help="Strip faint backgrounds (lines, margins) before OCR"
    )
    parser.add_argument("-j", "--jobs", type=int, default=None,
                        help="Max parallel OCR jobs (defaults to CPU‑1 if unset)")
    args = parser.parse_args()

    # If user didn’t set jobs set as half the cores (max 8). Falls back to 1 if single‑threaded
    if args.jobs is None:
        cpuCount = multiprocessing.cpu_count()
        args.jobs = min(8, max(1, cpuCount // 2))

    bulkConvertPdfs(
        inputDir=args.inputDir,
        outputDir=args.outputDir,
        language=args.language,
        maxJobs=args.jobs,
        forceOverwrite=args.force,
        skipText=args.skip,
        removeBackground=args.remove_background
    )
