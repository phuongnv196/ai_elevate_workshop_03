import React, { useState } from 'react';
import {
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import SettingsVoiceIcon from '@mui/icons-material/SettingsVoice';
import { ChatService } from '../../services/chatService';
import type { Conversation } from '../../types/chat';

interface TTSControlsProps {
  conversation: Conversation | null;
}

const TTSControls: React.FC<TTSControlsProps> = ({ conversation }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const handleConversationTTS = async () => {
    if (!conversation) return;

    try {
      setIsLoading(true);
      setError(null);

      // Stop current audio if playing
      if (audioElement) {
        audioElement.pause();
        audioElement.currentTime = 0;
        setIsPlaying(false);
      }

      const result = await ChatService.textToSpeechConversation(conversation.id);

      // Create and play audio
      const audio = new Audio(ChatService.getAudioDownloadUrl(result.audio_file));
      
      audio.onplay = () => setIsPlaying(true);
      audio.onended = () => {
        setIsPlaying(false);
        setAudioElement(null);
      };
      audio.onerror = () => {
        setIsPlaying(false);
        setAudioElement(null);
        setError('Lỗi khi phát audio');
      };

      setAudioElement(audio);
      await audio.play();
      setDialogOpen(false);

    } catch (err) {
      setError('Không thể chuyển đổi thành giọng nói. Vui lòng thử lại.');
      console.error('TTS Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopAudio = () => {
    if (audioElement) {
      audioElement.pause();
      audioElement.currentTime = 0;
      setIsPlaying(false);
      setAudioElement(null);
    }
  };

  if (!conversation) return null;

  return (
    <>
      <Tooltip title={isPlaying ? "Dừng đọc cuộc trò chuyện" : "Đọc toàn bộ cuộc trò chuyện"}>
        <IconButton
          size="small"
          onClick={isPlaying ? handleStopAudio : () => setDialogOpen(true)}
          sx={{
            color: isPlaying ? 'error.main' : 'text.secondary',
            '&:hover': {
              backgroundColor: 'action.hover'
            }
          }}
        >
          {isPlaying ? <SettingsVoiceIcon /> : <RecordVoiceOverIcon />}
        </IconButton>
      </Tooltip>

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Cài đặt Text-to-Speech</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Typography variant="body2" color="text.secondary">
            Chức năng này sẽ đọc tất cả phản hồi của AI trong cuộc trò chuyện hiện tại.
            <br />
            <em>Lưu ý: Tính năng điều chỉnh tốc độ và ngôn ngữ sẽ được thêm trong phiên bản tương lai.</em>
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>
            Hủy
          </Button>
          <Button
            onClick={handleConversationTTS}
            variant="contained"
            disabled={isLoading}
            startIcon={isLoading ? <CircularProgress size={16} /> : <RecordVoiceOverIcon />}
          >
            {isLoading ? 'Đang xử lý...' : 'Đọc cuộc trò chuyện'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default TTSControls;
