import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const features = [
    {
      icon: '🏘️',
      title: 'Property Management',
      description: 'Efficiently manage all your land properties in one centralized dashboard.'
    },
    {
      icon: '📊',
      title: 'Analytics & Insights',
      description: 'Get detailed analytics and insights about your property portfolio performance.'
    },
    {
      icon: '🔍',
      title: 'Smart Search',
      description: 'Quickly find properties using our advanced search and filtering capabilities.'
    },
    {
      icon: '💰',
      title: 'Revenue Tracking',
      description: 'Track sales, revenue, and financial performance across all properties.'
    },
    {
      icon: '📱',
      title: 'Mobile Responsive',
      description: 'Access your dashboard anywhere, anytime with our mobile-friendly design.'
    },
    {
      icon: '🔒',
      title: 'Secure & Reliable',
      description: 'Your data is protected with enterprise-grade security and reliability.'
    }
  ];

  const stats = [
    { number: '1,200+', label: 'Properties Managed' },
    { number: '₹50M+', label: 'Total Value' },
    { number: '500+', label: 'Happy Clients' },
    { number: '99.9%', label: 'Uptime' }
  ];

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-600 via-primary-500 to-accent-cyan text-white overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-dark-bg/20"></div>
        {/* Animated background elements */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 left-10 w-72 h-72 bg-accent-cyan rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-72 h-72 bg-primary-400 rounded-full mix-blend-multiply filter blur-xl animate-pulse delay-700"></div>
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Welcome to <span className="text-primary-200 bg-clip-text bg-gradient-to-r from-primary-200 to-cyan-200">LandWand</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-50 max-w-3xl mx-auto">
              Your complete solution for land and property management. Streamline operations, 
              track performance, and make data-driven decisions.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/dashboard"
                className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-all shadow-xl hover:shadow-2xl hover:scale-105 inline-flex items-center justify-center"
              >
                Go to Dashboard →
              </Link>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-all backdrop-blur-sm">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-dark-card border-y border-dark-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary-400 to-accent-cyan bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform">
                  {stat.number}
                </div>
                <div className="text-dark-text-secondary font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-dark-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-dark-text mb-4">
              Powerful Features for Land Management
            </h2>
            <p className="text-xl text-dark-text-secondary max-w-3xl mx-auto">
              Everything you need to manage your land properties efficiently and effectively.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-dark-card rounded-lg shadow-lg p-6 border border-dark-border hover:border-primary-500 transition-all hover:shadow-primary-500/10 group"
              >
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-dark-text mb-3">
                  {feature.title}
                </h3>
                <p className="text-dark-text-secondary leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-primary-600 via-primary-500 to-accent-cyan relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-0 right-0 w-96 h-96 bg-accent-cyan rounded-full mix-blend-multiply filter blur-xl"></div>
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-primary-50 mb-8 max-w-2xl mx-auto">
            Join thousands of property managers who trust LandWand for their land management needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-all shadow-xl hover:shadow-2xl hover:scale-105 inline-flex items-center justify-center"
            >
              Explore Dashboard
            </Link>
            <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-all backdrop-blur-sm">
              Contact Sales
            </button>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-dark-card border-y border-dark-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-dark-text mb-4">
              How LandWand Works
            </h2>
            <p className="text-xl text-dark-text-secondary">
              Simple steps to get started with land management
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-accent-cyan rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-primary-500/20">
                <span className="text-2xl text-white font-bold">1</span>
              </div>
              <h3 className="text-xl font-semibold text-dark-text mb-3">Add Properties</h3>
              <p className="text-dark-text-secondary">
                Add your land properties with detailed information including location, area, and pricing.
              </p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-accent-cyan rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-primary-500/20">
                <span className="text-2xl text-white font-bold">2</span>
              </div>
              <h3 className="text-xl font-semibold text-dark-text mb-3">Monitor Performance</h3>
              <p className="text-dark-text-secondary">
                Track sales, analyze trends, and monitor the performance of your property portfolio.
              </p>
            </div>

            <div className="text-center group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-accent-cyan rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-primary-500/20">
                <span className="text-2xl text-white font-bold">3</span>
              </div>
              <h3 className="text-xl font-semibold text-dark-text mb-3">Make Decisions</h3>
              <p className="text-dark-text-secondary">
                Use data-driven insights to make informed decisions about pricing, marketing, and sales.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
