# 🔊 Text-to-Speech (TTS) Features

## ✨ Tính năng đã thêm

### 🎤 API Endpoints mới

#### 1. Đọc một tin nhắn cụ thể
```http
POST /api/conversation/messages/{message_id}/tts
```

**Body:**
```json
{
  "speed": 1.0,
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Text-to-Speech conversion thành công",
  "audio_file": "tts_output_12345.wav",
  "download_url": "/api/tts/download/tts_output_12345.wav",
  "duration": 15.2,
  "file_size": 245760,
  "message_info": {
    "id": "msg-123",
    "role": "assistant",
    "content_preview": "Đây là nội dung được đọc...",
    "timestamp": "2025-08-02T12:00:00"
  }
}
```

#### 2. Đọc toàn bộ cuộc trò chuyện (chỉ AI responses)
```http
POST /api/conversation/conversations/{conversation_id}/messages/tts
```

**Body:**
```json
{
  "speed": 1.0,
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversion toàn bộ conversation thành công",
  "audio_file": "conversation_tts_67890.wav",
  "download_url": "/api/tts/download/conversation_tts_67890.wav",
  "duration": 120.5,
  "file_size": 1966080,
  "conversation_info": {
    "id": "conv-456",
    "messages_count": 5,
    "content_preview": "Phản hồi 1: Xin chào...",
  }
}
```

### 🎨 UI Features mới

#### 1. Message-level TTS
- **Nút TTS** trên mỗi tin nhắn AI (assistant messages)
- **Icons:** 🔊 (play) / 🔇 (stop) / ⏳ (loading)
- **Hover hiện nút:** Chỉ hiện khi hover vào message bubble
- **Position:** Góc trên bên phải của message bubble

#### 2. Conversation-level TTS  
- **Nút TTS** trong ChatHeader
- **Dialog cài đặt:** Tốc độ đọc, ngôn ngữ
- **Controls:** Play/Stop toàn bộ cuộc trò chuyện

### ⚙️ Tùy chọn TTS

#### Tốc độ đọc (Speed)
- **Range:** 0.5x - 2.0x
- **Default:** 1.0x (tốc độ bình thường)
- **UI:** Slider với marks

#### Ngôn ngữ (Language)
- **English (en)** - Default
- **Tiếng Việt (vi)**
- **Français (fr)**
- **Deutsch (de)**
- **Español (es)**

### 🧹 Text Cleaning

API tự động làm sạch text trước khi TTS:

```python
def _clean_text_for_tts(text: str) -> str:
    # Loại bỏ markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic  
    text = re.sub(r'`(.*?)`', r'\1', text)        # Code
    
    # Loại bỏ emoji
    text = re.sub(r'[🔧💡🎯🚫✅]', '', text)
    
    # Thay thế ký hiệu
    replacements = {
        '&': 'và', '@': 'at', '#': 'hashtag',
        '%': 'phần trăm', '$': 'đô la', '+': 'cộng'
    }
    
    return text
```

## 🚀 Cách sử dụng

### 1. Backend Setup
Backend đã có sẵn TTS service. Chỉ cần đảm bảo dependencies:

```bash
cd backend
pip install torch transformers scipy numpy
```

### 2. Frontend Usage

#### Đọc một tin nhắn:
```typescript
// Trong MessageBubble component
const handleTextToSpeech = async () => {
  const ttsResult = await ChatService.textToSpeech(message.id, {
    speed: 1.0,
    language: 'en'
  });
  
  const audio = new Audio(ChatService.getAudioDownloadUrl(ttsResult.audio_file));
  await audio.play();
};
```

#### Đọc toàn bộ conversation:
```typescript
// Trong TTSControls component
const handleConversationTTS = async () => {
  const result = await ChatService.textToSpeechConversation(conversation.id, {
    speed: 1.5,
    language: 'en'
  });
  
  const audio = new Audio(ChatService.getAudioDownloadUrl(result.audio_file));
  await audio.play();
};
```

## 📁 Files đã tạo/cập nhật

### Backend:
- `routes/conversation_router.py` - Thêm 2 TTS endpoints
- `services/tts_service.py` - Service đã có sẵn

### Frontend:
- `services/chatService.ts` - Thêm TTS methods
- `components/Chat/MessageBubble.tsx` - Thêm TTS button
- `components/Chat/TTSControls.tsx` - Component TTS cho conversation
- `components/Chat/ChatHeader.tsx` - Thêm TTSControls

## 🎯 Demo Flow

1. **User gửi tin nhắn:** "Explain machine learning"
2. **AI trả lời:** Một đoạn text dài về ML
3. **User click TTS button** trên AI message
4. **System:** Convert text → audio → play
5. **User click conversation TTS:** Dialog mở với settings
6. **User chọn speed 1.5x, language EN** → Convert toàn bộ conversation

## 🔧 Technical Details

### Audio Format
- **Output:** WAV files
- **Quality:** 16-bit, 22kHz
- **Storage:** Temporary files (auto cleanup)

### Browser Support
- **Modern browsers** với Web Audio API
- **HTMLAudioElement** cho playback
- **Fetch API** cho download

### Error Handling
- **503:** TTS service không available
- **404:** Message/Conversation không tồn tại
- **500:** Lỗi conversion hoặc audio playback

Tính năng TTS này giúp người dùng nghe AI responses thay vì chỉ đọc, rất hữu ích cho accessibility và multitasking! 🎧
