# Flask REST API

## Mô tả
Đây là một Flask REST API với các endpoint cơ bản để quản lý users, data, **Text-to-Speech functionality** sử dụng Meta's MMS-TTS model, và **Conversation API** với AI assistant tích hợp OpenAI.

## Tính năng chính
- 🎤 **Text-to-Speech API**: Chuyển đổi văn bản thành giọng nói
- 💬 **Conversation API**: Chat với AI assistant có hỗ trợ function calling
- 👥 **User Management**: CRUD operations cho users
- 📊 **Data Management**: Quản lý data entries

## Cấu trúc thư mục
```
backend/
├── main.py                          # Entry point của ứng dụng
├── requirements.txt                 # Dependencies (bao gồm TTS và Conversation)
├── test_tts_api.py                 # Test script cho TTS API
├── test_conversation_api.py        # Test script cho Conversation API
├── TTS_API_DOCUMENTATION.md        # Chi tiết documentation cho TTS API
├── CONVERSATION_API_DOCUMENTATION.md # Chi tiết documentation cho Conversation API
├── .env.example                    # Template cho environment variables
├── config/
│   └── config.py                   # Cấu hình ứng dụng
├── routes/
│   ├── api_routes.py              # API routes cơ bản
│   ├── tts_routes.py              # TTS endpoints
│   └── conversation_router.py     # Conversation endpoints
├── services/
│   ├── user_service.py            # User business logic
│   ├── data_service.py            # Data business logic
│   ├── tts_service.py             # Text-to-Speech service
│   └── function_calling_service.py # AI function calling service
├── core/
│   └── utils.py                   # Utility functions
├── data/                          # JSON database files (TinyDB)
│   ├── conversations.json
│   ├── messages.json
│   └── data_files.json
└── database.py                    # Database manager
```

## Cài đặt và chạy

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Cấu hình environment variables (tùy chọn):
```bash
# Copy template và điều chỉnh theo nhu cầu
cp .env.example .env
# Chỉnh sửa .env để thêm OPENAI_API_KEY nếu muốn sử dụng Conversation API
```

3. Chạy ứng dụng:
```bash
python main.py
```

Ứng dụng sẽ chạy trên http://localhost:5000

## API Endpoints

### Health Check
- `GET /health` - Kiểm tra tình trạng API

### Root
- `GET /` - Thông tin cơ bản về API

### Users
- `GET /api/users` - Lấy danh sách tất cả users
- `GET /api/users/<id>` - Lấy user theo ID
- `POST /api/users` - Tạo user mới
- `PUT /api/users/<id>` - Cập nhật user
- `DELETE /api/users/<id>` - Xóa user

### Data
- `GET /api/data` - Lấy danh sách tất cả data
- `POST /api/data` - Tạo data entry mới

### Text-to-Speech (TTS) 🎤
- `POST /api/tts/convert` - Chuyển đổi văn bản thành giọng nói
- `GET /api/tts/download/<filename>` - Tải xuống file audio đã tạo
- `GET /api/tts/info` - Lấy thông tin về TTS model
- `POST /api/tts/cleanup` - Dọn dẹp file audio cũ

### Conversation API 💬
- `GET /api/conversation/conversations` - Lấy danh sách conversations
- `POST /api/conversation/conversations` - Tạo conversation mới
- `PUT /api/conversation/conversations/<id>` - Cập nhật conversation
- `DELETE /api/conversation/conversations/<id>` - Xóa conversation
- `GET /api/conversation/conversations/<id>/messages` - Lấy messages
- `POST /api/conversation/conversations/<id>/chat` - Gửi tin nhắn chat

## Ví dụ sử dụng

### Conversation API
```bash
# Tạo conversation mới
curl -X POST http://localhost:5000/api/conversation/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "Tech Discussion"}'

# Gửi tin nhắn chat (yêu cầu OPENAI_API_KEY)
curl -X POST http://localhost:5000/api/conversation/conversations/{conversation_id}/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the latest AI developments?"}'

# Lấy danh sách conversations
curl http://localhost:5000/api/conversation/conversations
```

### Text-to-Speech
```bash
# Chuyển đổi văn bản thành giọng nói
curl -X POST http://localhost:5000/api/tts/convert \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Xin chào! Đây là test text-to-speech API.",
    "filename": "my_audio.wav"
  }'

# Tải xuống file audio
curl -X GET http://localhost:5000/api/tts/download/my_audio.wav -o output.wav

# Lấy thông tin model
curl -X GET http://localhost:5000/api/tts/info
```

### Tạo user mới
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyen Van A",
    "email": "nguyenvana@example.com",
    "age": 25
  }'
```

### Lấy danh sách users
```bash
curl http://localhost:5000/api/users
```

### Tạo data entry mới
```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tiêu đề mới",
    "content": "Nội dung của data entry",
    "category": "important"
  }'
```

## Định dạng Response
Tất cả responses đều có format chuẩn:
```json
{
  "success": true/false,
  "data": {...},
  "message": "Success/Error message"
}
```

## Kiểm tra API

### Test TTS API
```bash
python test_tts_api.py
```

### Test Conversation API
```bash
python test_conversation_api.py
```

### Test với custom parameters
```bash
# TTS với custom text
python test_tts_api.py --url http://localhost:5000 --text "Your test message here"
```

## Yêu cầu hệ thống

### Cho TTS API
- Python 3.8+
- PyTorch (tự động cài đặt)
- Transformers library
- Scipy và NumPy
- Ít nhất 2GB RAM để load model
- Khoảng 1GB ổ cứng cho model cache

### Cho Conversation API
- OpenAI API key (để sử dụng chat functionality)
- TinyDB cho local storage
- Requests library

## Environment Variables
Tạo file `.env` từ `.env.example` và cấu hình:
```env
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
# ... other optional variables
```

## Lưu ý quan trọng

### TTS API
- Model sẽ được tải xuống tự động lần đầu chạy (khoảng 400MB)
- File audio được tạo sẽ tự động xóa sau 24 giờ
- Giới hạn văn bản: 5000 ký tự
- Chỉ hỗ trợ tiếng Anh (có thể mở rộng cho ngôn ngữ khác)

### Conversation API
- Yêu cầu OpenAI API key để sử dụng chat functionality
- Hỗ trợ function calling cho tech news, data analysis
- Data được lưu local trong JSON files
- AI assistant chuyên về technology topics

## Documentation chi tiết
- TTS API: Xem `TTS_API_DOCUMENTATION.md`
- Conversation API: Xem `CONVERSATION_API_DOCUMENTATION.md`
