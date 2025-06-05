import axios from 'axios';
import authService from './authService';

const API_URL = 'http://localhost:5000/api';

// Axios instance for multipart/form-data (file uploads)
const apiClientMultipart = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Axios instance for JSON payloads
const apiClientJSON = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to all requests - multipart
apiClientMultipart.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add auth token to all requests - json
apiClientJSON.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const imageService = {
  // Upload image (file upload)
  uploadImage: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/images/upload', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error uploading image');
    }
  },

  enhanceImage: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/process/enhance', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error enhancing image');
    }
  },

  colorizeImage: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/process/colorize', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error colorizing image');
    }
  },

  analyzeDentalXray: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/dental/analyze', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error analyzing dental X-ray');
    }
  },

  detectCavities: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/detect/cavities', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error detecting cavities');
    }
  },

  detectMissingTeeth: async (formData) => {
    try {
      const response = await apiClientMultipart.post('/detect/missing-teeth', formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error detecting missing teeth');
    }
  },

  // Generate and send dental report (JSON)
  generateAndSendReport: async (reportData) => {
    try {
      const response = await apiClientJSON.post('/reports/generate', reportData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error generating report');
    }
  },

  // Find patient by name and birthdate (GET with query params)
  findPatientByNameAndBirthdate: async (name, birthdate) => {
    try {
      const response = await apiClientJSON.get('/patients/find', {
        params: { name, birthdate },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error finding patient');
    }
  },

  // Add patient (JSON)
  addPatient: async (patientData) => {
    try {
      const response = await apiClientJSON.post('/patients', patientData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error adding patient');
    }
  },

  // Save scan (JSON)
  saveScan: async (scanData) => {
    try {
      const response = await apiClientJSON.post('/scans', scanData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error saving scan');
    }
  },

  // Get image history (JSON)
  getImageHistory: async () => {
    try {
      const response = await apiClientJSON.get('/images/history');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error fetching image history');
    }
  },

  // Optional: get current user id from auth service
  getCurrentUserId: () => {
    return authService.getCurrentUserId ? authService.getCurrentUserId() : null;
  },
};

export default imageService;
