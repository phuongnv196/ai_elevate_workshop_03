import React, { useState } from 'react';
import {
  Box,
  Typography,
  IconButton,
  Tooltip,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import TTSControls from './TTSControls';
import type { Conversation } from '../../types/chat';

interface ChatHeaderProps {
  conversation: Conversation | null;
  onUpdateTitle: (conversationId: string, newTitle: string) => void;
  onDeleteConversation: (conversationId: string) => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({
  conversation,
  onUpdateTitle,
  onDeleteConversation
}) => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const handleEditTitle = () => {
    if (conversation) {
      setEditTitle(conversation.title);
      setIsEditingTitle(true);
    }
  };

  const handleSaveTitle = () => {
    if (conversation && editTitle.trim()) {
      onUpdateTitle(conversation.id, editTitle.trim());
      setIsEditingTitle(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditingTitle(false);
    setEditTitle('');
  };

  const handleDeleteConfirm = () => {
    if (conversation) {
      onDeleteConversation(conversation.id);
      setDeleteDialogOpen(false);
    }
  };

  if (!conversation) {
    return (
      <Box
        sx={{
          p: 2,
          borderBottom: '1px solid',
          borderColor: 'divider',
          backgroundColor: 'background.paper'
        }}
      >
        <Typography variant="h6" color="text.secondary">
          Chọn cuộc trò chuyện để bắt đầu
        </Typography>
      </Box>
    );
  }

  return (
    <>
      <Box
        sx={{
          p: 2,
          borderBottom: '1px solid',
          borderColor: 'divider',
          backgroundColor: 'background.paper',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}
      >
        <Box sx={{ flex: 1, mr: 2 }}>
          {isEditingTitle ? (
            <TextField
              fullWidth
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSaveTitle();
                } else if (e.key === 'Escape') {
                  handleCancelEdit();
                }
              }}
              onBlur={handleSaveTitle}
              autoFocus
              variant="standard"
              size="small"
            />
          ) : (
            <Typography
              variant="h6"
              sx={{
                cursor: 'pointer',
                '&:hover': {
                  color: 'primary.main'
                }
              }}
              onClick={handleEditTitle}
            >
              {conversation.title}
            </Typography>
          )}
          
          <Typography variant="caption" color="text.secondary">
            {conversation.message_count} tin nhắn • Cập nhật lúc{' '}
            {new Date(conversation.updated_at).toLocaleString('vi-VN')}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <TTSControls conversation={conversation} />
          
          <Tooltip title="Chỉnh sửa tiêu đề">
            <IconButton
              size="small"
              onClick={handleEditTitle}
              disabled={isEditingTitle}
            >
              <EditIcon />
            </IconButton>
          </Tooltip>

          <Tooltip title="Xóa cuộc trò chuyện">
            <IconButton
              size="small"
              onClick={() => setDeleteDialogOpen(true)}
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Tooltip>

          <Tooltip title="Tùy chọn khác">
            <IconButton size="small">
              <MoreVertIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Xác nhận xóa cuộc trò chuyện</DialogTitle>
        <DialogContent>
          <Typography>
            Bạn có chắc chắn muốn xóa cuộc trò chuyện "{conversation.title}"?
            Hành động này không thể hoàn tác.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>
            Hủy
          </Button>
          <Button
            onClick={handleDeleteConfirm}
            color="error"
            variant="contained"
          >
            Xóa
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ChatHeader;
