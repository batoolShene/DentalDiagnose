import React, { useState, useEffect } from 'react';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/reports'); // Your backend API URL
        if (!response.ok) {
          throw new Error(`Error fetching reports: ${response.statusText}`);
        }
        const data = await response.json();
        setReports(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchReports();
  }, []);
  
  if (loading) {
    return (
      <div className="processing-indicator">
        <div className="spinner"></div>
        <p>Loading reports...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  return (
    <div className="reports-container">
      <h2>Patient Reports</h2>
      
      <div className="report-filters">
        <div className="filter-group">
          <label className="filter-label">Date Range:</label>
          <select className="filter-select">
            <option>All Time</option>
            <option>Last 7 Days</option>
            <option>Last 30 Days</option>
            <option>Custom...</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label className="filter-label">Report Type:</label>
          <select className="filter-select">
            <option>All Types</option>
            <option>Cavity Detection</option>
            <option>Missing Teeth</option>
            <option>Enhancement</option>
            <option>Colorization</option>
          </select>
        </div>
      </div>
      
      <div className="report-list">
        <div className="report-header">
          <div>ID</div>
          <div>Patient</div>
          <div>Date</div>
          <div>Actions</div>
        </div>
        
        {reports.map(report => (
          <div key={report.id} className="report-item">
            <div>{report.id}</div>
            <div>{report.patientName}</div>
            <div>{report.date}</div>
            <div>
              <button className="view-report-btn">View</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Reports;
