// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import Reports from './pages/Reports';
import AccountsManagements from './pages/AccountsManagements'; // ✅ New import
import Navbar from './components/Navbar';
import { AuthProvider } from './context/AuthContext';
import authService from './services/authService';
import './App.css';


function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = () => {
      const isValid = authService.isTokenValid();
      setLoading(false);
      return isValid;
    };
    
    checkAuth();
  }, []);

  const ProtectedRoute = ({ children, roles }) => {
    if (loading) return <div className="loading">Loading...</div>;

    const isAuthenticated = authService.isTokenValid();
    const userRole = authService.getUserRole();

    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }

    if (roles && !roles.includes(userRole)) {
      return <Navigate to="/dashboard" />;
    }

    return children;
  };

  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Navbar />
          <div className="content">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute roles={['admin', 'doctor']}>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />

              <Route 
                path="/admin" 
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminPanel />
                  </ProtectedRoute>
                } 
              />

              <Route 
                path="/reports" 
                element={
                  <ProtectedRoute roles={['admin', 'doctor', 'secretary']}>
                    <Reports />
                  </ProtectedRoute>
                } 
              />

              {/* ✅ New admin-only route */}
              <Route 
                path="/accounts-managements"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AccountsManagements />
                  </ProtectedRoute>
                }
              />

              <Route path="/" element={<Navigate to="/dashboard" />} />
              <Route path="*" element={<Navigate to="/dashboard" />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
