import axios from 'axios';

// API Base URL - Update this to match your backend server
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// PROPERTY APIs
// ============================================================================

export const propertyAPI = {
  // Get all properties with optional filters
  getAll: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      if (filters.property_type) params.append('property_type', filters.property_type);
      if (filters.limit) params.append('limit', filters.limit);
      
      const response = await apiClient.get(`/api/data?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching properties:', error);
      throw error;
    }
  },

  // Get property by ID
  getById: async (propertyId) => {
    try {
      const response = await apiClient.get(`/api/data/${propertyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching property ${propertyId}:`, error);
      throw error;
    }
  },

  // Create new property
  create: async (propertyData) => {
    try {
      const response = await apiClient.post('/api/data', propertyData);
      return response.data;
    } catch (error) {
      console.error('Error creating property:', error);
      throw error;
    }
  },

  // Update property
  update: async (propertyId, propertyData) => {
    try {
      const response = await apiClient.put(`/api/data/${propertyId}`, propertyData);
      return response.data;
    } catch (error) {
      console.error(`Error updating property ${propertyId}:`, error);
      throw error;
    }
  },

  // Delete property
  delete: async (propertyId) => {
    try {
      const response = await apiClient.delete(`/api/data/${propertyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting property ${propertyId}:`, error);
      throw error;
    }
  },

  // Get property statistics
  getStats: async () => {
    try {
      const response = await apiClient.get('/api/data/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching property stats:', error);
      throw error;
    }
  },

  // Get aggregated data
  getAggregates: async () => {
    try {
      const response = await apiClient.get('/api/data/aggregate');
      return response.data;
    } catch (error) {
      console.error('Error fetching aggregates:', error);
      throw error;
    }
  },
};

// ============================================================================
// USER APIs
// ============================================================================

export const userAPI = {
  // Get all users
  getAll: async () => {
    try {
      const response = await apiClient.get('/api/users');
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },

  // Get user by ID
  getById: async (userId) => {
    try {
      const response = await apiClient.get(`/api/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching user ${userId}:`, error);
      throw error;
    }
  },

  // Create new user
  create: async (userData) => {
    try {
      const response = await apiClient.post('/api/users', userData);
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  },

  // Update user
  update: async (userId, userData) => {
    try {
      const response = await apiClient.put(`/api/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      console.error(`Error updating user ${userId}:`, error);
      throw error;
    }
  },

  // Delete user
  delete: async (userId) => {
    try {
      const response = await apiClient.delete(`/api/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting user ${userId}:`, error);
      throw error;
    }
  },
};

// ============================================================================
// LISTING APIs (to be implemented in backend)
// ============================================================================

export const listingAPI = {
  // Get all active listings
  getAll: async () => {
    try {
      const response = await apiClient.get('/api/listings');
      return response.data;
    } catch (error) {
      console.error('Error fetching listings:', error);
      throw error;
    }
  },

  // Get listings by seller
  getBySeller: async (sellerId) => {
    try {
      const response = await apiClient.get(`/api/listings/seller/${sellerId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching listings for seller ${sellerId}:`, error);
      throw error;
    }
  },

  // Create new listing
  create: async (listingData) => {
    try {
      const response = await apiClient.post('/api/listings', listingData);
      return response.data;
    } catch (error) {
      console.error('Error creating listing:', error);
      throw error;
    }
  },

  // Update listing status
  updateStatus: async (listingId, status) => {
    try {
      const response = await apiClient.patch(`/api/listings/${listingId}/status`, { status });
      return response.data;
    } catch (error) {
      console.error(`Error updating listing ${listingId} status:`, error);
      throw error;
    }
  },
};

// ============================================================================
// ENQUIRY APIs (to be implemented in backend)
// ============================================================================

export const enquiryAPI = {
  // Get all enquiries
  getAll: async () => {
    try {
      const response = await apiClient.get('/api/enquiries');
      return response.data;
    } catch (error) {
      console.error('Error fetching enquiries:', error);
      throw error;
    }
  },

  // Create new enquiry
  create: async (enquiryData) => {
    try {
      const response = await apiClient.post('/api/enquiries', enquiryData);
      return response.data;
    } catch (error) {
      console.error('Error creating enquiry:', error);
      throw error;
    }
  },

  // Get enquiries by buyer
  getByBuyer: async (buyerId) => {
    try {
      const response = await apiClient.get(`/api/enquiries/buyer/${buyerId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching enquiries for buyer ${buyerId}:`, error);
      throw error;
    }
  },

  // Update enquiry status
  updateStatus: async (enquiryId, status) => {
    try {
      const response = await apiClient.patch(`/api/enquiries/${enquiryId}/status`, { status });
      return response.data;
    } catch (error) {
      console.error(`Error updating enquiry ${enquiryId} status:`, error);
      throw error;
    }
  },
};

// ============================================================================
// TRANSACTION APIs (to be implemented in backend)
// ============================================================================

export const transactionAPI = {
  // Get all transactions
  getAll: async () => {
    try {
      const response = await apiClient.get('/api/transactions');
      return response.data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  },

  // Create new transaction
  create: async (transactionData) => {
    try {
      const response = await apiClient.post('/api/transactions', transactionData);
      return response.data;
    } catch (error) {
      console.error('Error creating transaction:', error);
      throw error;
    }
  },

  // Get transaction by ID
  getById: async (transactionId) => {
    try {
      const response = await apiClient.get(`/api/transactions/${transactionId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching transaction ${transactionId}:`, error);
      throw error;
    }
  },

  // Update transaction status
  updateStatus: async (transactionId, status) => {
    try {
      const response = await apiClient.patch(`/api/transactions/${transactionId}/status`, { status });
      return response.data;
    } catch (error) {
      console.error(`Error updating transaction ${transactionId} status:`, error);
      throw error;
    }
  },
};

// ============================================================================
// HEALTH CHECK
// ============================================================================

export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default apiClient;
