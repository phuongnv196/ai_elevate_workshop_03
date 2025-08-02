import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import RequestForm from '../../components/RequestForm/RequestForm';
import RequestList from '../../components/RequestList/RequestList';

const Dashboard = () => {
  return (
    <Grid container spacing={2}>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="h6" component="div">
              Dashboard
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <RequestForm />
      </Grid>
      <Grid>
        <RequestList />
      </Grid>
    </Grid>
  );
};

export default Dashboard;