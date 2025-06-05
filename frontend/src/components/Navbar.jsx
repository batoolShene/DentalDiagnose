import React, { useContext } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import authService from '../services/authService';
import applogo from '../assets/applogo.png';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Don't render navbar on login page
  if (location.pathname === '/login') {
    return null;
  }

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="logo">
          <img src={applogo} alt="AIDentify Logo" style={{ height: '120px' }} />
        </div>

        {user && (
          <div className="nav-links">
            <Link 
              to="/dashboard" 
              className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
            >
              Dashboard
            </Link>

            <Link 
              to="/reports" 
              className={`nav-link ${location.pathname === '/reports' ? 'active' : ''}`}
            >
              Reports
            </Link>

            {/* ✅ Admin-only links */}
            {authService.isAdmin() && (
              <>
                <Link 
                  to="/admin" 
                  className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}
                >
                  Admin
                </Link>

                <Link 
                  to="/accounts-managements" 
                  className={`nav-link ${location.pathname === '/accounts-managements' ? 'active' : ''}`}
                >
                  Account Managements
                </Link>
              </>
            )}

            <button 
              onClick={handleLogout} 
              className="nav-link"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
