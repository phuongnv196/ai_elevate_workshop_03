import React, { useState } from 'react';
import { Grid, Card, CardContent, Typography, TextField, Select, MenuItem, Button } from '@mui/material';

const SettingsForm = () => {
  const [language, setLanguage] = useState('en');
  const [theme, setTheme] = useState('light');
  const [dateFormat, setDateFormat] = useState('YYYY-MM-DD');

  const handleSubmit = (event: any) => {
    event.preventDefault();
    // Gửi yêu cầu đến server để lưu trữ cấu hình
  };

  return (
    <Grid container spacing={2}>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="h6" component="div">
              Cấu hình
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="body1" component="div">
              Ngôn ngữ
            </Typography>
            <Select value={language} onChange={(event) => setLanguage(event.target.value)}>
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="vi">Vietnamese</MenuItem>
            </Select>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="body1" component="div">
              Giao diện
            </Typography>
            <Select value={theme} onChange={(event) => setTheme(event.target.value)}>
              <MenuItem value="light">Sáng</MenuItem>
              <MenuItem value="dark">Tối</MenuItem>
            </Select>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <Card>
          <CardContent>
            <Typography variant="body1" component="div">
              Định dạng ngày
            </Typography>
            <Select value={dateFormat} onChange={(event) => setDateFormat(event.target.value)}>
              <MenuItem value="YYYY-MM-DD">YYYY-MM-DD</MenuItem>
              <MenuItem value="DD-MM-YYYY">DD-MM-YYYY</MenuItem>
            </Select>
          </CardContent>
        </Card>
      </Grid>
      <Grid>
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Lưu cấu hình
        </Button>
      </Grid>
    </Grid>
  );
};

export default SettingsForm;