import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const Details = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeImageIndex, setActiveImageIndex] = useState(0);

  // Mock data - In real app, this would come from API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockProperty = {
        id: parseInt(id),
        name: 'Green Valley Estate',
        location: 'North Bangalore, Karnataka',
        area: '2.5 acres',
        type: 'Residential',
        status: 'Available',
        price: '₹45,00,000',
        pricePerAcre: '₹18,00,000',
        description: 'Beautiful residential land in the heart of North Bangalore. Perfect for building your dream home or investment property. The land features excellent connectivity to major highways and is surrounded by lush greenery.',
        features: [
          'Prime location with excellent connectivity',
          'Clear title and all approvals in place',
          'Surrounded by developed infrastructure',
          'Close to schools, hospitals, and shopping centers',
          'Peaceful and serene environment',
          'Investment potential with high appreciation'
        ],
        specifications: {
          'Total Area': '2.5 acres',
          'Plot Type': 'Residential',
          'Facing': 'North-East',
          'Road Width': '40 feet',
          'Electricity': 'Available',
          'Water Supply': 'Borewell + Corporation',
          'Approvals': 'BMRDA Approved',
          'Possession': 'Immediate'
        },
        location_details: {
          'Distance to Airport': '25 km',
          'Distance to Railway Station': '12 km',
          'Distance to IT Hub': '18 km',
          'Distance to Hospital': '3 km',
          'Distance to School': '1.5 km',
          'Distance to Mall': '5 km'
        },
        images: [
          '/api/placeholder/600/400',
          '/api/placeholder/600/400',
          '/api/placeholder/600/400',
          '/api/placeholder/600/400'
        ],
        owner: {
          name: 'Rajesh Kumar',
          phone: '+91 9876543210',
          email: 'rajesh.kumar@email.com'
        },
        lastUpdated: '2 days ago',
        viewCount: 156,
        inquiries: 23
      };
      
      setProperty(mockProperty);
      setLoading(false);
    }, 1000);
  }, [id]);

  const handleInquiry = () => {
    alert('Inquiry form would open here. This feature will be implemented with the backend.');
  };

  const handleCallOwner = () => {
    if (property?.owner?.phone) {
      window.open(`tel:${property.owner.phone}`);
    }
  };

  const handleEmailOwner = () => {
    if (property?.owner?.email) {
      window.open(`mailto:${property.owner.email}?subject=Inquiry about ${property.name}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading property details...</p>
        </div>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl text-gray-400 mb-4">🏠</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Property Not Found</h2>
          <p className="text-gray-600 mb-6">The property you're looking for doesn't exist or has been removed.</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-600 hover:text-green-600 flex items-center space-x-2"
            >
              <span>←</span>
              <span>Back to Dashboard</span>
            </button>
            <span className="text-gray-300">|</span>
            <span className="text-gray-600">Property Details</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Property Images */}
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative">
                <div className="h-96 bg-gradient-to-r from-green-400 to-green-600 flex items-center justify-center">
                  <div className="text-center text-white">
                    <div className="text-6xl mb-4">🏞️</div>
                    <p className="text-lg">Property Image Placeholder</p>
                    <p className="text-sm opacity-75">Images will be loaded from API</p>
                  </div>
                </div>
                
                {/* Status Badge */}
                <div className="absolute top-4 left-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    property.status === 'Available' 
                      ? 'bg-green-100 text-green-800' 
                      : property.status === 'Sold'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {property.status}
                  </span>
                </div>

                {/* View Count */}
                <div className="absolute top-4 right-4 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
                  👁️ {property.viewCount} views
                </div>
              </div>
            </div>

            {/* Property Information */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-6">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{property.name}</h1>
                  <p className="text-gray-600 flex items-center space-x-2">
                    <span>📍</span>
                    <span>{property.location}</span>
                  </p>
                </div>
                <div className="mt-4 sm:mt-0 text-right">
                  <div className="text-3xl font-bold text-green-600">{property.price}</div>
                  <div className="text-sm text-gray-600">{property.pricePerAcre} per acre</div>
                </div>
              </div>

              <div className="border-t pt-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Description</h2>
                <p className="text-gray-700 leading-relaxed mb-6">
                  {property.description}
                </p>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">Key Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {property.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <span className="text-green-600">✓</span>
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Specifications */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Specifications</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(property.specifications).map(([key, value]) => (
                  <div key={key} className="flex justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-gray-700">{key}</span>
                    <span className="text-gray-900">{value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Location Details */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Location & Connectivity</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(property.location_details).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center p-3 border border-gray-200 rounded-lg">
                    <span className="text-gray-700">{key}</span>
                    <span className="font-medium text-gray-900">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Contact Card */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Owner</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600">Owner</p>
                  <p className="font-medium text-gray-900">{property.owner.name}</p>
                </div>
                
                <div className="space-y-2">
                  <button
                    onClick={handleCallOwner}
                    className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                  >
                    <span>📞</span>
                    <span>Call Owner</span>
                  </button>
                  
                  <button
                    onClick={handleEmailOwner}
                    className="w-full border border-green-600 text-green-600 py-2 px-4 rounded-lg hover:bg-green-50 transition-colors flex items-center justify-center space-x-2"
                  >
                    <span>✉️</span>
                    <span>Email Owner</span>
                  </button>
                  
                  <button
                    onClick={handleInquiry}
                    className="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center space-x-2"
                  >
                    <span>❓</span>
                    <span>Send Inquiry</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Property Stats */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Property Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Total Views</span>
                  <span className="font-medium text-gray-900">{property.viewCount}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Inquiries</span>
                  <span className="font-medium text-gray-900">{property.inquiries}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Last Updated</span>
                  <span className="font-medium text-gray-900">{property.lastUpdated}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Property ID</span>
                  <span className="font-medium text-gray-900">#{property.id.toString().padStart(6, '0')}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-2">
                <button className="w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                  📤 Share Property
                </button>
                <button className="w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                  ❤️ Add to Favorites
                </button>
                <button className="w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                  📊 View Analytics
                </button>
                <button className="w-full text-left px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                  ✏️ Edit Property
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Details;
