# ========== IMPORTS ==========
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from flask import Blueprint, request, jsonify
from tinydb import Query
from openai import OpenAI
import logging

# Import config và database
from config import Config
from database import db_manager

# Import function calling services
from services.function_calling_service import (
    get_tech_news, 
    read_data_file, 
    summarize_information, 
    function_tools
)

# ========== LOGGER SETUP ==========
logger = logging.getLogger(__name__)

# ========== BLUEPRINT SETUP ==========
conversation_bp = Blueprint('conversation', __name__)

# ========== DATABASE INITIALIZATION ==========
# Sử dụng database manager
conversations_db = db_manager.get_conversations_db()
messages_db = db_manager.get_messages_db()

# ========== CLIENT INITIALIZATION ==========
try:
    client = OpenAI(
        base_url=Config.OPENAI_BASE_URL,
        api_key=Config.OPENAI_API_KEY
    ) if Config.OPENAI_API_KEY else None
except Exception as e:
    logger.error("Vui lòng đảm bảo các biến môi trường OPENAI_API_KEY, OPENAI_BASE_URL đã được thiết lập.")
    client = None

# ========== CONVERSATION ROUTES ==========

@conversation_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Lấy danh sách tất cả conversations"""
    try:
        conversations = conversations_db.all()
        
        # Sắp xếp conversations theo thời gian tạo từ mới nhất đến cũ nhất
        conversations.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            "success": True,
            "conversations": conversations
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """Tạo conversation mới"""
    try:
        data = request.get_json()
        conversation_id = str(uuid.uuid4())
        
        conversation = {
            "id": conversation_id,
            "title": data.get("title", f"Cuộc trò chuyện {datetime.now().strftime('%H:%M %d/%m')}"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "message_count": 0
        }
        
        conversations_db.insert(conversation)
        
        return jsonify({
            "success": True,
            "conversation": conversation
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Xóa conversation và tất cả messages của nó"""
    try:
        Conversation = Query()
        Message = Query()
        
        # Xóa conversation
        conversations_db.remove(Conversation.id == conversation_id)
        
        # Xóa tất cả messages của conversation
        messages_db.remove(Message.conversation_id == conversation_id)
        
        return jsonify({
            "success": True,
            "message": "Conversation đã được xóa"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations/<conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """Cập nhật thông tin conversation (title)"""
    try:
        data = request.get_json()
        new_title = data.get("title")
        
        if not new_title or new_title.strip() == "":
            return jsonify({
                "success": False,
                "error": "Title không được để trống"
            }), 400
        
        Conversation = Query()
        conversation = conversations_db.search(Conversation.id == conversation_id)
        
        if not conversation:
            return jsonify({
                "success": False,
                "error": "Conversation không tồn tại"
            }), 404
        
        # Cập nhật title và updated_at
        conversations_db.update(
            {
                "title": new_title.strip(),
                "updated_at": datetime.now().isoformat()
            },
            Conversation.id == conversation_id
        )
        
        # Lấy conversation đã cập nhật
        updated_conversation = conversations_db.search(Conversation.id == conversation_id)[0]
        
        return jsonify({
            "success": True,
            "message": "Conversation title đã được cập nhật",
            "conversation": updated_conversation
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """Lấy tất cả messages trong một conversation"""
    try:
        Message = Query()
        messages = messages_db.search(Message.conversation_id == conversation_id)
        
        # Sắp xếp theo thời gian
        messages.sort(key=lambda x: x['timestamp'])
        
        return jsonify({
            "success": True,
            "messages": messages
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations/<conversation_id>/chat', methods=['POST'])
def chat(conversation_id):
    """Gửi tin nhắn và nhận phản hồi từ AI"""
    try:
        if not client:
            return jsonify({
                "success": False,
                "error": "OpenAI client chưa được khởi tạo"
            }), 500
        
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message không được để trống"
            }), 400
        
        # Lưu tin nhắn của user
        user_msg = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        }
        messages_db.insert(user_msg)
        
        # Lấy lịch sử conversation
        Message = Query()
        conversation_messages = messages_db.search(Message.conversation_id == conversation_id)
        conversation_messages.sort(key=lambda x: x['timestamp'])
        
        # Chuẩn bị messages cho OpenAI
        openai_messages = [
            {"role": "system", "content": """Bạn là một AI Technical Support Assistant chuyên về công nghệ và kỹ thuật. 

            🎯 **NHIỆM VỤ CHÍNH:**
            1. Trả lời các câu hỏi về công nghệ, lập trình, kỹ thuật
            2. Lấy và phân tích tin tức công nghệ mới nhất
            3. Đọc và phân tích file dữ liệu kỹ thuật
            4. Tóm tắt thông tin liên quan đến technology
            
            🚫 **LOẠI TRỪ THÔNG TIN KHÔNG LIÊN QUAN:**
            - Tin tức giải trí, thể thao, chính trị
            - Thông tin không có tính kỹ thuật
            - Nội dung không liên quan đến technology, IT, khoa học
            - Quảng cáo, marketing không có yếu tố tech
            
            ✅ **CHỈ TẬP TRUNG VÀO:**
            - Công nghệ thông tin (IT, Software, Hardware)
            - Khoa học máy tính và AI
            - Lập trình và phát triển phần mềm
            - Cybersecurity và bảo mật
            - Cloud computing, DevOps
            - IoT, Blockchain, Data Science
            - Mobile development, Web development
            - Startup công nghệ và innovation
            
            Khi gặp câu hỏi không liên quan đến công nghệ, hãy lịch sự chuyển hướng về chủ đề technical."""}
        ]
        
        # Thêm lịch sử conversation (giới hạn 10 tin nhắn gần nhất)
        for msg in conversation_messages[-20:]:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Gọi OpenAI API với function calling
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=openai_messages,
            tools=function_tools,
            tool_choice="auto",
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE
        )
        
        response_message = response.choices[0].message
        assistant_content = ""
        
        # Xử lý function calling
        if response_message.tool_calls:
            assistant_content += "🔧 Đang thực hiện các chức năng được yêu cầu...\n\n"
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Thực hiện function call
                if function_name == "get_tech_news":
                    result = get_tech_news(function_args.get("query", "technology"))
                elif function_name == "read_data_file":
                    result = read_data_file(function_args.get("file_path"))
                elif function_name == "summarize_information":
                    result = summarize_information(
                        function_args.get("text"),
                        function_args.get("summary_type", "general")
                    )
                else:
                    result = f"Function {function_name} không được hỗ trợ."
                
                assistant_content += result + "\n\n"
                
            # Gọi lại OpenAI để có response tự nhiên hơn
            openai_messages.append({"role": "assistant", "content": assistant_content})
            openai_messages.append({"role": "user", "content": "Hãy tóm tắt và giải thích kết quả trên một cách ngắn gọn."})
            
            final_response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=openai_messages,
                max_tokens=500,
                temperature=Config.TEMPERATURE
            )
            
            assistant_content += "💡 **Tóm tắt:**\n" + final_response.choices[0].message.content
        else:
            assistant_content = response_message.content
        
        # Lưu tin nhắn của assistant
        assistant_msg = {
            "id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": assistant_content,
            "timestamp": datetime.now().isoformat()
        }
        messages_db.insert(assistant_msg)
        
        # Cập nhật conversation
        Conversation = Query()
        conversations_db.update(
            {
                "updated_at": datetime.now().isoformat(),
                "message_count": len(messages_db.search(Message.conversation_id == conversation_id))
            },
            Conversation.id == conversation_id
        )
        
        return jsonify({
            "success": True,
            "response": assistant_content,
            "user_message": user_msg,
            "assistant_message": assistant_msg
        })
        
    except Exception as e:
        logger.error(f"Lỗi trong chat: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500