# LandWand Frontend

A modern React.js frontend application for land and property management.

## 🚀 Features

- **Modern Dashboard**: Comprehensive dashboard with property analytics and management
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Property Management**: Add, view, edit, and manage land properties
- **Search & Filter**: Advanced search and filtering capabilities
- **Analytics**: Property performance tracking and insights
- **Routing**: Multi-page application with React Router DOM

## 🛠️ Technology Stack

- **React 19.2.0** - UI framework
- **React Router DOM 7.9.4** - Client-side routing
- **Tailwind CSS 4.1.16** - Utility-first CSS framework
- **Axios 1.12.2** - HTTP client for API calls
- **Create React App** - Build tooling and development environment

## 📦 Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Project Structure

```
src/
├── components/          # Reusable React components
│   ├── Card.jsx        # Property cards and stat cards
│   ├── Footer.jsx      # Footer component
│   └── Navbar.jsx      # Navigation bar
├── pages/              # Page components
│   ├── Dashboard.jsx   # Main dashboard page
│   ├── Details.jsx     # Property details page
│   └── home.jsx        # Landing page
├── App.js              # Main application component
├── App.css             # Custom styles
├── index.js            # React DOM entry point
└── index.css           # Global styles with Tailwind
```

## 📱 Pages Overview

### Home Page (`/`)
- Landing page with hero section
- Feature highlights
- Call-to-action sections
- Company statistics

### Dashboard (`/dashboard`)
- **Overview Tab**: Key statistics and recent activity
- **Properties Tab**: Property grid with search and filtering
- **Analytics Tab**: Performance charts and insights
- Responsive design for all screen sizes

### Property Details (`/details/:id`)
- Detailed property information
- Image gallery placeholder
- Owner contact information
- Property specifications
- Location connectivity details

## 🎨 Design System

### Colors
- **Primary Green**: `#16a34a` (green-600)
- **Light Green**: `#22c55e` (green-500)
- **Dark Green**: `#15803d` (green-700)
- **Gray Scale**: Various shades for backgrounds and text

### Components
- **Cards**: Modular card components for properties and statistics
- **Buttons**: Primary, secondary, and outline button styles
- **Forms**: Consistent input and select styling
- **Navigation**: Responsive navbar with mobile menu

## 🔧 Available Scripts

### Development
```bash
npm start          # Start development server
npm test           # Run test suite
npm run build      # Build for production
npm run eject      # Eject from Create React App
```

### Linting and Formatting
```bash
npm run lint       # Run ESLint (if configured)
npm run format     # Format code (if configured)
```

## 🌐 API Integration

The frontend is prepared for backend integration with:
- Axios HTTP client configured
- Mock data structure in place
- API call patterns established
- Error handling prepared

### Expected API Endpoints
```
GET    /api/properties     # Fetch all properties
GET    /api/properties/:id # Fetch single property
POST   /api/properties     # Create new property
PUT    /api/properties/:id # Update property
DELETE /api/properties/:id # Delete property
GET    /api/stats          # Dashboard statistics
```

## 📊 Mock Data Structure

### Property Object
```javascript
{
  id: 1,
  name: "Green Valley Estate",
  location: "North Bangalore",
  area: "2.5 acres",
  type: "Residential",
  status: "Available",
  price: "₹45,00,000",
  description: "...",
  features: [...],
  specifications: {...},
  owner: {...}
}
```

## 🎯 Future Enhancements

- [ ] User authentication system
- [ ] Real-time notifications
- [ ] Advanced filtering options
- [ ] Map integration for property locations
- [ ] Image upload and gallery
- [ ] PDF report generation
- [ ] Mobile app using React Native
- [ ] Dark mode theme

## 🐛 Known Issues

- Tailwind CSS configuration needs backend setup completion
- Image placeholders need real image integration
- Some interactive features need backend API

## 🤝 Development Guidelines

1. **Component Structure**: Keep components modular and reusable
2. **Styling**: Use Tailwind CSS classes consistently
3. **State Management**: Use React hooks for local state
4. **API Calls**: Implement proper error handling
5. **Responsive Design**: Test on multiple screen sizes
6. **Performance**: Optimize bundle size and loading times

## 📞 Support

For development support or questions, please refer to:
- React documentation: https://reactjs.org/
- Tailwind CSS docs: https://tailwindcss.com/
- React Router docs: https://reactrouter.com/

---

Built with ❤️ for efficient land management

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
