from pathlib import Path
from pypdf import PdfReader


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = BASE_DIR / "documents" / "rag_document.pdf"


# ============================================================
# READ PDF
# ============================================================

def read_pdf():

    if not PDF_PATH.exists():
        print("❌ PDF file not found!")
        print("Expected location:")
        print(PDF_PATH)
        return ""

    reader = PdfReader(str(PDF_PATH))

    full_text = ""

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            full_text += f"\n\n--- PAGE {page_number} ---\n\n"
            full_text += text

    return full_text


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    text = read_pdf()

    if text:

        print("\n✅ PDF read successfully!")

        print("\nTotal characters:", len(text))

        print("\n---------- FIRST PART OF DOCUMENT ----------\n")

        print(text[:3000])

        print("\n--------------------------------------------")

    else:

        print("❌ No text was extracted from the PDF.")