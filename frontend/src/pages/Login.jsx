// src/pages/Login.jsx
import React, { useState, useContext } from 'react';
import { useNavigate, Navigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import authService from '../services/authService';
import applogo from '../assets/applogo.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, user } = useContext(AuthContext);
  const navigate = useNavigate();

  // If already logged in, redirect to dashboard
  if (user && authService.isTokenValid()) {
    return <Navigate to="/dashboard" />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!email || !password) {
      setError('Please enter both email and password');
      setLoading(false);
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      setLoading(false);
      return;
    }

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = (role) => {
    switch (role) {
      case 'admin':
        setEmail('admin@aidentify.com');
        setPassword('admin123');
        break;
      case 'doctor':
        setEmail('doctor@aidentify.com');
        setPassword('doctor123');
        break;
      case 'employee':
        setEmail('employee@aidentify.com');
        setPassword('employee123');
        break;
      default:
        break;
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <img src={applogo} alt="AIDentify Logo" style={{ height: '120px' }} />
          <p><b>Login to your account</b></p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email address"
              disabled={loading}
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={loading}
              autoComplete="current-password"
            />
          </div>

          <div className="demo-credentials">
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '10px' }}>
              Demo credentials (click to fill):
            </p>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '15px' }}>
              <button
                type="button"
                onClick={() => fillDemoCredentials('admin')}
                className="demo-btn"
                disabled={loading}
                style={{
                  padding: '5px 10px',
                  fontSize: '0.8rem',
                  backgroundColor: '#f0f0f0',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Admin
              </button>
              <button
                type="button"
                onClick={() => fillDemoCredentials('doctor')}
                className="demo-btn"
                disabled={loading}
                style={{
                  padding: '5px 10px',
                  fontSize: '0.8rem',
                  backgroundColor: '#f0f0f0',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Doctor
              </button>
              <button
                type="button"
                onClick={() => fillDemoCredentials('employee')}
                className="demo-btn"
                disabled={loading}
                style={{
                  padding: '5px 10px',
                  fontSize: '0.8rem',
                  backgroundColor: '#f0f0f0',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Employee
              </button>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="login-btn"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Log In'}
          </button>

          {/* Register link */}
          <div style={{ marginTop: '15px', textAlign: 'center' }}>
            <span style={{ fontSize: '0.9rem' }}>
              Don’t have an account? <Link to="/register">Register here</Link>
            </span>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
