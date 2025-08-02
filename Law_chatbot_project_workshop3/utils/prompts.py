def build_prompt(user_question, context_snippets):
    context_text = "\n".join(context_snippets)
    return f"""Câu hỏi: {user_question}

Dựa vào tài liệu luật dưới đây, hãy trả lời chính xác và ngắn gọn. nếu không tìm thấy thông tin, hãy trả lời "Không có thông tin".:

{context_text}
"""
