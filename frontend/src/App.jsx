import React from 'react';
import CarbonScoreForm from './components/CarbonScoreForm';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-green-600 text-white py-6 mb-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">Carbon-Aware Product Recommendation</h1>
          <p className="mt-2">Calculate and compare product carbon scores to find greener alternatives</p>
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
  );
}

export default App;
