import React, { useState } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  IconButton,
  Typography,
  Button,
  Tooltip,
  Menu,
  MenuItem,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Paper
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import ChatIcon from '@mui/icons-material/Chat';
import type { Conversation } from '../../types/chat';

interface ConversationListProps {
  conversations: Conversation[];
  selectedConversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
  onCreateConversation: (title?: string) => void;
  onDeleteConversation: (conversationId: string) => void;
  onUpdateTitle: (conversationId: string, newTitle: string) => void;
  loading?: boolean;
}

const ConversationList: React.FC<ConversationListProps> = ({
  conversations,
  selectedConversationId,
  onSelectConversation,
  onCreateConversation,
  onDeleteConversation,
  onUpdateTitle,
  loading = false
}) => {
  const [menuAnchor, setMenuAnchor] = useState<null | HTMLElement>(null);
  const [selectedForMenu, setSelectedForMenu] = useState<string | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, conversationId: string) => {
    event.stopPropagation();
    setMenuAnchor(event.currentTarget);
    setSelectedForMenu(conversationId);
  };

  const handleMenuClose = () => {
    setMenuAnchor(null);
    setSelectedForMenu(null);
  };

  const handleEditClick = () => {
    const conversation = conversations.find(c => c.id === selectedForMenu);
    if (conversation) {
      setEditTitle(conversation.title);
      setEditDialogOpen(true);
    }
    handleMenuClose();
  };

  const handleDeleteClick = () => {
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const handleEditSave = () => {
    if (selectedForMenu && editTitle.trim()) {
      onUpdateTitle(selectedForMenu, editTitle.trim());
      setEditDialogOpen(false);
      setEditTitle('');
    }
  };

  const handleDeleteConfirm = () => {
    if (selectedForMenu) {
      onDeleteConversation(selectedForMenu);
      setDeleteDialogOpen(false);
    }
  };

  const handleCreateConversation = () => {
    if (newTitle.trim()) {
      onCreateConversation(newTitle.trim());
    } else {
      onCreateConversation();
    }
    setCreateDialogOpen(false);
    setNewTitle('');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return 'Hôm nay';
    } else if (diffDays === 2) {
      return 'Hôm qua';
    } else if (diffDays <= 7) {
      return `${diffDays - 1} ngày trước`;
    } else {
      return date.toLocaleDateString('vi-VN');
    }
  };

  return (
    <>
      <Paper
        elevation={0}
        sx={{
          width: 300,
          height: '100vh',
          borderRight: '1px solid',
          borderColor: 'divider',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: 'background.default'
        }}
      >
        {/* Header */}
        <Box sx={{ p: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
          <Button
            fullWidth
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
            sx={{ mb: 1 }}
          >
            Cuộc trò chuyện mới
          </Button>
          
          <Typography variant="h6" sx={{ mt: 1 }}>
            Lịch sử trò chuyện
          </Typography>
        </Box>

        {/* Conversations List */}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {loading ? (
            <Box sx={{ p: 2, textAlign: 'center' }}>
              <Typography color="text.secondary">Đang tải...</Typography>
            </Box>
          ) : conversations.length === 0 ? (
            <Box sx={{ p: 3, textAlign: 'center' }}>
              <ChatIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 1 }} />
              <Typography color="text.secondary" variant="body2">
                Chưa có cuộc trò chuyện nào.
                Tạo cuộc trò chuyện mới để bắt đầu!
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {conversations.map((conversation) => (
                <ListItem key={conversation.id} disablePadding>
                  <ListItemButton
                    selected={selectedConversationId === conversation.id}
                    onClick={() => onSelectConversation(conversation.id)}
                    sx={{
                      py: 1.5,
                      px: 2,
                      borderRadius: 0,
                      '&.Mui-selected': {
                        backgroundColor: 'primary.main',
                        color: 'primary.contrastText',
                        '&:hover': {
                          backgroundColor: 'primary.dark',
                        },
                        '& .MuiListItemText-secondary': {
                          color: 'primary.contrastText',
                          opacity: 0.7
                        }
                      }
                    }}
                  >
                    <ListItemText
                      primary={
                        <Typography
                          variant="body2"
                          sx={{
                            fontWeight: 500,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap'
                          }}
                        >
                          {conversation.title}
                        </Typography>
                      }
                      secondary={
                        <Typography variant="caption">
                          {conversation.message_count} tin nhắn • {formatDate(conversation.updated_at)}
                        </Typography>
                      }
                    />

                    <Tooltip title="Tùy chọn">
                      <IconButton
                        size="small"
                        onClick={(e) => handleMenuOpen(e, conversation.id)}
                        sx={{
                          ml: 1,
                          color: selectedConversationId === conversation.id
                            ? 'primary.contrastText'
                            : 'text.secondary',
                          '&:hover': {
                            backgroundColor: selectedConversationId === conversation.id
                              ? 'rgba(255,255,255,0.1)'
                              : 'action.hover'
                          }
                        }}
                      >
                        <MoreVertIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Paper>

      {/* Context Menu */}
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={handleMenuClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={handleEditClick}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Đổi tên
        </MenuItem>
        <MenuItem onClick={handleDeleteClick} sx={{ color: 'error.main' }}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Xóa
        </MenuItem>
      </Menu>

      {/* Create Conversation Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Tạo cuộc trò chuyện mới</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Tiêu đề cuộc trò chuyện (tùy chọn)"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Nhập tiêu đề hoặc để trống để tự động tạo"
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>
            Hủy
          </Button>
          <Button onClick={handleCreateConversation} variant="contained">
            Tạo
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Title Dialog */}
      <Dialog
        open={editDialogOpen}
        onClose={() => setEditDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Đổi tên cuộc trò chuyện</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Tiêu đề mới"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>
            Hủy
          </Button>
          <Button onClick={handleEditSave} variant="contained">
            Lưu
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Xác nhận xóa</DialogTitle>
        <DialogContent>
          <Typography>
            Bạn có chắc chắn muốn xóa cuộc trò chuyện này?
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

export default ConversationList;
