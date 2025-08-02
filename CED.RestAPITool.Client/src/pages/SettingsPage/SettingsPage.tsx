import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import SettingsForm from '../../components/SettingsForm/SettingsForm';

const SettingsPage = () => {
  return (
    <Grid container spacing={2}>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="h6" component="div">
              Settings
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <SettingsForm />
      </Grid>
    </Grid>
  );
};

export default SettingsPage;