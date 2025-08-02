import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const CollectionList = () => {
  return (
    <List>
      <ListItem >
        <ListItemText primary="Collection 1" />
      </ListItem>
      <ListItem >
        <ListItemText primary="Collection 2" />
      </ListItem>
      <ListItem >
        <ListItemText primary="Collection 3" />
      </ListItem>
    </List>
  );
};

export default CollectionList;