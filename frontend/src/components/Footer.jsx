import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark-card border-t border-dark-border text-dark-text">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-cyan rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">L</span>
              </div>
              <span className="text-xl font-bold">LandWand</span>
            </div>
            <p className="text-dark-text-secondary mb-6 max-w-md">
              Your complete solution for land and property management. Streamline operations, 
              track performance, and make data-driven decisions with ease.
            </p>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-dark-text-secondary hover:text-primary-400 transition-colors"
                aria-label="Facebook"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
              <a
                href="#"
                className="text-dark-text-secondary hover:text-primary-400 transition-colors"
                aria-label="Twitter"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
              <a
                href="#"
                className="text-dark-text-secondary hover:text-primary-400 transition-colors"
                aria-label="LinkedIn"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
              <a
                href="#"
                className="text-dark-text-secondary hover:text-primary-400 transition-colors"
                aria-label="Instagram"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.624 5.367 11.99 11.988 11.99s11.987-5.366 11.987-11.99C23.971 5.39 18.641.026 12.017 0zm4.624 12.492c0 2.506-2.031 4.537-4.537 4.537s-4.537-2.031-4.537-4.537 2.031-4.537 4.537-4.537 4.537 2.031 4.537 4.537zm3.415-7.418c-.584 0-1.059-.474-1.059-1.059s.474-1.059 1.059-1.059 1.059.474 1.059 1.059-.474 1.059-1.059 1.059z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Dashboard
                </Link>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Services
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Community
                </a>
              </li>
              <li>
                <a href="#" className="text-dark-text-secondary hover:text-primary-400 transition-colors">
                  Status Page
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Newsletter Signup */}
        <div className="border-t border-dark-border py-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold mb-2">Stay Updated</h3>
              <p className="text-dark-text-secondary">Get the latest updates and news about LandWand.</p>
            </div>
            <div className="flex flex-col sm:flex-row gap-2 max-w-md">
              <input
                type="email"
                placeholder="Enter your email"
                className="px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-dark-text placeholder-dark-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent flex-1"
              />
              <button className="bg-gradient-to-r from-primary-500 to-accent-cyan text-white px-6 py-2 rounded-lg hover:from-primary-600 hover:to-primary-500 transition-all whitespace-nowrap shadow-lg shadow-primary-500/20">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Footer */}
        <div className="border-t border-dark-border py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <p className="text-dark-text-secondary text-sm">
              © {currentYear} LandWand. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-dark-text-secondary hover:text-primary-400 text-sm transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-dark-text-secondary hover:text-primary-400 text-sm transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-dark-text-secondary hover:text-primary-400 text-sm transition-colors">
                Cookie Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
