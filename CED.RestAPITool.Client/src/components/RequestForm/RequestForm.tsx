import React, { useState } from 'react';
import { Grid, TextField, Select, MenuItem, Button } from '@mui/material';

const RequestForm = () => {
  const [method, setMethod] = useState('GET');
  const [url, setUrl] = useState('');
  const [headers, setHeaders] = useState({});
  const [body, setBody] = useState('');

  const handleSubmit = (event: any) => {
    event.preventDefault();
    // Gửi yêu cầu đến server
  };

  return (
    <Grid container spacing={2}>
      <Grid>
        <TextField label="Method" value={method} onChange={(event) => setMethod(event.target.value)} />
      </Grid>
      <Grid>
        <TextField label="URL" value={url} onChange={(event) => setUrl(event.target.value)} />
      </Grid>
      <Grid>
        <Select label="Headers" value={headers} onChange={(event) => setHeaders(event.target.value)}>
          <MenuItem value="Content-Type">Content-Type</MenuItem>
          <MenuItem value="Authorization">Authorization</MenuItem>
        </Select>
      </Grid>
      <Grid>
        <TextField label="Body" value={body} onChange={(event) => setBody(event.target.value)} />
      </Grid>
      <Grid>
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Gửi yêu cầu
        </Button>
      </Grid>
    </Grid>
  );
};

export default RequestForm;