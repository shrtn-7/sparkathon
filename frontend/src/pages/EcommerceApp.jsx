import React, { useState, useEffect } from 'react';
import { getProductsByCategory } from '../utils/productData';
import CategoryFilter from '../components/CategoryFilter';
import ProductGrid from '../components/ProductGrid';
import ProductModal from '../components/ProductModal';

const EcommerceApp = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const filteredProducts = getProductsByCategory(selectedCategory);
    setProducts(filteredProducts);
  }, [selectedCategory]);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-green-600 text-white py-6 mb-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">Carbon-Aware Store</h1>
          <p className="mt-2">Shop sustainably with real-time carbon footprint scores</p>
        </div>
      </header>

      <main className="container mx-auto px-4">
        {/* Category Filter */}
        <CategoryFilter
          selectedCategory={selectedCategory}
          onCategoryChange={handleCategoryChange}
        />

        {/* Product Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            {selectedCategory === 'All' ? 'All Products' : `${selectedCategory}`} 
            ({products.length} items)
          </p>
        </div>

        {/* Product Grid */}
        <ProductGrid
          products={products}
          onProductClick={handleProductClick}
        />

        {/* Product Modal */}
        <ProductModal
          product={selectedProduct}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 bg-gray-100">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2024 Carbon-Aware Store - Shop with environmental consciousness</p>
        </div>
      </footer>
    </div>
  );
};

export default EcommerceApp;
