import React, { useState } from 'react';
import EcommerceApp from './pages/EcommerceApp';
import CarbonScoreForm from './pages/CarbonScoreForm';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('ecommerce');

  const toggleView = () => {
    setCurrentView(currentView === 'ecommerce' ? 'calculator' : 'ecommerce');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h2 className="text-xl font-bold text-gray-800">Carbon-Aware Platform</h2>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setCurrentView('ecommerce')}
                className={`px-4 py-2 rounded-md transition-colors ${
                  currentView === 'ecommerce'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Store
              </button>
              <button
                onClick={() => setCurrentView('calculator')}
                className={`px-4 py-2 rounded-md transition-colors ${
                  currentView === 'calculator'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Calculator
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      {currentView === 'ecommerce' ? (
        <EcommerceApp />
      ) : (
        <div className="min-h-screen bg-gray-50">
          <header className="bg-green-600 text-white py-6 mb-8">
            <div className="container mx-auto px-4">
              <h1 className="text-3xl font-bold">Carbon Score Calculator</h1>
              <p className="mt-2">Calculate and compare product carbon scores to check the carbon footprint of the product</p>
            </div>
          </header>

          <main className="container mx-auto px-4">
            <CarbonScoreForm />
          </main>

          <footer className="mt-12 py-6 bg-gray-100">
            <div className="container mx-auto px-4 text-center text-gray-600">
              <p>© 2024 Carbon-Aware Product Recommendation Engine</p>
            </div>
          </footer>
        </div>
      )}
    </div>
  );
}

export default App;
