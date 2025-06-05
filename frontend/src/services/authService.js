import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = 'http://localhost:5000/api/auth';

const authService = {
  // Login user and store token
  login: async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/login`, { 
        username: email.trim(), // Send as 'username' for backend compatibility
        password 
      });
      
      if (response.data.token) {
        // Store the complete response data
        const userData = {
          token: response.data.token,
          user: response.data.user,
          username: response.data.user.email, // Use email as username
          role: response.data.user.role
        };
        localStorage.setItem('user', JSON.stringify(userData));
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  },

  // Logout user and remove token
  logout: () => {
    localStorage.removeItem('user');
  },

  // Register new user (admin only)
  register: async (userData) => {
    try {
      const token = authService.getToken();
      const response = await axios.post(`${API_URL}/register`, userData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  },

  // Get current user from local storage
  getCurrentUser: () => {
    try {
      const userData = JSON.parse(localStorage.getItem('user'));
      return userData;
    } catch (error) {
      console.error('Error parsing user data:', error);
      return null;
    }
  },

  // Get auth token
  getToken: () => {
    const userData = authService.getCurrentUser();
    return userData?.token;
  },

  // Check if token is valid
  isTokenValid: () => {
    const token = authService.getToken();
    if (!token) return false;
    
    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      return decoded.exp > currentTime;
    } catch (error) {
      console.error('Token validation error:', error);
      return false;
    }
  },

  // Get user role
  getUserRole: () => {
    const token = authService.getToken();
    if (!token) return null;
    
    try {
      const decoded = jwtDecode(token);
      return decoded.role;
    } catch (error) {
      console.error('Error getting user role:', error);
      return null;
    }
  },

  // Get user info from token
  getUserInfo: () => {
    const token = authService.getToken();
    if (!token) return null;
    
    try {
      const decoded = jwtDecode(token);
      return {
        email: decoded.sub,
        username: decoded.sub, // Use email as username
        user_id: decoded.user_id,
        name: decoded.name,
        role: decoded.role
      };
    } catch (error) {
      console.error('Error getting user info:', error);
      return null;
    }
  },

  // Check if user has admin role
  isAdmin: () => {
    const role = authService.getUserRole();
    return role === 'admin';
  },

  // Check if user has doctor role  
  isDoctor: () => {
    const role = authService.getUserRole();
    return role === 'doctor' || role === 'admin';
  },

  // Check if user has employee role
  isEmployee: () => {
    const role = authService.getUserRole();
    return role === 'employee';
  },

  // Check if user can access analysis features (admin, doctor)
  canAnalyze: () => {
    const role = authService.getUserRole();
    return role === 'admin' || role === 'doctor';
  },

  // Check if user can view reports (all roles)
  canViewReports: () => {
    const role = authService.getUserRole();
    return ['admin', 'doctor', 'employee'].includes(role);
  },

  // Get user profile from API
  getProfile: async () => {
    try {
      const token = authService.getToken();
      const response = await axios.get(`${API_URL}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get profile');
    }
  },

  // Change password
  changePassword: async (passwordData) => {
    try {
      const token = authService.getToken();
      const response = await axios.post(`${API_URL}/change-password`, passwordData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to change password');
    }
  },

  // Get all users (admin only)
  getAllUsers: async () => {
    try {
      const token = authService.getToken();
      const response = await axios.get(`${API_URL}/users`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get users');
    }
  },

  // Get activity logs (admin only)
  getActivityLogs: async (limit = 100) => {
    try {
      const token = authService.getToken();
      const response = await axios.get(`${API_URL}/activity-logs?limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Failed to get activity logs');
    }
  },

  // Test database connection
  testDatabaseConnection: async () => {
    try {
      const response = await axios.get(`${API_URL}/test-db`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Database connection test failed');
    }
  }
};

export default authService;
