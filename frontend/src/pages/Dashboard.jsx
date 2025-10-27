import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { StatCard, PropertyCard } from '../components/Card';

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [properties, setProperties] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  // Mock data - In real app, this would come from API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setStats({
        totalProperties: 1247,
        availableProperties: 892,
        soldProperties: 234,
        totalRevenue: '$2.4M'
      });

      setProperties([
        {
          id: 1,
          name: 'Green Valley Estate',
          location: 'North Bangalore',
          area: '2.5 acres',
          type: 'Residential',
          status: 'Available',
          price: '₹45,00,000',
          lastUpdated: '2 days ago'
        },
        {
          id: 2,
          name: 'Commercial Hub',
          location: 'Electronic City',
          area: '1.8 acres',
          type: 'Commercial',
          status: 'Sold',
          price: '₹1,20,00,000',
          lastUpdated: '1 week ago'
        },
        {
          id: 3,
          name: 'Sunset Gardens',
          location: 'Whitefield',
          area: '3.2 acres',
          type: 'Residential',
          status: 'Available',
          price: '₹67,50,000',
          lastUpdated: '5 hours ago'
        },
        {
          id: 4,
          name: 'Tech Park Land',
          location: 'Sarjapur',
          area: '5.0 acres',
          type: 'Commercial',
          status: 'Under Review',
          price: '₹2,50,00,000',
          lastUpdated: '3 days ago'
        },
        {
          id: 5,
          name: 'Lakeside Plots',
          location: 'Hebbal',
          area: '1.2 acres',
          type: 'Residential',
          status: 'Available',
          price: '₹35,00,000',
          lastUpdated: '1 day ago'
        },
        {
          id: 6,
          name: 'Industrial Zone',
          location: 'Peenya',
          area: '8.7 acres',
          type: 'Industrial',
          status: 'Available',
          price: '₹4,20,00,000',
          lastUpdated: '6 hours ago'
        }
      ]);

      setLoading(false);
    }, 1000);
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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600 mt-1">Manage your land properties and analytics</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">
                + Add Property
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', name: 'Overview', icon: '📊' },
                { id: 'properties', name: 'Properties', icon: '🏘️' },
                { id: 'analytics', name: 'Analytics', icon: '📈' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-green-500 text-green-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
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
            <div className="bg-white rounded-lg shadow-md border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {[
                    { action: 'New property added', property: 'Sunset Gardens', time: '2 hours ago', type: 'success' },
                    { action: 'Property sold', property: 'Commercial Hub', time: '1 day ago', type: 'info' },
                    { action: 'Price updated', property: 'Green Valley Estate', time: '3 days ago', type: 'warning' },
                    { action: 'Property inquiry', property: 'Tech Park Land', time: '5 days ago', type: 'info' }
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
                      <div className={`w-2 h-2 rounded-full ${
                        activity.type === 'success' ? 'bg-green-500' :
                        activity.type === 'info' ? 'bg-blue-500' :
                        activity.type === 'warning' ? 'bg-yellow-500' : 'bg-gray-500'
                      }`}></div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">
                          <span className="font-medium">{activity.action}:</span> {activity.property}
                        </p>
                        <p className="text-xs text-gray-500">{activity.time}</p>
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
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Search properties by name or location..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
                <div className="flex space-x-4">
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
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
                <div className="text-gray-400 text-6xl mb-4">🔍</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No properties found</h3>
                <p className="text-gray-600">Try adjusting your search or filter criteria</p>
              </div>
            )}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Charts Placeholder */}
              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Property Types Distribution</h3>
                <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <div className="text-4xl mb-2">📊</div>
                    <p>Chart visualization coming soon</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Sales Trend</h3>
                <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <div className="text-4xl mb-2">📈</div>
                    <p>Chart visualization coming soon</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Summary Stats */}
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">89%</div>
                  <div className="text-sm text-gray-600">Occupancy Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">24</div>
                  <div className="text-sm text-gray-600">Avg. Days to Sell</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">₹2.8L</div>
                  <div className="text-sm text-gray-600">Avg. Price per Acre</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">156</div>
                  <div className="text-sm text-gray-600">Active Inquiries</div>
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
