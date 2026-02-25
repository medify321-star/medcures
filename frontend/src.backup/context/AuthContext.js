import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('medcures_token'));
  const [loading, setLoading] = useState(true);
  const [guestChatCount, setGuestChatCount] = useState(parseInt(localStorage.getItem('guest_chat_count') || '0'));

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('medcures_token');
  }, []);

  const verifyToken = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
    } catch (error) {
      console.error('Token verification failed:', error);
      logout();
    } finally {
      setLoading(false);
    }
  }, [token, logout]);

  useEffect(() => {
    if (token) {
      verifyToken();
    } else {
      setLoading(false);
    }
  }, [token, verifyToken]);

  const login = async (email, password) => {
    const response = await axios.post(`${API}/auth/login`, { email, password });
    setToken(response.data.token);
    setUser(response.data.user);
    localStorage.setItem('medcures_token', response.data.token);
    return response.data;
  };

  const signup = async (email, password, name) => {
    const response = await axios.post(`${API}/auth/signup`, { email, password, name });
    setToken(response.data.token);
    setUser(response.data.user);
    localStorage.setItem('medcures_token', response.data.token);
    return response.data;
  };

  const incrementGuestChat = () => {
    const newCount = guestChatCount + 1;
    setGuestChatCount(newCount);
    localStorage.setItem('guest_chat_count', newCount.toString());
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      login,
      signup,
      logout,
      isAuthenticated: !!token,
      guestChatCount,
      incrementGuestChat
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};