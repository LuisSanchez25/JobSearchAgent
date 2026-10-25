import unicodedata
from pathlib import Path
from pypdf import PdfReader
import re

CACHE = Path("cache")
CACHE.mkdir(exist_ok=True)              # create the folder if it's missing

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[•●▪◦■►\uf0b7]", "-", text)   # unify bullet symbols
    text = re.sub(r"[ \t]+", " ", text)            # collapse runs of spaces
    text = re.sub(r" *\n *", "\n", text)           # trim spaces around line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)         # at most one blank line in a row
    return text.strip()

def extract_pdf(path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages) 

def get_text(pdf_path):
    out = CACHE / (pdf_path.stem + ".txt")    # resumes/ml.pdf -> cache/ml.txt
    # Reuse the saved text if it's newer than the PDF
    if out.exists() and out.stat().st_mtime > pdf_path.stat().st_mtime:
        return out.read_text(encoding="utf-8")
    text = clean_text(extract_pdf(pdf_path)) #reader.pages[0].extract_text()
    out.write_text(text, encoding="utf-8")
    return text

if __name__ ==  "__main__":
    for pdf_path in Path("resumes").glob("*.pdf"):
        text = get_text(pdf_path)
        print(pdf_path.name, len(text), "characters")