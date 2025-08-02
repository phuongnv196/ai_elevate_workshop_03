import fitz

# Giả định một hàm để mô phỏng việc trích xuất văn bản từ PDF
# Hàm này không có điều kiện lọc độ dài chunk
def extract_all_chunks_from_text(text):
    """
    Trích xuất các đoạn văn bản từ một chuỗi văn bản, bao gồm cả các đoạn ngắn.
    
    Args:
        text (str): Chuỗi văn bản đầu vào.
    
    Returns:
        list: Danh sách các đoạn văn bản được trích xuất.
    """
    # Tách văn bản thành các đoạn dựa trên dấu xuống dòng kép
    # Chú ý: Không có điều kiện 'len(p.strip()) > 50' ở đây
    paragraphs = [p.strip() for p in text.split("\n\n")]
    
    return paragraphs

# --- Đoạn mã kiểm tra ---

# Chuỗi văn bản mẫu có cả đoạn dài và ngắn
sample_text = """Article 11. Cases not subject to administrative sanctioning 
"""

# Gọi hàm với chuỗi văn bản mẫu
chunks = extract_all_chunks_from_text(sample_text)

print("Kết quả trích xuất các đoạn văn bản:")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} (độ dài: {len(chunk)}):")
    print(f"'{chunk}'")
    print("---")

print("\n")
print("Phân tích:")
print("- Nếu kết quả bao gồm cả các đoạn 'Phần này là một đoạn rất ngắn.' và 'Ngắn.',")
print("  nghĩa là điều kiện 'len > 50' đã được loại bỏ thành công.")
print("- Hàm đã tách văn bản thành các đoạn và đưa tất cả vào danh sách.")

