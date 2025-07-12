const API_BASE_URL = 'http://localhost:8000/api';

export const predictCarbonScore = async (productData) => {
  const response = await fetch(`${API_BASE_URL}/predict-score`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to predict carbon score');
  }
  
  return response.json();
};

export const getGreenerAlternatives = async (productData) => {
  const response = await fetch(`${API_BASE_URL}/get-alternatives`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to get alternatives');
  }
  
  return response.json();
}; 