import React from 'react';
import { motion } from 'framer-motion';

const ConfidenceBar = ({ confidence, showLabel = true }) => {
  // Determine color based on confidence level
  const getColor = () => {
    if (confidence >= 0.8) return { bg: 'bg-green-500', text: 'text-green-700', label: 'High Confidence' };
    if (confidence >= 0.6) return { bg: 'bg-yellow-500', text: 'text-yellow-700', label: 'Moderate Confidence' };
    return { bg: 'bg-red-500', text: 'text-red-700', label: 'Low Confidence' };
  };

  const { bg, text, label } = getColor();
  const percentage = (confidence * 100).toFixed(1);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="w-full"
    >
      {showLabel && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Confidence Level</span>
          <span className={`text-sm font-semibold ${text}`}>{label}</span>
        </div>
      )}
      
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full ${bg} rounded-full relative`}
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <span className="text-xs font-bold text-white drop-shadow-md">
              {percentage}%
            </span>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default ConfidenceBar;
