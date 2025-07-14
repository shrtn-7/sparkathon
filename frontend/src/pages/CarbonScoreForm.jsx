import React, { useState } from 'react';
import { predictCarbonScore } from '../services/api';

const CarbonScoreForm = () => {
  const [formData, setFormData] = useState({
    category: '',
    origin_country: '',
    weight_kg: '',
    packaging: '',
    delivery_method: '',
    delivery_distance_km: '',
    delivery_speed: 'Standard'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'weight_kg' || name === 'delivery_distance_km'
        ? parseFloat(value) || value
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const scoreResult = await predictCarbonScore(formData);

      const score = scoreResult.carbon_score;
      let label = '';

      if (score < 50) {
        label = 'Eco-Friendly';
      } else if (score < 100) {
        label = 'Neutral';
      } else {
        label = 'Hazardous';
      }

      setResult({ ...scoreResult, label });
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Calculate Product Carbon Score</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-2">Category:</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Category</option>
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Food">Food</option>
            <option value="Furniture">Furniture</option>
          </select>
        </div>

        <div>
          <label className="block mb-2">Origin Country:</label>
          <input
            type="text"
            name="origin_country"
            value={formData.origin_country}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
        </div>

        <div>
          <label className="block mb-2">Weight (kg):</label>
          <input
            type="number"
            name="weight_kg"
            value={formData.weight_kg}
            onChange={handleChange}
            step="0.1"
            min="0"
            className="w-full p-2 border rounded"
            required
          />
        </div>

        <div>
          <label className="block mb-2">Packaging:</label>
          <select
            name="packaging"
            value={formData.packaging}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Packaging</option>
            <option value="Plastic">Plastic</option>
            <option value="Cardboard">Cardboard</option>
            <option value="Recycled">Recycled</option>
          </select>
        </div>

        <div>
          <label className="block mb-2">Delivery Method:</label>
          <select
            name="delivery_method"
            value={formData.delivery_method}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Delivery Method</option>
            <option value="Air">Air</option>
            <option value="Sea">Sea</option>
            <option value="Road">Road</option>
          </select>
        </div>

        <div>
          <label className="block mb-2">Delivery Distance (km):</label>
          <input
            type="number"
            name="delivery_distance_km"
            value={formData.delivery_distance_km}
            onChange={handleChange}
            min="0"
            className="w-full p-2 border rounded"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700 disabled:bg-gray-400"
        >
          {loading ? 'Calculating...' : 'Calculate Carbon Score'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-gray-100 rounded">
          <h3 className="text-xl font-bold mb-2">Carbon Score Result</h3>
          <p className="text-2xl font-semibold text-green-600">
            {result.carbon_score.toFixed(2)}
          </p>

          {result.label && (
            <p className="mt-2 text-lg">
              <span className={`font-bold px-3 py-1 rounded inline-block
                ${result.label === 'Eco-Friendly' ? 'bg-green-200 text-green-800' :
                  result.label === 'Neutral' ? 'bg-yellow-200 text-yellow-800' :
                  'bg-red-200 text-red-800'}`}>
                {result.label}
              </span>
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default CarbonScoreForm;
