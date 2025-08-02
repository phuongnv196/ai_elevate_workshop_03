import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const RequestList = () => {
  return (
    <List>
      <ListItem >
        <ListItemText primary="Yêu cầu 1" />
      </ListItem>
      <ListItem >
        <ListItemText primary="Yêu cầu 2" />
      </ListItem>
      <ListItem >
        <ListItemText primary="Yêu cầu 3" />
      </ListItem>
    </List>
  );
};

export default RequestList;