import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SettingsPage from './pages/SettingsPage/SettingsPage';
import Dashboard from './pages/Dashboard/Dashboard';
import RequestPage from './pages/RequestPage/RequestPage';
import CollectionPage from './pages/CollectionPage/CollectionPage';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/request" element={<RequestPage />} />
        <Route path="/collection" element={<CollectionPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;