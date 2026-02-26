import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Landing from './pages/Landing';
import Chat from './pages/Chat';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/terms" element={<Terms />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        {/* Add a fallback route for 404s if desired */}
      </Routes>
    </Router>
  );
}

export default App;
