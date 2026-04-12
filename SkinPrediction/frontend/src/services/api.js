/**
 * API Service
 * ============
 * Handles all API calls to the backend server.
 */

import axios from 'axios';

// Get API URL from environment variable or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload image and get prediction
 * @param {File} imageFile - Image file to upload
 * @returns {Promise<Object>} Prediction result
 */
export const predictDisease = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await api.post('/api/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Prediction error:', error);
    throw error.response?.data || { 
      error: 'Failed to get prediction',
      message: 'An unexpected error occurred'
    };
  }
};

/**
 * Check API health status
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};

/**
 * Get prediction history
 * @param {number} limit - Number of records to fetch
 * @returns {Promise<Object>} Prediction history
 */
export const getHistory = async (limit = 10) => {
  try {
    const response = await api.get('/api/history', {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('History fetch error:', error);
    throw error.response?.data || { 
      error: 'Failed to fetch history',
      message: 'An unexpected error occurred'
    };
  }
};

/**
 * Get information about all diseases
 * @returns {Promise<Object>} Disease information
 */
export const getDiseasesInfo = async () => {
  try {
    const response = await api.get('/api/diseases');
    return response.data;
  } catch (error) {
    console.error('Diseases info error:', error);
    throw error.response?.data || { 
      error: 'Failed to fetch diseases info',
      message: 'An unexpected error occurred'
    };
  }
};

export default api;
