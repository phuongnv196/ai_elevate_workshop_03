import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import RequestForm from '../../components/RequestForm/RequestForm';

const RequestPage = () => {
  return (
    <Grid container spacing={2}>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="h6" component="div">
              Request
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <RequestForm />
      </Grid>
    </Grid>
  );
};

export default RequestPage;