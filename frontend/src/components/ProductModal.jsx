import React, { useState, useEffect } from 'react';
import { predictCarbonScore } from '../services/api';

const ProductModal = ({ product, isOpen, onClose }) => {
  const [carbonScore, setCarbonScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && product) {
      fetchCarbonScore();
    }
  }, [isOpen, product]);

  const fetchCarbonScore = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const productData = {
        category: product.category,
        origin_country: product.origin_country,
        weight_kg: product.weight_kg,
        packaging: product.packaging,
        delivery_method: product.delivery_method,
        delivery_distance_km: product.delivery_distance_km,
        delivery_speed: product.delivery_speed
      };

      const scoreResult = await predictCarbonScore(productData);
      
      const score = scoreResult.carbon_score;
      let label = '';
      let colorClass = '';

      if (score < 50) {
        label = 'Eco-Friendly';
        colorClass = 'bg-green-100 text-green-800';
      } else if (score < 100) {
        label = 'Neutral';
        colorClass = 'bg-yellow-100 text-yellow-800';
      } else {
        label = 'Hazardous';
        colorClass = 'bg-red-100 text-red-800';
      }

      setCarbonScore({ ...scoreResult, label, colorClass });
    } catch (err) {
      setError(err.message || 'Failed to predict carbon score');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen || !product) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto modal-scrollbar">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-2xl font-bold text-gray-800">
              {product.product_name}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
          </div>

          {/* Product Image */}
          <div className="mb-6">
            <img 
              src={product.image_url} 
              alt={product.product_name}
              className="w-full h-64 object-contain bg-gray-100 rounded-lg"
            />
          </div>

          {/* Product Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Product Details</h3>
              <div className="space-y-2 text-sm">
                <p><strong>Description:</strong> {product.description}</p>
                <p><strong>Category:</strong> {product.category}</p>
                <p><strong>Origin:</strong> {product.origin_country}</p>
                <p><strong>Weight:</strong> {product.weight_kg} kg</p>
                <p><strong>Price:</strong> ${product.price_usd.toFixed(2)}</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Shipping Details</h3>
              <div className="space-y-2 text-sm">
                <p><strong>Packaging:</strong> {product.packaging}</p>
                <p><strong>Delivery Method:</strong> {product.delivery_method}</p>
                <p><strong>Delivery Distance:</strong> {product.delivery_distance_km} km</p>
                <p><strong>Delivery Speed:</strong> {product.delivery_speed}</p>
              </div>
            </div>
          </div>

          {/* Carbon Score Section */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Carbon Score</h3>
            
            {loading && (
              <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-green-600"></div>
                <span className="ml-2">Calculating carbon score...</span>
              </div>
            )}

            {error && (
              <div className="bg-red-100 text-red-700 p-3 rounded-md">
                {error}
              </div>
            )}

            {carbonScore && (
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="text-3xl font-bold text-green-600">
                    {carbonScore.carbon_score.toFixed(2)}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${carbonScore.colorClass}`}>
                    {carbonScore.label}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  This score represents the estimated carbon footprint of this product, 
                  including production, packaging, and delivery.
                </p>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mt-6">
            <button className="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors">
              Add to Cart
            </button>
            <button className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-300 transition-colors">
              Add to Wishlist
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
