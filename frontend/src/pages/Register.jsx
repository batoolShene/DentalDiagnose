// src/pages/Register.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import applogo from '../assets/applogo.png';

const Register = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    country: '',
    stateCity: '',
    clinicName: '',
    clinicPhone: '',
    service: '',
  });

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (response.ok) {
      alert('Registration request submitted!');
      navigate('/');
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (err) {
    alert('Something went wrong. Please try again.');
    console.error(err);
  }
};


  return (
    <div className="register-page">
      <div className="login-container">
        <div className="login-header">
          <img src={applogo} alt="AIDentify Logo" style={{ height: '120px' }} />
          <p><b>Contact For Register</b></p>
          <p style={{ fontSize: '0.9rem', color: '#555' }}>
            Please Fill Out Your Details &<br />We will contact you soonly
          </p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '250px' }}>
              <label>Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="Hind Sumary"
                required
              />
              <label>Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="1234@1234.com"
                required
              />
              <label>Phone Number</label>
              <input
                type="text"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="0123456789"
                required
              />
              <label>Country</label>
              <select
                name="country"
                value={formData.country}
                onChange={handleChange}
                required
              >
                <option value="">Select Country</option>
                <option value="Palestine">Palestine</option>
                <option value="Jordan">Jordan</option>
                <option value="Egypt">Egypt</option>
              </select>
            </div>

            <div style={{ flex: 1, minWidth: '250px' }}>
              <label>State/City</label>
              <input
                type="text"
                name="stateCity"
                value={formData.stateCity}
                onChange={handleChange}
                placeholder="Jerusalem"
                required
              />
              <label>Clinic’s Name</label>
              <input
                type="text"
                name="clinicName"
                value={formData.clinicName}
                onChange={handleChange}
                placeholder="clinic_name"
                required
              />
              <label>Clinic’s Phone Number</label>
              <input
                type="text"
                name="clinicPhone"
                value={formData.clinicPhone}
                onChange={handleChange}
                placeholder="0123456789"
                required
              />
              <label>Service needed</label>
              <select
                name="service"
                value={formData.service}
                onChange={handleChange}
                required
              >
                <option value="">Services</option>
                <option value="In-Person Meeting">In-Person Meeting</option>
                <option value="Online Meeting">Online Meeting</option>
              </select>
            </div>
          </div>

          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <button 
              type="submit" 
              className="login-btn"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
