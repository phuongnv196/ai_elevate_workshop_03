import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Avatar,
  IconButton,
  Tooltip
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import type { Message } from '../../types/chat';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const handleCopyMessage = () => {
    navigator.clipboard.writeText(message.content);
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('vi-VN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatContent = (content: string) => {
    // Xử lý markdown đơn giản
    const formattedContent = content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code style="background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; font-family: monospace;">$1</code>')
      .replace(/\n/g, '<br>');

    return { __html: formattedContent };
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
              '& code': {
                backgroundColor: isUser ? 'rgba(255,255,255,0.2)' : '#f5f5f5',
                color: isUser ? 'inherit' : '#d73a49',
                padding: '2px 4px',
                borderRadius: '3px',
                fontFamily: 'monospace'
              },
              '& strong': {
                fontWeight: 'bold'
              },
              '& em': {
                fontStyle: 'italic'
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
                right: 4,
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
