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
from config.config import Config
from database import db_manager

# Import function calling services
from services.function_calling_service import (
    get_tech_news, 
    read_data_file, 
    summarize_information, 
    function_tools
)

# Import TTS service
from services.tts_service import TTSService

# ========== LOGGER SETUP ==========
logger = logging.getLogger(__name__)

# ========== BLUEPRINT SETUP ==========
conversation_bp = Blueprint('conversation', __name__)

# ========== DATABASE INITIALIZATION ==========
# Sử dụng database manager
conversations_db = db_manager.get_conversations_db()
messages_db = db_manager.get_messages_db()

# ========== TTS SERVICE INITIALIZATION ==========
tts_service = TTSService()

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

@conversation_bp.route('/messages/<message_id>/tts', methods=['POST'])
def text_to_speech_message(message_id):
    """Convert message content to speech"""
    try:
        # Kiểm tra TTS service có available không
        if not tts_service.is_available:
            return jsonify({
                "success": False,
                "error": "Text-to-Speech service không khả dụng. Vui lòng cài đặt dependencies."
            }), 503
        
        # Tìm message theo ID
        Message = Query()
        message = messages_db.search(Message.id == message_id)
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Message không tồn tại"
            }), 404
        
        message = message[0]
        message_content = message.get("content", "")
        
        if not message_content.strip():
            return jsonify({
                "success": False,
                "error": "Message không có nội dung để đọc"
            }), 400
        
        # Lấy thông tin tùy chọn từ request (note: current TTS service doesn't support these yet)
        data = request.get_json() or {}
        # voice_speed = data.get("speed", 1.0)  # Future enhancement
        # language = data.get("language", "en")  # Future enhancement
        
        # Xử lý nội dung trước khi TTS (loại bỏ markdown, emoji, etc.)
        processed_content = _clean_text_for_tts(message_content)
        
        # Generate speech
        result = tts_service.text_to_speech(
            text=processed_content,
            output_filename=None
        )
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Text-to-Speech conversion thành công",
                "audio_file": result["filename"],
                "download_url": f"/api/tts/download/{result['filename']}",
                "duration": result.get("duration_seconds"),
                "file_size": result.get("file_size_bytes"),
                "message_info": {
                    "id": message["id"],
                    "role": message["role"],
                    "content_preview": processed_content[:100] + "..." if len(processed_content) > 100 else processed_content,
                    "timestamp": message["timestamp"]
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Lỗi TTS: {result['error']}"
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi trong text-to-speech: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@conversation_bp.route('/conversations/<conversation_id>/messages/tts', methods=['POST'])
def text_to_speech_conversation(conversation_id):
    """Convert toàn bộ conversation thành speech (chỉ assistant messages)"""
    try:
        if not tts_service.is_available:
            return jsonify({
                "success": False,
                "error": "Text-to-Speech service không khả dụng"
            }), 503
        
        # Lấy tất cả messages của conversation
        Message = Query()
        messages = messages_db.search(Message.conversation_id == conversation_id)
        
        if not messages:
            return jsonify({
                "success": False,
                "error": "Conversation không có messages"
            }), 404
        
        # Chỉ lấy assistant messages và sắp xếp theo thời gian
        assistant_messages = [msg for msg in messages if msg.get("role") == "assistant"]
        assistant_messages.sort(key=lambda x: x['timestamp'])
        
        if not assistant_messages:
            return jsonify({
                "success": False,
                "error": "Conversation không có AI responses để đọc"
            }), 404
        
        # Kết hợp nội dung các messages
        combined_content = "\n\n".join([
            f"Phản hồi {i+1}: {msg['content']}" 
            for i, msg in enumerate(assistant_messages)
        ])
        
        # Lấy thông tin tùy chọn (note: current TTS service doesn't support these yet)
        data = request.get_json() or {}
        # voice_speed = data.get("speed", 1.0)  # Future enhancement
        # language = data.get("language", "en")  # Future enhancement
        
        # Xử lý và generate speech
        processed_content = _clean_text_for_tts(combined_content)
        
        result = tts_service.text_to_speech(
            text=processed_content,
            output_filename=None
        )
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Conversion toàn bộ conversation thành công",
                "audio_file": result["filename"],
                "download_url": f"/api/tts/download/{result['filename']}",
                "duration": result.get("duration_seconds"),
                "file_size": result.get("file_size_bytes"),
                "conversation_info": {
                    "id": conversation_id,
                    "messages_count": len(assistant_messages),
                    "content_preview": processed_content[:200] + "..." if len(processed_content) > 200 else processed_content
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Lỗi TTS: {result['error']}"
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi trong conversation TTS: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def _clean_text_for_tts(text: str) -> str:
    """Clean text for better TTS output"""
    import re
    
    # Loại bỏ markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic  
    text = re.sub(r'`(.*?)`', r'\1', text)        # Code
    text = re.sub(r'#{1,6}\s*(.*)', r'\1', text)  # Headers
    
    # Loại bỏ emoji và special characters
    text = re.sub(r'[🔧💡🎯🚫✅]', '', text)
    
    # Thay thế URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'link', text)
    
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Thay thế một số ký hiệu để đọc tự nhiên hơn
    replacements = {
        '&': 'và',
        '@': 'at',
        '#': 'hashtag',
        '%': 'phần trăm',
        '$': 'đô la',
        '+': 'cộng',
        '=': 'bằng',
        '<': 'nhỏ hơn',
        '>': 'lớn hơn',
        '•': '',
        '→': 'đến',
        '←': 'từ'
    }
    
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)
    
    return text