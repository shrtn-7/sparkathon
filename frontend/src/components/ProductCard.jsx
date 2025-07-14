import React from 'react';

const ProductCard = ({ product, onProductClick }) => {
  return (
    <div 
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow duration-200"
      onClick={() => onProductClick(product)}
    >
      <div className="h-48 bg-gray-100 flex items-center justify-center">
        <img 
          src={product.image_url} 
          alt={product.product_name}
          className="max-h-full max-w-full object-contain"
          loading="lazy"
        />
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-lg text-gray-800 mb-2 truncate">
          {product.product_name}
        </h3>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {product.description}
        </p>
        
        <div className="flex justify-between items-center">
          <span className="text-2xl font-bold text-green-600">
            ${product.price_usd.toFixed(2)}
          </span>
          
          <span className="text-xs bg-gray-100 px-2 py-1 rounded-full text-gray-600">
            {product.category}
          </span>
        </div>
        
        <div className="mt-2 flex justify-between items-center text-xs text-gray-500">
          <span>From {product.origin_country}</span>
          <span>{product.weight_kg}kg</span>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
