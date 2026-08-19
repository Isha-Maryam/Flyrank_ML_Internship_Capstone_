import os

pdf_path = "docs/flyrank-seo-research-march-2026.pdf"
txt_path = "docs/flyrank-seo-research-march-2026.txt"

try:
    import pypdf
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages):
        text += f"\n--- Page {idx + 1} ---\n"
        text += page.extract_text()
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Success! PDF text extracted to docs/flyrank-seo-research-march-2026.txt")
except Exception as e:
    print("Error:", e)
