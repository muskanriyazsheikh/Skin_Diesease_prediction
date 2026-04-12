import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ResultPage from './pages/ResultPage';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-blue-50">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
