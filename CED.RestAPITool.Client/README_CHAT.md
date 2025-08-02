# Chat Bot UI - CED RestAPI Tool Client

Giao diện chat bot hiện đại giống ChatGPT được xây dựng với React, TypeScript và Material-UI.

## ✨ Tính năng

### 🎯 Giao diện Chat
- **UI hiện đại**: Thiết kế giống ChatGPT với theme sáng, typography đẹp
- **Responsive**: Tối ưu cho mọi kích thước màn hình
- **Animation mượt**: Hiệu ứng typing, slide-in cho tin nhắn
- **Real-time typing indicator**: Hiển thị khi AI đang xử lý

### 💬 Quản lý cuộc trò chuyện
- **Sidebar quản lý**: Danh sách cuộc trò chuyện với thời gian cập nhật
- **Tạo/Xóa conversation**: Quản lý nhiều cuộc trò chuyện
- **Đổi tên conversation**: Chỉnh sửa tiêu đề linh hoạt
- **Lưu trữ lịch sử**: Tin nhắn được lưu trữ persistent

### 🤖 Tính năng AI
- **Function Calling**: Hỗ trợ gọi các function từ backend
- **Tech News**: Lấy tin tức công nghệ mới nhất
- **File Reading**: Đọc và phân tích file dữ liệu
- **Information Summarization**: Tóm tắt thông tin thông minh

## 🛠️ Cấu trúc dự án

```
src/
├── components/Chat/          # Các component chat
│   ├── MessageBubble.tsx     # Hiển thị tin nhắn
│   ├── MessageInput.tsx      # Input gửi tin nhắn
│   ├── ChatHeader.tsx        # Header chat với controls
│   ├── ChatInterface.tsx     # Giao diện chat chính
│   ├── ConversationList.tsx  # Sidebar danh sách chat
│   └── TypingIndicator.tsx   # Indicator khi AI typing
├── pages/ChatPage/           # Trang chat chính
│   └── index.tsx
├── services/                 # API services
│   └── chatService.ts        # Service gọi API backend
├── types/                    # TypeScript types
│   └── chat.ts              # Types cho chat
└── styles/                   # CSS styles
    └── chat.css             # Styles và animations
```

## 🚀 Chạy ứng dụng

### 1. Cài đặt dependencies
```bash
cd CED.RestAPITool.Client
npm install
```

### 2. Chạy backend API
```bash
cd ../backend
python main.py
```

### 3. Chạy frontend
```bash
npm run dev
```

### 4. Truy cập ứng dụng
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📡 API Integration

Ứng dụng tích hợp với các API từ `backend/routes/conversation_router.py`:

### Conversations API
- `GET /api/conversations` - Lấy danh sách cuộc trò chuyện
- `POST /api/conversations` - Tạo cuộc trò chuyện mới
- `PUT /api/conversations/:id` - Cập nhật tiêu đề
- `DELETE /api/conversations/:id` - Xóa cuộc trò chuyện

### Messages API  
- `GET /api/conversations/:id/messages` - Lấy tin nhắn
- `POST /api/conversations/:id/chat` - Gửi tin nhắn & nhận phản hồi AI

## 🎨 Thiết kế UI

### Theme và Colors
- **Primary**: Blue (#2563eb) - Màu chính cho buttons, links
- **Secondary**: Green (#10b981) - Màu phụ cho AI avatar
- **Background**: Light gray (#f8fafc) - Nền tổng thể
- **Typography**: Inter font - Font hiện đại, dễ đọc

### Components Design
- **Message Bubbles**: Bo góc mềm mại, colors phân biệt user/AI
- **Sidebar**: Design tối giản với hover effects
- **Input**: Multi-line với send button và attachment icon
- **Header**: Controls để edit/delete conversation

## 🔧 Cấu hình

### Vite Proxy
File `vite.config.ts` đã được cấu hình proxy để forward API calls:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

### Environment
- Development: API proxy qua Vite dev server
- Production: Build static files vào `../CED.RestAPITool/wwwroot`

## 🚀 Features mở rộng

### Có thể thêm:
- **Dark mode toggle**: Chế độ sáng/tối
- **File upload**: Đính kèm file trong chat
- **Message search**: Tìm kiếm trong tin nhắn
- **Export chat**: Xuất cuộc trò chuyện ra file
- **Voice messages**: Tin nhắn giọng nói
- **Message reactions**: React tin nhắn với emoji

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **CORS Error**: Đảm bảo backend đã enable CORS
2. **API Connection**: Kiểm tra backend đang chạy port 5000
3. **Build Error**: Xóa node_modules và npm install lại
4. **TypeScript Error**: Kiểm tra types import đúng đường dẫn

### Debug:
```bash
# Check backend API
curl http://localhost:5000/api/conversations

# Check frontend build
npm run build

# Lint check
npm run lint
```

## 🏗️ Tech Stack

- **Frontend**: React 19 + TypeScript + Vite
- **UI Library**: Material-UI (MUI) v7
- **Routing**: React Router v7  
- **HTTP Client**: Fetch API
- **Styling**: Material-UI Theme + Custom CSS
- **Icons**: Material-UI Icons
- **Build Tool**: Vite với HMR

Ứng dụng được xây dựng theo component architecture với separation of concerns rõ ràng, dễ maintain và mở rộng.
