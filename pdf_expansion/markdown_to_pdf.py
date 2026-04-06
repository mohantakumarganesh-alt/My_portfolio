import subprocess
import os

MARKDOWN_PATH = r"C:\\Users\\Ganesh\\Desktop\\portfolio\\pdf_expansion\\expanded_report.md"
OUTPUT_PDF = r"C:\\Users\\Ganesh\\Desktop\\portfolio\\pdf_expansion\\expanded_report.pdf"

# Ensure pandoc is installed; you may need to install it separately.

def convert_md_to_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")
    cmd = ["pandoc", md_path, "-o", pdf_path, "--pdf-engine=xelatex"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc conversion failed: {result.stderr}")
    print(f"Converted {md_path} to {pdf_path}")

if __name__ == "__main__":
    convert_md_to_pdf(MARKDOWN_PATH, OUTPUT_PDF)
