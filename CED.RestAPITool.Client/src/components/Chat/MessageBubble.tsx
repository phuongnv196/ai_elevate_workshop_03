import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Avatar,
  IconButton,
  Tooltip,
  CircularProgress
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import VolumeOffIcon from '@mui/icons-material/VolumeOff';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import type { Message } from '../../types/chat';
import { ChatService } from '../../services/chatService';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoadingTTS, setIsLoadingTTS] = useState(false);
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);

  const handleCopyMessage = () => {
    navigator.clipboard.writeText(message.content);
  };

  const handleTextToSpeech = async () => {
    if (isPlaying && audioElement) {
      // Stop current audio
      audioElement.pause();
      audioElement.currentTime = 0;
      setIsPlaying(false);
      return;
    }

    try {
      setIsLoadingTTS(true);
      
      // Call TTS API
      const ttsResult = await ChatService.textToSpeech(message.id);

      // Create audio element and play
      const audio = new Audio(ChatService.getAudioDownloadUrl(ttsResult.audio_file));
      
      audio.onplay = () => setIsPlaying(true);
      audio.onended = () => {
        setIsPlaying(false);
        setAudioElement(null);
      };
      audio.onerror = () => {
        setIsPlaying(false);
        setAudioElement(null);
        console.error('Error playing audio');
      };

      setAudioElement(audio);
      await audio.play();
      
    } catch (error) {
      console.error('Error with text-to-speech:', error);
    } finally {
      setIsLoadingTTS(false);
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('vi-VN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatContent = (content: string) => {
    try {
      // Configure marked options
      marked.setOptions({
        breaks: true, // Support line breaks
        gfm: true     // GitHub Flavored Markdown
      });

      // Convert markdown to HTML
      const htmlContent = marked.parse(content) as string;
      
      // Sanitize HTML to prevent XSS attacks
      const cleanHtml = DOMPurify.sanitize(htmlContent, {
        ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'a'],
        ALLOWED_ATTR: ['href', 'title', 'target']
      });

      return { __html: cleanHtml };
    } catch (error) {
      console.error('Error formatting content:', error);
      // Fallback to plain text if markdown parsing fails
      return { __html: content.replace(/\n/g, '<br>') };
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: isUser ? 'row-reverse' : 'row',
        gap: 1,
        mb: 2,
        px: 2
      }}
    >
      <Avatar
        sx={{
          width: 32,
          height: 32,
          backgroundColor: isUser ? 'primary.main' : 'secondary.main',
          mt: 0.5
        }}
      >
        {isUser ? <PersonIcon fontSize="small" /> : <SmartToyIcon fontSize="small" />}
      </Avatar>

      <Box
        sx={{
          maxWidth: '70%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: isUser ? 'flex-end' : 'flex-start'
        }}
      >
        <Paper
          elevation={1}
          sx={{
            p: 2,
            backgroundColor: isUser ? 'primary.main' : 'background.paper',
            color: isUser ? 'primary.contrastText' : 'text.primary',
            borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
            position: 'relative',
            '&:hover .copy-button': {
              opacity: 1
            }
          }}
        >
          <Typography
            variant="body1"
            sx={{
              wordBreak: 'break-word',
              lineHeight: 1.5,
              '& p': {
                margin: 0,
                marginBottom: '0.5em',
                '&:last-child': {
                  marginBottom: 0
                }
              },
              '& code': {
                backgroundColor: isUser ? 'rgba(255,255,255,0.2)' : '#f5f5f5',
                color: isUser ? 'inherit' : '#d73a49',
                padding: '2px 4px',
                borderRadius: '3px',
                fontFamily: 'monospace',
                fontSize: '0.9em'
              },
              '& pre': {
                backgroundColor: isUser ? 'rgba(255,255,255,0.1)' : '#f8f8f8',
                padding: '8px 12px',
                borderRadius: '6px',
                margin: '8px 0',
                overflow: 'auto',
                '& code': {
                  backgroundColor: 'transparent',
                  padding: 0,
                  color: 'inherit'
                }
              },
              '& strong': {
                fontWeight: 'bold'
              },
              '& em': {
                fontStyle: 'italic'
              },
              '& h1, & h2, & h3, & h4, & h5, & h6': {
                margin: '0.5em 0',
                fontWeight: 'bold'
              },
              '& h1': { fontSize: '1.5em' },
              '& h2': { fontSize: '1.3em' },
              '& h3': { fontSize: '1.1em' },
              '& ul, & ol': {
                margin: '0.5em 0',
                paddingLeft: '1.5em'
              },
              '& li': {
                margin: '0.2em 0'
              },
              '& blockquote': {
                margin: '0.5em 0',
                paddingLeft: '1em',
                borderLeft: `3px solid ${isUser ? 'rgba(255,255,255,0.3)' : '#ddd'}`,
                fontStyle: 'italic'
              },
              '& a': {
                color: isUser ? 'inherit' : 'primary.main',
                textDecoration: 'underline'
              }
            }}
            dangerouslySetInnerHTML={formatContent(message.content)}
          />

          <Tooltip title="Sao chép">
            <IconButton
              className="copy-button"
              size="small"
              onClick={handleCopyMessage}
              sx={{
                position: 'absolute',
                top: 4,
                right: isUser ? 36 : 4,
                opacity: 0,
                transition: 'opacity 0.2s',
                color: isUser ? 'primary.contrastText' : 'text.secondary',
                '&:hover': {
                  backgroundColor: isUser ? 'rgba(255,255,255,0.1)' : 'action.hover'
                }
              }}
            >
              <ContentCopyIcon fontSize="small" />
            </IconButton>
          </Tooltip>

          {/* TTS Button - chỉ hiện cho assistant messages */}
          {!isUser && (
            <Tooltip title={isPlaying ? "Dừng đọc" : "Đọc to"}>
              <IconButton
                className="copy-button"
                size="small"
                onClick={handleTextToSpeech}
                disabled={isLoadingTTS}
                sx={{
                  position: 'absolute',
                  top: 4,
                  right: 4,
                  opacity: 0,
                  transition: 'opacity 0.2s',
                  color: 'text.secondary',
                  '&:hover': {
                    backgroundColor: 'action.hover'
                  }
                }}
              >
                {isLoadingTTS ? (
                  <CircularProgress size={16} />
                ) : isPlaying ? (
                  <VolumeOffIcon fontSize="small" />
                ) : (
                  <VolumeUpIcon fontSize="small" />
                )}
              </IconButton>
            </Tooltip>
          )}
        </Paper>

        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ mt: 0.5, px: 1 }}
        >
          {formatTime(message.timestamp)}
        </Typography>
      </Box>
    </Box>
  );
};

export default MessageBubble;
