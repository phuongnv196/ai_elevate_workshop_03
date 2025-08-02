# Flask REST API

## Mô tả
Đây là một Flask REST API với các endpoint cơ bản để quản lý users, data và **Text-to-Speech functionality** sử dụng Meta's MMS-TTS model.

## Tính năng mới: Text-to-Speech API 🎤
API này hỗ trợ chuyển đổi văn bản thành giọng nói sử dụng model `facebook/mms-tts-eng` với chất lượng cao.

## Cấu trúc thư mục
```
backend/
├── main.py                    # Entry point của ứng dụng
├── requirements.txt           # Dependencies (đã thêm TTS libraries)
├── test_tts_api.py           # Test script cho TTS API
├── TTS_API_DOCUMENTATION.md  # Chi tiết documentation cho TTS API
├── config/
│   └── config.py             # Cấu hình ứng dụng
├── routes/
│   └── api_routes.py         # API routes (bao gồm TTS endpoints)
├── services/
│   ├── user_service.py       # User business logic
│   ├── data_service.py       # Data business logic
│   └── tts_service.py        # Text-to-Speech service
└── core/
    └── utils.py              # Utility functions
```

## Cài đặt và chạy

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Chạy ứng dụng:
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

## Ví dụ sử dụng

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

## Kiểm tra TTS API
Chạy test script để kiểm tra tất cả TTS endpoints:
```bash
python test_tts_api.py
```

Hoặc test với custom URL và text:
```bash
python test_tts_api.py --url http://localhost:5000 --text "Your test message here"
```

## Yêu cầu hệ thống cho TTS
- Python 3.8+
- PyTorch (tự động cài đặt)
- Transformers library
- Scipy và NumPy
- Ít nhất 2GB RAM để load model
- Khoảng 1GB ổ cứng cho model cache

## Lưu ý quan trọng
- Model sẽ được tải xuống tự động lần đầu chạy (khoảng 400MB)
- File audio được tạo sẽ tự động xóa sau 24 giờ
- Giới hạn văn bản: 5000 ký tự
- Chỉ hỗ trợ tiếng Anh (có thể mở rộng cho ngôn ngữ khác)

Xem chi tiết trong file `TTS_API_DOCUMENTATION.md`
