import os
import sys

OUTLINE_PATH = r"C:\\Users\\Ganesh\\Desktop\\portfolio\\pdf_expansion\\expanded_outline.md"
OUTPUT_MD = r"C:\\Users\\Ganesh\\Desktop\\portfolio\\pdf_expansion\\expanded_report.md"

PLACEHOLDER_TEXT = "(This section will be expanded with detailed analysis, data, and discussion.)"

def read_outline(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    # Assume each line starts with a number and title
    sections = []
    for line in lines:
        if ". " in line:
            title = line.split('. ', 1)[1]
            sections.append(title)
    return sections

def generate_report(sections, output_path):
    with open(output_path, "w", encoding="utf-8") as out:
        for idx, title in enumerate(sections, start=1):
            out.write(f"# {title}\n\n")
            out.write(f"{PLACEHOLDER_TEXT}\n\n")

if __name__ == "__main__":
    if not os.path.exists(OUTLINE_PATH):
        sys.exit(f"Outline not found: {OUTLINE_PATH}")
    secs = read_outline(OUTLINE_PATH)
    generate_report(secs, OUTPUT_MD)
    print(f"Generated expanded report markdown at {OUTPUT_MD}")
