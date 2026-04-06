import os
import PyPDF2

PDF_PATH = r"C:\\Users\\Ganesh\\Downloads\\Effects of Agricultural Mechanization on Rural Employment.pdf"
OUTPUT_TEXT = "original_text.txt"

def extract_text_and_pages(pdf_path, output_text_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        num_pages = len(reader.pages)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        full_text = "\n\n".join(text)
    with open(output_text_path, "w", encoding="utf-8") as out:
        out.write(full_text)
    return num_pages, full_text

if __name__ == "__main__":
    pages, _ = extract_text_and_pages(PDF_PATH, OUTPUT_TEXT)
    print(f"Extracted {pages} pages. Text saved to {OUTPUT_TEXT}")
