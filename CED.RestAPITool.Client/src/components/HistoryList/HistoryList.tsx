import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const HistoryList = () => {
  return (
    <List>
      <ListItem >
        <ListItemText primary="History 1" />
      </ListItem>
      <ListItem >
        <ListItemText primary="History 2" />
      </ListItem>
      <ListItem >
        <ListItemText primary="History 3" />
      </ListItem>
    </List>
  );
};

export default HistoryList;