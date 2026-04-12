import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiUpload, FiAlertTriangle, FiCheckCircle, FiInfo, FiShield } from 'react-icons/fi';
import ConfidenceBar from '../components/ConfidenceBar';
import Disclaimer from '../components/Disclaimer';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { prediction } = location.state || {};

  if (!prediction) {
    return (
      <div className="min-h-screen flex items-center justify-center py-12 px-4">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">No Prediction Data</h2>
          <p className="text-gray-600 mb-6">Please upload an image first.</p>
          <button onClick={() => navigate('/upload')} className="btn-primary">
            Go to Upload
          </button>
        </div>
      </div>
    );
  }

  const { prediction: predData, disease_info, disclaimer } = prediction;
  const severityColor = {
    'Low': 'bg-green-100 text-green-800 border-green-300',
    'Low-Medium': 'bg-blue-100 text-blue-800 border-blue-300',
    'Medium': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'Medium-High': 'bg-orange-100 text-orange-800 border-orange-300',
    'High': 'bg-red-100 text-red-800 border-red-300',
  };

  return (
    <div className="min-h-screen py-12 px-4 animate-fade-in">
      <div className="max-w-5xl mx-auto">
        {/* Back Button */}
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => navigate('/upload')}
          className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 mb-6 font-medium"
        >
          <FiArrowLeft />
          <span>Upload Another Image</span>
        </motion.button>

        {/* Main Result Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card mb-8"
        >
          {/* Disease Name */}
          <div className="text-center mb-6">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="inline-block bg-gradient-to-r from-primary-600 to-secondary-600 text-white px-6 py-3 rounded-full mb-4"
            >
              <FiCheckCircle className="inline-block mr-2" />
              Prediction Complete
            </motion.div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
              {predData.disease}
            </h1>
            
            {/* Severity Badge */}
            <div className="flex justify-center mb-4">
              <span className={`px-4 py-2 rounded-full border text-sm font-semibold ${severityColor[disease_info.severity] || 'bg-gray-100 text-gray-800 border-gray-300'}`}>
                Severity: {disease_info.severity}
              </span>
            </div>
          </div>

          {/* Confidence Bar */}
          <div className="mb-6">
            <ConfidenceBar confidence={predData.confidence} />
          </div>

          {/* Consultation Urgency */}
          <div className={`p-4 rounded-lg border-2 ${
            disease_info.severity === 'High' 
              ? 'bg-red-50 border-red-300' 
              : disease_info.severity.includes('Medium')
              ? 'bg-yellow-50 border-yellow-300'
              : 'bg-green-50 border-green-300'
          }`}>
            <div className="flex items-start space-x-3">
              <FiAlertTriangle className={`text-xl flex-shrink-0 mt-0.5 ${
                disease_info.severity === 'High' ? 'text-red-600' : 'text-yellow-600'
              }`} />
              <div>
                <h3 className="font-semibold mb-1">Recommended Action</h3>
                <p className="text-sm">{disease_info.consultation}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Disease Information */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"
        >
          {/* Description */}
          <div className="card">
            <div className="flex items-center space-x-2 mb-4">
              <FiInfo className="text-primary-600 text-2xl" />
              <h2 className="text-2xl font-bold text-gray-900">Description</h2>
            </div>
            <p className="text-gray-700 leading-relaxed">{disease_info.description}</p>
          </div>

          {/* Symptoms */}
          <div className="card">
            <div className="flex items-center space-x-2 mb-4">
              <FiAlertTriangle className="text-orange-600 text-2xl" />
              <h2 className="text-2xl font-bold text-gray-900">Common Symptoms</h2>
            </div>
            <ul className="space-y-2">
              {disease_info.symptoms.map((symptom, index) => (
                <li key={index} className="flex items-start space-x-2 text-gray-700">
                  <span className="text-orange-500 font-bold mt-1">•</span>
                  <span>{symptom}</span>
                </li>
              ))}
            </ul>
          </div>
        </motion.div>

        {/* Treatment & Precautions */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"
        >
          {/* Treatment */}
          <div className="card bg-blue-50 border border-blue-200">
            <div className="flex items-center space-x-2 mb-4">
              <FiCheckCircle className="text-blue-600 text-2xl" />
              <h2 className="text-2xl font-bold text-blue-900">Treatment</h2>
            </div>
            <p className="text-blue-800 leading-relaxed">{disease_info.treatment}</p>
          </div>

          {/* Precautions */}
          <div className="card bg-green-50 border border-green-200">
            <div className="flex items-center space-x-2 mb-4">
              <FiShield className="text-green-600 text-2xl" />
              <h2 className="text-2xl font-bold text-green-900">Precautions</h2>
            </div>
            <ul className="space-y-2">
              {disease_info.precautions.map((precaution, index) => (
                <li key={index} className="flex items-start space-x-2 text-green-800">
                  <span className="text-green-600 font-bold mt-1">✓</span>
                  <span>{precaution}</span>
                </li>
              ))}
            </ul>
          </div>
        </motion.div>

        {/* All Probabilities */}
        {predData.all_probabilities && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="card mb-8"
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-900">All Class Probabilities</h2>
            <div className="space-y-3">
              {Object.entries(predData.all_probabilities)
                .sort(([, a], [, b]) => b - a)
                .map(([disease, prob]) => (
                  <div key={disease} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 flex-1">{disease}</span>
                    <div className="w-48 mx-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            disease === predData.disease
                              ? 'bg-primary-600'
                              : 'bg-gray-400'
                          }`}
                          style={{ width: `${(prob * 100).toFixed(1)}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-sm font-semibold text-gray-900 w-16 text-right">
                      {(prob * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
            </div>
          </motion.div>
        )}

        {/* Medical Disclaimer */}
        <Disclaimer />

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="flex flex-col sm:flex-row gap-4 justify-center mt-8"
        >
          <button
            onClick={() => navigate('/upload')}
            className="btn-primary flex items-center justify-center space-x-2"
          >
            <FiUpload />
            <span>Analyze Another Image</span>
          </button>
          <button
            onClick={() => navigate('/')}
            className="btn-secondary flex items-center justify-center space-x-2"
          >
            <FiArrowLeft />
            <span>Back to Home</span>
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default ResultPage;
