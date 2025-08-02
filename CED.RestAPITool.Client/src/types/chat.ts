export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatResponse {
  success: boolean;
  response?: string;
  user_message?: Message;
  assistant_message?: Message;
  error?: string;
}

export interface ConversationResponse {
  success: boolean;
  conversations?: Conversation[];
  conversation?: Conversation;
  error?: string;
}

export interface MessagesResponse {
  success: boolean;
  messages?: Message[];
  error?: string;
}
