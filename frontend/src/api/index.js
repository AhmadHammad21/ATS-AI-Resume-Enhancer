import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export const analyzeResumes = async (jobDescription, files) => {
  const formData = new FormData();
  formData.append('job_description', jobDescription);
  files.forEach(file => {
    formData.append('resumes', file);
  });

  try {
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing resumes:', error);
    throw error;
  }
};

export default api; 