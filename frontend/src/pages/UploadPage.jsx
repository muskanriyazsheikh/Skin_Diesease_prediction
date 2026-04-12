import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { FiUpload, FiImage, FiX, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';
import { predictDisease } from '../services/api';

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Handle file drop/selection
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError('');
    
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0].code === 'file-too-large') {
        setError('File is too large. Maximum size is 5MB.');
      } else if (rejection.errors[0].code === 'file-invalid-type') {
        setError('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).');
      } else {
        setError('Invalid file. Please try again.');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setSelectedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false,
  });

  // Remove selected file
  const removeFile = () => {
    setSelectedFile(null);
    setPreview(null);
    setError('');
  };

  // Upload and predict
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Send to backend for prediction
      const result = await predictDisease(selectedFile);
      
      // Navigate to result page with data
      navigate('/result', { state: { prediction: result } });
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to process image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 animate-fade-in">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gradient">
            Upload Skin Image
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload a clear photo of the skin lesion for AI-powered analysis.
            Our system will detect the condition and provide treatment recommendations.
          </p>
        </motion.div>

        {/* Upload Area */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          {!preview ? (
            // Dropzone
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200 ${
                isDragActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }`}
            >
              <input {...getInputProps()} />
              <FiUpload className="text-6xl text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-gray-900">
                {isDragActive ? 'Drop image here' : 'Drag & Drop Image'}
              </h3>
              <p className="text-gray-600 mb-4">or click to browse files</p>
              <p className="text-sm text-gray-500">
                Supported formats: PNG, JPG, JPEG, GIF, WEBP (Max: 5MB)
              </p>
            </div>
          ) : (
            // Preview
            <div className="space-y-4">
              <div className="relative">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-96 object-cover rounded-lg"
                />
                <button
                  onClick={removeFile}
                  className="absolute top-4 right-4 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
                  aria-label="Remove image"
                >
                  <FiX size={20} />
                </button>
              </div>
              
              <div className="flex items-center space-x-2 text-green-600">
                <FiCheckCircle />
                <span className="font-medium">Image selected: {selectedFile?.name}</span>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg flex items-start space-x-3"
            >
              <FiAlertCircle className="text-red-600 text-xl flex-shrink-0 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </motion.div>
          )}

          {/* Upload Button */}
          <div className="mt-6">
            <button
              onClick={handleUpload}
              disabled={!selectedFile || loading}
              className="btn-primary w-full flex items-center justify-center space-x-2 text-lg"
            >
              {loading ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  >
                    ⚙️
                  </motion.div>
                  <span>Analyzing Image...</span>
                </>
              ) : (
                <>
                  <FiImage />
                  <span>Analyze Image</span>
                </>
              )}
            </button>
          </div>
        </motion.div>

        {/* Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-8 card bg-blue-50 border border-blue-200"
        >
          <h3 className="text-lg font-semibold mb-3 text-blue-900">Tips for Better Results</h3>
          <ul className="space-y-2 text-sm text-blue-800">
            <li className="flex items-start space-x-2">
              <span className="font-bold">•</span>
              <span>Ensure good lighting and clear focus on the lesion</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="font-bold">•</span>
              <span>Include the entire affected area in the frame</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="font-bold">•</span>
              <span>Avoid blur, shadows, or obstructions</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="font-bold">•</span>
              <span>Take photos from multiple angles if possible</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  );
};

export default UploadPage;
