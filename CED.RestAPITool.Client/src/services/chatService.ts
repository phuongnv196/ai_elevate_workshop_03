import type { Conversation, ConversationResponse, MessagesResponse, ChatResponse } from '../types/chat';

// Use Vite proxy for API calls
const API_BASE_URL = '/api/conversation';

export class ChatService {
  static async getConversations(): Promise<Conversation[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations`);
      const data: ConversationResponse = await response.json();
      
      if (data.success && data.conversations) {
        return data.conversations;
      }
      throw new Error(data.error || 'Failed to fetch conversations');
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  }

  static async createConversation(title?: string): Promise<Conversation> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });
      
      const data: ConversationResponse = await response.json();
      
      if (data.success && data.conversation) {
        return data.conversation;
      }
      throw new Error(data.error || 'Failed to create conversation');
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  }

  static async deleteConversation(conversationId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
        method: 'DELETE',
      });
      
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Failed to delete conversation');
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      throw error;
    }
  }

  static async updateConversationTitle(conversationId: string, title: string): Promise<Conversation> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });
      
      const data: ConversationResponse = await response.json();
      
      if (data.success && data.conversation) {
        return data.conversation;
      }
      throw new Error(data.error || 'Failed to update conversation title');
    } catch (error) {
      console.error('Error updating conversation title:', error);
      throw error;
    }
  }

  static async getMessages(conversationId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`);
      const data: MessagesResponse = await response.json();
      
      if (data.success && data.messages) {
        return data.messages;
      }
      throw new Error(data.error || 'Failed to fetch messages');
    } catch (error) {
      console.error('Error fetching messages:', error);
      throw error;
    }
  }

  static async sendMessage(conversationId: string, message: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      
      const data: ChatResponse = await response.json();
      
      if (data.success) {
        return data;
      }
      throw new Error(data.error || 'Failed to send message');
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  static async textToSpeech(messageId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/messages/${messageId}/tts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
      
      const data = await response.json();
      
      if (data.success) {
        return data;
      }
      throw new Error(data.error || 'Failed to convert text to speech');
    } catch (error) {
      console.error('Error converting to speech:', error);
      throw error;
    }
  }

  static async textToSpeechConversation(conversationId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages/tts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });
      
      const data = await response.json();
      
      if (data.success) {
        return data;
      }
      throw new Error(data.error || 'Failed to convert conversation to speech');
    } catch (error) {
      console.error('Error converting conversation to speech:', error);
      throw error;
    }
  }

  static getAudioDownloadUrl(filename: string): string {
    return `/api/tts/download/${filename}`;
  }
}
