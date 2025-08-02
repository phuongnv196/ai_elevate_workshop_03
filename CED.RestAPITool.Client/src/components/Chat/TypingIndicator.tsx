import React from 'react';
import { Box, Typography } from '@mui/material';

const TypingIndicator: React.FC = () => {
  return (
    <Box sx={{ px: 2, mb: 2 }}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 1,
          p: 2,
          backgroundColor: 'action.hover',
          borderRadius: 2,
          maxWidth: '70%'
        }}
      >
        <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: 'primary.main',
              animation: 'typing 1.4s infinite ease-in-out'
            }}
          />
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: 'primary.main',
              animation: 'typing 1.4s infinite ease-in-out',
              animationDelay: '0.16s'
            }}
          />
          <Box
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: 'primary.main',
              animation: 'typing 1.4s infinite ease-in-out',
              animationDelay: '0.32s'
            }}
          />
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
          AI đang trả lời...
        </Typography>
      </Box>
    </Box>
  );
};

export default TypingIndicator;
