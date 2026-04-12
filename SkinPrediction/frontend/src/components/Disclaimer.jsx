import React from 'react';
import { motion } from 'framer-motion';
import { FiAlertTriangle } from 'react-icons/fi';

const Disclaimer = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500 rounded-lg p-4 my-6"
    >
      <div className="flex items-start space-x-3">
        <FiAlertTriangle className="text-red-600 text-xl flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="font-semibold text-red-800 mb-1">Medical Disclaimer</h4>
          <p className="text-sm text-red-700">
            <strong>IMPORTANT:</strong> This AI-based prediction is for informational purposes only and should NOT be 
            considered a medical diagnosis. Always consult with a qualified dermatologist or healthcare professional 
            for proper medical advice, diagnosis, and treatment. Skin conditions require professional evaluation, 
            and some may require biopsy for definitive diagnosis.
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default Disclaimer;
