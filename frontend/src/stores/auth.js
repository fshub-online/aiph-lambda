// User authentication store with Pinia
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import api from '@/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || null);
  const isAuthenticated = computed(() => !!user.value);

  function setUser (userData) {
    user.value = userData;
  }

  function setToken (tokenValue) {
    token.value = tokenValue;
    if (tokenValue) {
      localStorage.setItem('token', tokenValue);
    } else {
      localStorage.removeItem('token');
    }
  }

  function logout () {
    setUser(null);
    setToken(null);
  }

  async function login (credentials) {
    try {
      // Call the OAuth endpoint
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);
      formData.append('grant_type', 'password');

      const response = await api.post('/oauth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      setToken(response.data.access_token);

      // Get user details
      await getUserInfo();

      return true;
    } catch (error) {
      console.error('Login error:', error);
      logout();
      throw error;
    }
  }

  async function getUserInfo () {
    try {
      if (!token.value) return;

      const response = await api.get('/oauth/me', {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      setUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Get user info error:', error);
      logout();
      throw error;
    }
  }

  async function changePassword (currentPassword, newPassword) {
    try {
      const response = await api.post('/oauth/me/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      }, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      return response.data;
    } catch (error) {
      const msg = error?.response?.data?.detail || error.message || 'Failed to change password';
      throw new Error(msg);
    }
  }

  async function updateProfile (profileData) {
    try {
      const response = await api.patch('/oauth/me', profileData, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      setUser(response.data);
      return response.data;
    } catch (error) {
      const msg = error?.response?.data?.detail || error.message || 'Failed to update profile';
      throw new Error(msg);
    }
  }

  // Check if there's a token and get user info on startup
  async function initialize () {
    if (token.value) {
      try {
        await getUserInfo();
      } catch (error) {
        console.error('Failed to restore session:', error);
      }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    getUserInfo,
    initialize,
    changePassword,
    updateProfile,
    setToken, // expose for api.js
    setUser, // expose for api.js (if needed)
  };
});
