# ========== IMPORTS ==========
import os
import json
import requests
import feedparser
import pandas as pd
from typing import List, Dict, Optional, Any
from openai import OpenAI
from bs4 import BeautifulSoup
import logging
from tinydb import Query

# Import config và database
from config.config import Config
from database import db_manager

# ========== LOGGER SETUP ==========
logger = logging.getLogger(__name__)

# ========== DATABASE INITIALIZATION ==========
data_files_db = db_manager.get_data_files_db()

# ========== CLIENT INITIALIZATION ==========
try:
    client = OpenAI(
        base_url=Config.OPENAI_BASE_URL,
        api_key=Config.OPENAI_API_KEY
    ) if Config.OPENAI_API_KEY else None
except Exception as e:
    logger.error("Vui lòng đảm bảo các biến môi trường OPENAI_API_KEY, OPENAI_BASE_URL đã được thiết lập.")
    client = None

# ========== FUNCTION CALLING TOOLS ==========

def get_tech_news(query: str = "technology") -> str:
    """Lấy tin tức công nghệ mới nhất"""
    try:
        feeds = [
            ""
        ]
        
        news_items = []
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    # Lấy thông tin cơ bản từ RSS
                    news_item = {
                        "title": entry.title,
                        "summary": entry.summary if hasattr(entry, 'summary') else "Không có tóm tắt",
                        "link": entry.link,
                        "published": entry.published if hasattr(entry, 'published') else "N/A"
                    }
                    
                    # Fetch thông tin chi tiết từ link
                    detailed_content = fetch_article_content(entry.link)
                    if detailed_content:
                        news_item["detailed_content"] = detailed_content
                    
                    news_items.append(news_item)
            except Exception as e:
                logger.error(f"Lỗi khi lấy tin từ {feed_url}: {e}")
                continue
        
        if news_items:
            result = ""
            for i, item in enumerate(news_items[:10], 1):
                result += f"{i}. **{item['title']}**\n"
                result += f"   📅 {item['published']}\n"
                result += f"   📝 {item['summary'][:200]}...\n"
                
                # Thêm nội dung chi tiết nếu có
                if 'detailed_content' in item and item['detailed_content']:
                    result += f"   📰 **Chi tiết:** {item['detailed_content'][:300]}...\n"
                
                result += f"   🔗 {item['link']}\n\n"
            return result
        else:
            return "Không thể lấy tin tức lúc này. Vui lòng thử lại sau."
            
    except Exception as e:
        return f"Lỗi khi lấy tin tức: {str(e)}"

def fetch_article_content(url: str) -> str:
    """Fetch nội dung chi tiết của bài báo từ URL"""
    try:
        # Set headers để tránh bị block
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Gửi request với timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm nội dung chính của bài báo (dành cho VnExpress)
        content_selectors = [
            '.Normal',  # VnExpress article paragraphs
            '.article-content p',  # Generic article content
            '.content p',  # Alternative content selector
            'p'  # Fallback to all paragraphs
        ]
        
        article_text = ""
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                # Lấy text từ các đoạn văn
                article_text = " ".join([p.get_text().strip() for p in paragraphs[:5]])  # Lấy 5 đoạn đầu
                break
        
        # Làm sạch text
        if article_text:
            # Loại bỏ các ký tự không mong muốn
            article_text = article_text.replace('\n', ' ').replace('\r', ' ')
            article_text = ' '.join(article_text.split())  # Loại bỏ khoảng trắng thừa
            
            # Giới hạn độ dài
            if len(article_text) > 500:
                article_text = article_text[:500] + "..."
                
            return article_text
        
        return ""
        
    except requests.RequestException as e:
        logger.error(f"Lỗi khi fetch URL {url}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Lỗi khi parse content từ {url}: {e}")
        return ""

def read_data_file(file_path: str) -> str:
    """Đọc và phân tích file dữ liệu"""
    try:
        # Kiểm tra file có tồn tại trong database không
        DataFile = Query()
        file_record = data_files_db.search(DataFile.path == file_path)
        
        if not file_record:
            return f"File '{file_path}' không tồn tại trong hệ thống."
        
        file_info = file_record[0]
        actual_path = file_info['actual_path']
        
        if not os.path.exists(actual_path):
            return f"File vật lý '{actual_path}' không tồn tại."
        
        # Đọc file theo extension
        if actual_path.endswith('.csv'):
            df = pd.read_csv(actual_path)
            result = f"📊 **PHÂN TÍCH FILE CSV: {file_path}**\n\n"
            result += f"🔢 Số dòng: {len(df)}\n"
            result += f"🔢 Số cột: {len(df.columns)}\n"
            result += f"📋 Các cột: {', '.join(df.columns.tolist())}\n\n"
            result += "📈 **5 dòng đầu tiên:**\n"
            result += df.head().to_string(index=False)
            result += "\n\n📊 **Thống kê cơ bản:**\n"
            result += df.describe().to_string()
            return result
            
        elif actual_path.endswith('.json'):
            with open(actual_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            result = f"📄 **PHÂN TÍCH FILE JSON: {file_path}**\n\n"
            result += f"📊 Loại dữ liệu: {type(data).__name__}\n"
            if isinstance(data, dict):
                result += f"🔑 Số keys: {len(data.keys())}\n"
                result += f"🗝️ Keys: {', '.join(list(data.keys())[:10])}\n"
            elif isinstance(data, list):
                result += f"📋 Số phần tử: {len(data)}\n"
            result += f"\n📝 **Nội dung (100 ký tự đầu):**\n{str(data)[:100]}..."
            return result
            
        elif actual_path.endswith('.txt'):
            with open(actual_path, 'r', encoding='utf-8') as f:
                content = f.read()
            result = f"📄 **PHÂN TÍCH FILE TEXT: {file_path}**\n\n"
            result += f"📊 Số ký tự: {len(content)}\n"
            result += f"📋 Số dòng: {len(content.splitlines())}\n"
            result += f"📝 Số từ: {len(content.split())}\n\n"
            result += f"**Nội dung (500 ký tự đầu):**\n{content[:500]}..."
            return result
        else:
            return f"Định dạng file '{actual_path.split('.')[-1]}' chưa được hỗ trợ."
            
    except Exception as e:
        return f"Lỗi khi đọc file: {str(e)}"

def summarize_information(text: str, summary_type: str = "general") -> str:
    """Tổng hợp thông tin từ text"""
    try:
        if not client:
            return "OpenAI client chưa được khởi tạo."
        
        prompt_templates = {
            "general": "Hãy tóm tắt thông tin sau một cách ngắn gọn và rõ ràng:",
            "technical": "Hãy tóm tắt các thông tin kỹ thuật quan trọng từ text sau:",
            "news": "Hãy tóm tắt các tin tức chính từ thông tin sau:",
            "data": "Hãy phân tích và tóm tắt dữ liệu từ thông tin sau:"
        }
        
        prompt = prompt_templates.get(summary_type, prompt_templates["general"])
        
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia tóm tắt thông tin. Hãy tóm tắt một cách ngắn gọn, chính xác và dễ hiểu."},
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return f"📝 **TÓM TẮT THÔNG TIN:**\n\n{response.choices[0].message.content}"
        
    except Exception as e:
        return f"Lỗi khi tóm tắt thông tin: {str(e)}"

# Định nghĩa các function tools cho OpenAI
function_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_tech_news",
            "description": "Lấy tin tức công nghệ mới nhất",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Từ khóa tìm kiếm tin tức (mặc định: technology)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_data_file",
            "description": "Đọc và phân tích file dữ liệu (CSV, JSON, TXT)",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Đường dẫn đến file cần đọc"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_information",
            "description": "Tóm tắt thông tin từ text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text cần tóm tắt"
                    },
                    "summary_type": {
                        "type": "string",
                        "enum": ["general", "technical", "news", "data"],
                        "description": "Loại tóm tắt"
                    }
                },
                "required": ["text"]
            }
        }
    }
]
