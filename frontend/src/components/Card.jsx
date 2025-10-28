import React from 'react';

const Card = ({ title, value, change, changeType, icon, subtitle, className = '' }) => {
  const getChangeColor = () => {
    if (changeType === 'positive') return 'text-primary-400';
    if (changeType === 'negative') return 'text-red-400';
    return 'text-dark-text-secondary';
  };

  const getChangeIcon = () => {
    if (changeType === 'positive') return '↗';
    if (changeType === 'negative') return '↘';
    return '→';
  };

  return (
    <div className={`bg-dark-card rounded-lg shadow-lg p-6 border border-dark-border hover:border-primary-500 hover:shadow-primary-500/10 transition-all ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            {icon && (
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500/20 to-accent-cyan/20 rounded-lg flex items-center justify-center border border-primary-500/30">
                <span className="text-primary-400 text-lg">{icon}</span>
              </div>
            )}
            <div>
              <h3 className="text-sm font-medium text-dark-text-secondary uppercase tracking-wide">{title}</h3>
              {subtitle && <p className="text-xs text-dark-text-muted mt-1">{subtitle}</p>}
            </div>
          </div>
          
          <div className="mt-4">
            <div className="text-2xl font-bold text-dark-text">{value}</div>
            {change && (
              <div className={`flex items-center mt-2 text-sm ${getChangeColor()}`}>
                <span className="mr-1">{getChangeIcon()}</span>
                <span>{change}</span>
                <span className="text-dark-text-muted ml-1">from last month</span>
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
    className="bg-dark-card rounded-lg shadow-lg overflow-hidden border border-dark-border hover:border-primary-500 hover:shadow-primary-500/10 transition-all cursor-pointer group"
    onClick={() => onClick && onClick(property)}
  >
    <div className="h-48 bg-gradient-to-r from-primary-600 to-accent-cyan relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-dark-bg/40"></div>
      <div className="absolute bottom-4 left-4 text-white">
        <h3 className="text-lg font-semibold group-hover:scale-105 transition-transform">{property.name}</h3>
        <p className="text-sm opacity-90">{property.location}</p>
      </div>
    </div>
    
    <div className="p-4">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-dark-text-muted">Area</span>
        <span className="font-semibold text-dark-text">{property.area}</span>
      </div>
      
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm text-dark-text-muted">Type</span>
        <span className="font-semibold text-dark-text">{property.type}</span>
      </div>
      
      <div className="flex justify-between items-center mb-4">
        <span className="text-sm text-dark-text-muted">Status</span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          property.status === 'Available' 
            ? 'bg-primary-500/20 text-primary-300 border border-primary-500/30' 
            : property.status === 'Sold'
            ? 'bg-red-500/20 text-red-300 border border-red-500/30'
            : 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30'
        }`}>
          {property.status}
        </span>
      </div>
      
      <div className="border-t border-dark-border pt-4">
        <div className="flex justify-between items-center">
          <span className="text-lg font-bold bg-gradient-to-r from-primary-400 to-accent-cyan bg-clip-text text-transparent">{property.price}</span>
          <button className="text-primary-400 hover:text-primary-300 text-sm font-medium group-hover:translate-x-1 transition-transform">
            View Details →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default Card;
