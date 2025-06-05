import React, { useState, useEffect } from 'react';
import authService from '../services/authService';  // import your authService

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterDate, setFilterDate] = useState('');
  const [selectedRole, setSelectedRole] = useState('all');

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const token = authService.getToken();

        if (!token) throw new Error('No auth token found');

        const response = await fetch('http://localhost:5000/api/admin/admin-data', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.message || 'Failed to fetch admin data');
        }

        const data = await response.json();
        setUsers(data.users || []);
        setFilteredUsers(data.users || []);
        setLogs(data.logs || []);
        setFilteredLogs(data.logs || []);
      } catch (error) {
        console.error('Error fetching admin data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAdminData();
  }, []);

  // Filter logs by selected date
  useEffect(() => {
    if (!filterDate) {
      setFilteredLogs(logs);
    } else {
      const selectedDate = new Date(filterDate).toDateString(); // "Sun Jun 01 2025"
      const filtered = logs.filter(log => {
        const logDateStr = log.action_time || log.timestamp;
        if (!logDateStr) return false;

        const logDate = new Date(logDateStr).toDateString();
        return logDate === selectedDate;
      });
      setFilteredLogs(filtered);
    }
  }, [filterDate, logs]);

  // Filter users by selected role
  useEffect(() => {
    if (selectedRole === 'all') {
      setFilteredUsers(users);
    } else {
      const filtered = users.filter(user => user.role === selectedRole);
      setFilteredUsers(filtered);
    }
  }, [selectedRole, users]);

  const getUsernameById = (userId) => {
    const user = users.find((u) => u.id === userId);
    return user ? user.username || user.name : 'Unknown';
  };

  return (
    <div className="admin-panel">
      <h2>Admin Panel</h2>

      {loading ? (
        <div className="processing-indicator">
          <div className="spinner"></div>
          <p>Loading admin data...</p>
        </div>
      ) : (
        <>
          {/* Users Section */}
          <div className="user-list">
            <div className="list-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>User Management (Approved Users)</h3>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                style={{ padding: '5px' }}
              >
                <option value="all">All</option>
                <option value="admin">Admin</option>
                <option value="doctor">Doctor</option>
                <option value="employee">Employee</option>
              </select>
            </div>
            <div className="list-body">
              {filteredUsers.length > 0 ? (
                filteredUsers.map((user) => (
                  <div key={user.id} className="list-item">
                    <div style={{ flex: 1 }}>{user.username || user.name}</div>
                    <div style={{ flex: 1 }}>{user.role}</div>
                    <div style={{ flex: 2 }}>Last login: {user.lastLogin || user.last_login}</div>
                  </div>
                ))
              ) : (
                <div style={{ padding: '10px' }}>No users for selected role.</div>
              )}
            </div>
          </div>

          {/* System Logs Section */}
          <div className="log-list">
            <div className="list-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>System Logs</h3>
              <input
                type="date"
                value={filterDate}
                onChange={(e) => setFilterDate(e.target.value)}
                style={{ padding: '5px' }}
              />
            </div>
            <div className="list-body">
              {filteredLogs.length > 0 ? (
                filteredLogs.map((log) => (
                  <div key={log.id} className="list-item">
                    <div style={{ flex: 1 }}>#{log.id}</div>
                    <div style={{ flex: 1 }}>{getUsernameById(log.user_id)}</div>
                    <div style={{ flex: 1 }}>{log.action_description || log.action}</div>
                    <div style={{ flex: 2 }}>{log.action_time || log.timestamp}</div>
                  </div>
                ))
              ) : (
                <div style={{ padding: '10px' }}>No logs for selected date.</div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AdminPanel;
