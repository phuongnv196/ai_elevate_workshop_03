import React, { useState, useEffect } from 'react';
import {
  Box,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Alert,
  Snackbar
} from '@mui/material';
import ConversationList from '../../components/Chat/ConversationList';
import ChatInterface from '../../components/Chat/ChatInterface';
import { ChatService } from '../../services/chatService';
import type { Conversation } from '../../types/chat';

// Create a modern theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2563eb',
      light: '#3b82f6',
      dark: '#1d4ed8',
    },
    secondary: {
      main: '#10b981',
      light: '#34d399',
      dark: '#059669',
    },
    background: {
      default: '#f8fafc',
      paper: '#ffffff',
    },
    text: {
      primary: '#0f172a',
      secondary: '#64748b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

const ChatPage: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const selectedConversation = conversations.find(c => c.id === selectedConversationId) || null;

  // Load conversations on component mount
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setLoading(true);
      setError(null);
      const loadedConversations = await ChatService.getConversations();
      setConversations(loadedConversations);
      
      // Auto-select first conversation if none selected
      if (!selectedConversationId && loadedConversations.length > 0) {
        setSelectedConversationId(loadedConversations[0].id);
      }
    } catch (err) {
      setError('Không thể tải danh sách cuộc trò chuyện. Vui lòng kiểm tra kết nối mạng.');
      console.error('Error loading conversations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  const handleCreateConversation = async (title?: string) => {
    try {
      setError(null);
      const newConversation = await ChatService.createConversation(title);
      setConversations(prev => [newConversation, ...prev]);
      setSelectedConversationId(newConversation.id);
    } catch (err) {
      setError('Không thể tạo cuộc trò chuyện mới. Vui lòng thử lại.');
      console.error('Error creating conversation:', err);
    }
  };

  const handleDeleteConversation = (conversationId: string) => {
    setConversations(prev => prev.filter(c => c.id !== conversationId));
    
    // If deleted conversation was selected, clear selection or select another
    if (selectedConversationId === conversationId) {
      const remainingConversations = conversations.filter(c => c.id !== conversationId);
      setSelectedConversationId(remainingConversations.length > 0 ? remainingConversations[0].id : null);
    }
  };

  const handleUpdateTitle = async (conversationId: string, newTitle: string) => {
    try {
      const updatedConversation = await ChatService.updateConversationTitle(conversationId, newTitle);
      setConversations(prev =>
        prev.map(c => c.id === conversationId ? updatedConversation : c)
      );
    } catch (err) {
      setError('Không thể cập nhật tiêu đề. Vui lòng thử lại.');
      console.error('Error updating title:', err);
    }
  };

  const handleConversationUpdate = () => {
    // Reload conversations to get updated message counts and timestamps
    loadConversations();
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
        {/* Sidebar - Conversation List */}
        <ConversationList
          conversations={conversations}
          selectedConversationId={selectedConversationId}
          onSelectConversation={handleSelectConversation}
          onCreateConversation={handleCreateConversation}
          onDeleteConversation={handleDeleteConversation}
          onUpdateTitle={handleUpdateTitle}
          loading={loading}
        />

        {/* Main Chat Interface */}
        <ChatInterface
          selectedConversation={selectedConversation}
          onConversationUpdate={handleConversationUpdate}
          onConversationDelete={handleDeleteConversation}
        />

        {/* Global Error Snackbar */}
        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={() => setError(null)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert
            onClose={() => setError(null)}
            severity="error"
            sx={{ width: '100%' }}
          >
            {error}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
};

export default ChatPage;
