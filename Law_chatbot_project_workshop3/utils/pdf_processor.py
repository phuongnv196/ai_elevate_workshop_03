import fitz  # PyMuPDF

def extract_chunks_from_pdf(file_path):
    doc = fitz.open(file_path)
    print(f"Số trang: {doc.page_count}")
    chunks = []
    for i, page in enumerate(doc):
        text = page.get_text()

        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]

        chunks.extend(paragraphs)

    return chunks