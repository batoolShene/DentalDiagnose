import React, { useState } from 'react';
import ImageUpload from '../components/ImageUpload';
import authService from '../services/authService';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const userRole = authService.getUserRole();

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>AIDentify - Dental Diagnostic System</h1>
        <p>Welcome, {authService.getCurrentUser()?.username}</p>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          Image Analysis
        </button>

        {(userRole === 'admin' || userRole === 'doctor') && (
          <button 
            className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            Recent Analyses
          </button>
        )}

        <button 
          className={`tab-button ${activeTab === 'help' ? 'active' : ''}`}
          onClick={() => setActiveTab('help')}
        >
          Help & Info
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'upload' && (
          <div className="dashboard-section">
            <ImageUpload />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="dashboard-section">
            <h2>Recent Analyses</h2>
            <p>Your recent dental image analyses will appear here.</p>
            {/* You would typically fetch and display recent analyses here */}
            <div className="history-placeholder">
              <p>Loading history...</p>
            </div>
          </div>
        )}

        {activeTab === 'help' && (
          <div className="dashboard-section help-section">
            <h2>Help & Information</h2>

            <div className="help-card">
              <h3>Image Upload</h3>
              <p>
                Upload dental X-rays or CT scans in JPG, PNG, TIF, or DICOM format.
                Maximum file size is 16MB.
              </p>
            </div>

            <div className="help-card">
              <h3>Image Enhancement</h3>
              <p>
                The enhancement feature improves contrast and clarity in dental images,
                making it easier to identify structures and potential issues.
              </p>
            </div>

            <div className="help-card">
              <h3>Image Colorization</h3>
              <p>
                Colorization applies a color map to grayscale images, which can help
                highlight different densities and structures within the dental scan.
              </p>
            </div>

            <div className="help-card">
              <h3>Cavity Detection</h3>
              <p>
                Our AI model analyzes X-rays to identify potential cavities,
                highlighting their locations and providing confidence scores.
              </p>
            </div>

            <div className="help-card">
              <h3>Missing Teeth Detection</h3>
              <p>
                This feature identifies missing teeth in panoramic X-rays,
                marking the gaps and providing dental position information.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
