import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiUpload, FiClock, FiShield, FiArrowRight, FiActivity, FiEye, FiHeart } from 'react-icons/fi';

const HomePage = () => {
  const features = [
    {
      icon: <FiActivity className="text-4xl text-primary-600" />,
      title: 'AI-Powered Detection',
      description: 'Advanced CNN deep learning model trained on thousands of skin lesion images for accurate classification.',
    },
    {
      icon: <FiClock className="text-4xl text-secondary-600" />,
      title: 'Instant Results',
      description: 'Get prediction results in seconds with detailed confidence scores and probability breakdowns.',
    },
    {
      icon: <FiShield className="text-4xl text-green-600" />,
      title: 'Treatment Guidance',
      description: 'Receive comprehensive treatment recommendations and precautionary measures for detected conditions.',
    },
  ];

  const steps = [
    {
      icon: <FiUpload className="text-3xl" />,
      title: 'Upload Image',
      description: 'Take or upload a clear photo of the skin lesion',
    },
    {
      icon: <FiEye className="text-3xl" />,
      title: 'AI Analysis',
      description: 'Our CNN model analyzes the image instantly',
    },
    {
      icon: <FiHeart className="text-3xl" />,
      title: 'Get Results',
      description: 'View prediction, confidence score, and treatment info',
    },
  ];

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 text-white py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-5xl mx-auto text-center relative z-10"
        >
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
            AI-Powered Skin Disease
            <span className="block text-secondary-300">Detection System</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-100 max-w-3xl mx-auto">
            Advanced deep learning technology to help identify skin conditions quickly and accurately.
            Get instant analysis with treatment recommendations.
          </p>
          <Link
            to="/upload"
            className="inline-flex items-center space-x-2 bg-white text-primary-700 font-bold py-4 px-8 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg"
          >
            <FiUpload />
            <span>Start Detection</span>
            <FiArrowRight />
          </Link>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-4xl font-bold text-center mb-12 text-gradient"
          >
            Why Choose SkinAI?
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="card text-center hover:transform hover:scale-105 transition-all duration-300"
              >
                <div className="flex justify-center mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-5xl mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-4xl font-bold text-center mb-12 text-gradient"
          >
            How It Works
          </motion.h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="relative"
              >
                <div className="card text-center">
                  <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 text-primary-600">
                    {step.icon}
                  </div>
                  <div className="absolute -top-3 -right-3 bg-primary-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                  <p className="text-gray-600">{step.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-white">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto text-center"
        >
          <h2 className="text-4xl font-bold mb-6 text-gradient">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-gray-700 mb-8">
            Upload your skin image now and receive instant AI-powered analysis with detailed treatment recommendations.
          </p>
          <Link
            to="/upload"
            className="btn-primary inline-flex items-center space-x-2 text-lg"
          >
            <FiUpload />
            <span>Upload Image Now</span>
            <FiArrowRight />
          </Link>
        </motion.div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-8 px-4 bg-red-50 border-t-2 border-red-200">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm text-red-700">
            <strong>Disclaimer:</strong> This application is for informational purposes only and should NOT be 
            considered a medical diagnosis. Always consult with a qualified dermatologist for proper medical advice.
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
