"""
Prompt templates for RAG system
Enhanced version from Law_chatbot_project_workshop3
"""
from typing import List

def build_law_prompt(user_question: str, context_snippets: List[str]) -> str:
    """
    Build prompt for law-related questions with context
    
    Args:
        user_question (str): User's question
        context_snippets (List[str]): Relevant context from documents
        
    Returns:
        str: Formatted prompt
    """
    context_text = "\n\n".join(context_snippets) if context_snippets else "Không có thông tin liên quan."
    
    return f"""Câu hỏi: {user_question}

Dựa vào tài liệu luật dưới đây, hãy trả lời chính xác và ngắn gọn. Nếu không tìm thấy thông tin liên quan, hãy trả lời "Không có thông tin" và đưa ra lời khuyên chung nếu có thể:

=== TÀI LIỆU THAM KHẢO ===
{context_text}

=== YÊU CẦU ===
- Trả lời dựa trên tài liệu được cung cấp
- Sử dụng ngôn ngữ chuyên nghiệp nhưng dễ hiểu
- Nếu câu hỏi không rõ ràng, hãy yêu cầu làm rõ

Trả lời:"""

def build_general_chat_prompt(user_question: str, context_snippets: List[str] = None) -> str:
    """
    Build prompt for general chat without specific context
    
    Args:
        user_question (str): User's question
        context_snippets (List[str], optional): Optional context
        
    Returns:
        str: Formatted prompt
    """
    if context_snippets:
        context_text = "\n\n".join(context_snippets)
        return f"""Câu hỏi: {user_question}

Thông tin tham khảo:
{context_text}

Hãy trả lời một cách hữu ích và chính xác dựa trên thông tin được cung cấp."""
    
    return user_question

def build_system_prompt() -> str:
    """
    Build system prompt for the assistant
    
    Returns:
        str: System prompt
    """
    return """Bạn là một trợ lý AI thông minh và hữu ích, chuyên về tư vấn pháp luật Việt Nam, đặc biệt là luật xử lý vi phạm hành chính.

NHIỆM VỤ:
- Trả lời các câu hỏi pháp lý dựa trên tài liệu được cung cấp
- Đưa ra lời khuyên pháp lý chính xác và thực tiễn
- Giải thích các điều luật một cách dễ hiểu

NGUYÊN TẮC:
- Luôn dựa trên tài liệu pháp lý chính thức
- Sử dụng ngôn ngữ chuyên nghiệp nhưng dễ hiểu
- Không đưa ra lời khuyên khi không có căn cứ pháp lý
- Khuyến khích tham khảo ý kiến luật sư khi cần thiết

ĐỊNH DẠNG TRẢLỜI:
- Trả lời trực tiếp câu hỏi
- Trích dẫn điều luật cụ thể nếu có
- Đưa ra ví dụ thực tế nếu phù hợp
- Kết thúc bằng lời khuyên thực tiễn"""

def build_search_prompt(query: str) -> str:
    """
    Build prompt for search query enhancement
    
    Args:
        query (str): Original search query
        
    Returns:
        str: Enhanced search query
    """
    # Add common legal terms and variations
    enhanced_query = query
    
    # Common legal term mappings
    term_mappings = {
        "phạt": ["xử phạt", "vi phạm", "chế tài"],
        "tiền": ["tiền phạt", "mức phạt", "số tiền"],
        "hành chính": ["vi phạm hành chính", "xử lý hành chính"],
        "xe": ["phương tiện", "giao thông"],
        "lái xe": ["điều khiển phương tiện", "người điều khiển"]
    }
    
    # Enhance query with related terms
    for key, related_terms in term_mappings.items():
        if key in query.lower():
            enhanced_query += " " + " ".join(related_terms)
    
    return enhanced_query
