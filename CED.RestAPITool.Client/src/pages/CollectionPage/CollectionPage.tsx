import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import CollectionList from '../../components/CollectionList/CollectionList';

const CollectionPage = () => {
  return (
    <Grid container spacing={2}>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="h6" component="div">
              Collection
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <CollectionList />
      </Grid>
    </Grid>
  );
};

export default CollectionPage;