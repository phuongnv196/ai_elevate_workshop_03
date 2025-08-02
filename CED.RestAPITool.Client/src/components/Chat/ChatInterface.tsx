import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  CircularProgress,
  Typography,
  Alert,
  Snackbar
} from '@mui/material';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import ChatHeader from './ChatHeader';
import TypingIndicator from './TypingIndicator';
import { ChatService } from '../../services/chatService';
import type { Message, Conversation } from '../../types/chat';

interface ChatInterfaceProps {
  selectedConversation: Conversation | null;
  onConversationUpdate: () => void;
  onConversationDelete: (conversationId: string) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  selectedConversation,
  onConversationUpdate,
  onConversationDelete
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load messages when conversation changes
  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation.id);
    } else {
      setMessages([]);
    }
  }, [selectedConversation]);

  const loadMessages = async (conversationId: string) => {
    try {
      setLoading(true);
      setError(null);
      const loadedMessages = await ChatService.getMessages(conversationId);
      setMessages(loadedMessages);
    } catch (err) {
      setError('Không thể tải tin nhắn. Vui lòng thử lại.');
      console.error('Error loading messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!selectedConversation) return;

    try {
      setSending(true);
      setError(null);

      const response = await ChatService.sendMessage(selectedConversation.id, content);
      
      if (response.user_message && response.assistant_message) {
        setMessages(prev => [...prev, response.user_message!, response.assistant_message!]);
        onConversationUpdate(); // Update conversation list
      }
    } catch (err) {
      setError('Không thể gửi tin nhắn. Vui lòng thử lại.');
      console.error('Error sending message:', err);
    } finally {
      setSending(false);
    }
  };

  const handleUpdateTitle = async (conversationId: string, newTitle: string) => {
    try {
      await ChatService.updateConversationTitle(conversationId, newTitle);
      onConversationUpdate(); // Update conversation list
    } catch (err) {
      setError('Không thể cập nhật tiêu đề. Vui lòng thử lại.');
      console.error('Error updating title:', err);
    }
  };

  const handleDeleteConversation = async (conversationId: string) => {
    try {
      await ChatService.deleteConversation(conversationId);
      onConversationDelete(conversationId);
    } catch (err) {
      setError('Không thể xóa cuộc trò chuyện. Vui lòng thử lại.');
      console.error('Error deleting conversation:', err);
    }
  };

  if (!selectedConversation) {
    return (
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'background.default',
          p: 4
        }}
      >
        <Typography variant="h4" color="text.secondary" gutterBottom>
          Chào mừng đến với AI Assistant
        </Typography>
        <Typography variant="body1" color="text.secondary" textAlign="center">
          Chọn một cuộc trò chuyện từ sidebar hoặc tạo cuộc trò chuyện mới để bắt đầu.
        </Typography>
      </Box>
    );
  }

  return (
    <>
      <Box
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: 'background.default'
        }}
      >
        {/* Chat Header */}
        <ChatHeader
          conversation={selectedConversation}
          onUpdateTitle={handleUpdateTitle}
          onDeleteConversation={handleDeleteConversation}
        />

        {/* Messages Area */}
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            backgroundColor: 'background.paper'
          }}
        >
          {loading ? (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%'
              }}
            >
              <CircularProgress />
            </Box>
          ) : messages.length === 0 ? (
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                p: 4
              }}
            >
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Bắt đầu cuộc trò chuyện
              </Typography>
              <Typography variant="body2" color="text.secondary" textAlign="center">
                Gửi tin nhắn đầu tiên để bắt đầu trò chuyện với AI Assistant.
              </Typography>
            </Box>
          ) : (
            <Box sx={{ py: 2 }}>
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              {sending && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </Box>
          )}
        </Box>

        {/* Message Input */}
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={!selectedConversation}
          loading={sending}
        />
      </Box>

      {/* Error Snackbar */}
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setError(null)}
          severity="error"
          sx={{ width: '100%' }}
        >
          {error}
        </Alert>
      </Snackbar>
    </>
  );
};

export default ChatInterface;
