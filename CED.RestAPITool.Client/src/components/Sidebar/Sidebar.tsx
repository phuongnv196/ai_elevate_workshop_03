import React from 'react';
import { Drawer, List, ListItem, ListItemText } from '@mui/material';

const Sidebar = () => {
  return (
    <Drawer variant="permanent" anchor="left">
      <List>
        <ListItem>
          <ListItemText primary="Request" />
        </ListItem>
        <ListItem>
          <ListItemText primary="Collection" />
        </ListItem>
        <ListItem>
          <ListItemText primary="History" />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;