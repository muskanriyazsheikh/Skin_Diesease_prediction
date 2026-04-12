import React from 'react';
import { FiShield, FiMail, FiGithub } from 'react-icons/fi';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-3">SkinAI</h3>
            <p className="text-sm text-gray-400">
              AI-powered skin disease detection system using deep learning technology.
              Fast, accurate, and accessible skin health screening.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/" className="hover:text-white transition-colors">Home</a>
              </li>
              <li>
                <a href="/upload" className="hover:text-white transition-colors">Upload Image</a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-3">Contact</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center space-x-2">
                <FiMail className="text-primary-400" />
                <span>support@skinai.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <FiGithub className="text-primary-400" />
                <a href="#" className="hover:text-white transition-colors">GitHub</a>
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 pt-6 border-t border-gray-800">
          <div className="bg-red-900/20 border border-red-800 rounded-lg p-4 mb-4">
            <div className="flex items-start space-x-2">
              <FiShield className="text-red-400 mt-1 flex-shrink-0" />
              <p className="text-xs text-red-300">
                <strong>Medical Disclaimer:</strong> This application is for informational purposes only and should NOT 
                be considered a medical diagnosis. Always consult with a qualified dermatologist or healthcare 
                professional for proper medical advice, diagnosis, and treatment.
              </p>
            </div>
          </div>
          
          <div className="text-center text-sm text-gray-500">
            <p>&copy; {currentYear} SkinAI. All rights reserved.</p>
            <p className="mt-1">Built with React, Flask, and TensorFlow</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
