export const predictCarbonScore = async (productData) => {
  const response = await fetch(`http://localhost:8000/api/predict-score`, {
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


