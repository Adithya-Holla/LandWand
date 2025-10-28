import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { StatCard, PropertyCard } from '../components/Card';
import { propertyAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [properties, setProperties] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch properties from API
  const fetchProperties = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch properties from backend
      const response = await propertyAPI.getAll();
      
      if (response.status === 'success') {
        // Transform backend data to match frontend format
        const transformedProperties = response.data.map(prop => ({
          id: prop.property_id,
          name: prop.title,
          location: `Location ID: ${prop.location_id}`, // We'll enhance this later
          area: `Property #${prop.property_id}`,
          type: prop.property_type,
          status: 'Available', // Default status, will be enhanced with listing data
          price: `₹${(prop.price / 100000).toFixed(2)}L`,
          lastUpdated: new Date(prop.posted_date).toLocaleDateString('en-IN')
        }));
        
        setProperties(transformedProperties);
        
        // Calculate stats from properties
        const totalProps = transformedProperties.length;
        const availableProps = transformedProperties.filter(p => p.status === 'Available').length;
        const soldProps = transformedProperties.filter(p => p.status === 'Sold').length;
        const totalRevenue = response.data.reduce((sum, prop) => sum + prop.price, 0);
        
        setStats({
          totalProperties: totalProps,
          availableProperties: availableProps,
          soldProperties: soldProps,
          totalRevenue: `₹${(totalRevenue / 10000000).toFixed(1)}M`
        });
      }
      
      setLoading(false);
    } catch (err) {
      console.error('Error fetching properties:', err);
      setError('Failed to load properties. Please ensure the backend server is running.');
      setLoading(false);
    }
  };

  // Fetch properties on component mount
  useEffect(() => {
    fetchProperties();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredProperties = properties.filter(property => {
    const matchesSearch = property.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         property.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || property.status.toLowerCase().includes(filterStatus.toLowerCase());
    return matchesSearch && matchesFilter;
  });

  const handlePropertyClick = (property) => {
    navigate(`/details/${property.id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-dark-text-secondary">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Error Banner */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 mx-4 mt-4 rounded-lg flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
          <button 
            onClick={fetchProperties}
            className="bg-red-500/20 hover:bg-red-500/30 px-3 py-1 rounded text-sm transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Header */}
      <div className="bg-dark-card shadow-sm border-b border-dark-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-dark-text">Dashboard</h1>
              <p className="text-dark-text-secondary mt-1">Manage your land properties and analytics</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button className="bg-gradient-to-r from-primary-500 to-accent-cyan text-white px-4 py-2 rounded-lg hover:from-primary-600 hover:to-primary-500 transition-all font-medium shadow-lg shadow-primary-500/20">
                + Add Property
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-dark-border">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', name: 'Overview', icon: '📊' },
                { id: 'properties', name: 'Properties', icon: '🏘️' },
                { id: 'analytics', name: 'Analytics', icon: '📈' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-400'
                      : 'border-transparent text-dark-text-secondary hover:text-dark-text hover:border-dark-hover'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title="Total Properties"
                value={stats.totalProperties?.toLocaleString()}
                change="+12%"
                changeType="positive"
                icon="🏘️"
              />
              <StatCard
                title="Available"
                value={stats.availableProperties?.toLocaleString()}
                change="+8%"
                changeType="positive"
                icon="✅"
              />
              <StatCard
                title="Sold"
                value={stats.soldProperties?.toLocaleString()}
                change="+23%"
                changeType="positive"
                icon="💰"
              />
              <StatCard
                title="Total Revenue"
                value={stats.totalRevenue}
                change="+18%"
                changeType="positive"
                icon="📈"
              />
            </div>

            {/* Recent Activity */}
            <div className="bg-dark-card rounded-lg shadow-lg border border-dark-border">
              <div className="px-6 py-4 border-b border-dark-border">
                <h2 className="text-lg font-semibold text-dark-text">Recent Activity</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {[
                    { action: 'New property added', property: 'Sunset Gardens', time: '2 hours ago', type: 'success' },
                    { action: 'Property sold', property: 'Commercial Hub', time: '1 day ago', type: 'info' },
                    { action: 'Price updated', property: 'Green Valley Estate', time: '3 days ago', type: 'warning' },
                    { action: 'Property inquiry', property: 'Tech Park Land', time: '5 days ago', type: 'info' }
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center space-x-4 p-3 bg-dark-hover rounded-lg">
                      <div className={`w-2 h-2 rounded-full ${
                        activity.type === 'success' ? 'bg-primary-400' :
                        activity.type === 'info' ? 'bg-accent-cyan' :
                        activity.type === 'warning' ? 'bg-yellow-400' : 'bg-dark-text-muted'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm text-dark-text">
                          <span className="font-medium">{activity.action}:</span> {activity.property}
                        </p>
                        <p className="text-xs text-dark-text-muted">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Properties Tab */}
        {activeTab === 'properties' && (
          <div className="space-y-6">
            {/* Search and Filter */}
            <div className="bg-dark-card rounded-lg shadow-lg border border-dark-border p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Search properties by name or location..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-dark-text placeholder-dark-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
                <div className="flex space-x-4">
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="px-4 py-2 bg-dark-bg border border-dark-border rounded-lg text-dark-text focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="all">All Status</option>
                    <option value="available">Available</option>
                    <option value="sold">Sold</option>
                    <option value="under review">Under Review</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Properties Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProperties.map((property) => (
                <PropertyCard
                  key={property.id}
                  property={property}
                  onClick={handlePropertyClick}
                />
              ))}
            </div>

            {filteredProperties.length === 0 && (
              <div className="text-center py-12">
                <div className="text-dark-text-muted text-6xl mb-4">🔍</div>
                <h3 className="text-lg font-medium text-dark-text mb-2">No properties found</h3>
                <p className="text-dark-text-secondary">Try adjusting your search or filter criteria</p>
              </div>
            )}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Charts Placeholder */}
              <div className="bg-dark-card rounded-lg shadow-lg border border-dark-border p-6">
                <h3 className="text-lg font-semibold text-dark-text mb-4">Property Types Distribution</h3>
                <div className="h-64 bg-dark-hover rounded-lg flex items-center justify-center">
                  <div className="text-center text-dark-text-secondary">
                    <div className="text-4xl mb-2">📊</div>
                    <p>Chart visualization coming soon</p>
                  </div>
                </div>
              </div>

              <div className="bg-dark-card rounded-lg shadow-lg border border-dark-border p-6">
                <h3 className="text-lg font-semibold text-dark-text mb-4">Sales Trend</h3>
                <div className="h-64 bg-dark-hover rounded-lg flex items-center justify-center">
                  <div className="text-center text-dark-text-secondary">
                    <div className="text-4xl mb-2">📈</div>
                    <p>Chart visualization coming soon</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="bg-dark-card rounded-lg shadow-lg border border-dark-border p-6">
              <h3 className="text-lg font-semibold text-dark-text mb-4">Performance Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-400">89%</div>
                  <div className="text-sm text-dark-text-secondary">Occupancy Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-cyan">24</div>
                  <div className="text-sm text-dark-text-secondary">Avg. Days to Sell</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400">₹2.8L</div>
                  <div className="text-sm text-dark-text-secondary">Avg. Price per Acre</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-400">156</div>
                  <div className="text-sm text-dark-text-secondary">Active Inquiries</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
