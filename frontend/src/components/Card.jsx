import React from 'react';

const Card = ({ title, value, change, changeType, icon, subtitle, className = '' }) => {
  const getChangeColor = () => {
    if (changeType === 'positive') return 'text-green-600';
    if (changeType === 'negative') return 'text-red-600';
    return 'text-gray-600';
  };

  const getChangeIcon = () => {
    if (changeType === 'positive') return '↗';
    if (changeType === 'negative') return '↘';
    return '→';
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            {icon && (
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-green-600 text-lg">{icon}</span>
              </div>
            )}
            <div>
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">{title}</h3>
              {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
            </div>
          </div>
          
          <div className="mt-4">
            <div className="text-2xl font-bold text-gray-900">{value}</div>
            {change && (
              <div className={`flex items-center mt-2 text-sm ${getChangeColor()}`}>
                <span className="mr-1">{getChangeIcon()}</span>
                <span>{change}</span>
                <span className="text-gray-500 ml-1">from last month</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Specialized card components
export const StatCard = ({ title, value, change, changeType, icon }) => (
  <Card
    title={title}
    value={value}
    change={change}
    changeType={changeType}
    icon={icon}
  />
);

export const PropertyCard = ({ property, onClick }) => (
  <div 
    className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow cursor-pointer"
    onClick={() => onClick && onClick(property)}
  >
    <div className="h-48 bg-gradient-to-r from-green-400 to-green-600 relative">
      <div className="absolute inset-0 bg-black bg-opacity-20"></div>
      <div className="absolute bottom-4 left-4 text-white">
        <h3 className="text-lg font-semibold">{property.name}</h3>
        <p className="text-sm opacity-90">{property.location}</p>
      </div>
    </div>
    
    <div className="p-4">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-gray-600">Area</span>
        <span className="font-semibold text-gray-900">{property.area}</span>
      </div>
      
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-gray-600">Type</span>
        <span className="font-semibold text-gray-900">{property.type}</span>
      </div>
      
      <div className="flex justify-between items-center mb-4">
        <span className="text-sm text-gray-600">Status</span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          property.status === 'Available' 
            ? 'bg-green-100 text-green-800' 
            : property.status === 'Sold'
            ? 'bg-red-100 text-red-800'
            : 'bg-yellow-100 text-yellow-800'
        }`}>
          {property.status}
        </span>
      </div>
      
      <div className="border-t pt-4">
        <div className="flex justify-between items-center">
          <span className="text-lg font-bold text-green-600">{property.price}</span>
          <button className="text-green-600 hover:text-green-700 text-sm font-medium">
            View Details →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default Card;
