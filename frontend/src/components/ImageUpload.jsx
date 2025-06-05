// frontend/src/components/ImageUpload.jsx
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import imageService from '../services/imageService';
import ReportModal from './ReportModal';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showReportModal, setShowReportModal] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);

  // NEW STATES for Save Analysis modal & workflow
  const [showSaveAnalysisModal, setShowSaveAnalysisModal] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);

  // Handle file upload
  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.tif', '.dicom', '.dcm']
    },
    maxFiles: 1
  });

  // Process image functions
  const processImage = async (action) => {
    if (!image) {
      setError("Please upload an image first");
      return;
    }

    setProcessing(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('image', image);
      
      let response;
      switch (action) {
        case 'enhance':
          response = await imageService.enhanceImage(formData);
          break;
        case 'colorize':
          response = await imageService.colorizeImage(formData);
          break;
        case 'detect_xray':
          response = await imageService.analyzeDentalXray(formData);
          break;
        case 'detect_missing_teeth':
          response = await imageService.detectMissingTeeth(formData);
          break;
        default:
          throw new Error('Invalid action');
      }
      
      if (response.image) {
        setResult({
          type: 'image',
          data: `data:image/jpeg;base64,${response.image}`,
          additionalData: response.results || null,
          action: action,
          timestamp: new Date().toISOString()
        });
      } else if (response.results) {
        setResult({
          type: 'detection',
          data: response.results,
          action: action,
          timestamp: new Date().toISOString()
        });
      }
    } catch (err) {
      setError(err.message || 'An error occurred during processing');
    } finally {
      setProcessing(false);
    }
  };

  // Render multi-label results
  const renderMultiLabelResults = (conditions) => {
    if (!conditions || conditions.length === 0) {
      return <p>No conditions detected.</p>;
    }

    return (
      <div className="conditions-list">
        <h4>Detected Conditions:</h4>
        <ul>
          {conditions.map((condition, index) => (
            <li key={index} className={`condition-item ${condition.condition.toLowerCase().replace(' ', '-')}`}>
              <span className="condition-name">{condition.condition}</span>
              <span className="condition-confidence">({condition.confidence}% confidence)</span>
              {condition.note && <span className="condition-note"> - {condition.note}</span>}
            </li>
          ))}
        </ul>
      </div>
    );
  };

  // Generate report function
  const generateReport = () => {
    if (!result || !result.additionalData) {
      setError("No analysis results available to generate report");
      return;
    }
    setShowReportModal(true);
  };

  // Handle report generation and email sending
  const handleReportGeneration = async (patientInfo) => {
    setGeneratingReport(true);
    try {
      const reportData = {
        patientInfo,
        analysisResults: result.additionalData,
        analysisType: result.action,
        timestamp: result.timestamp,
        imageData: result.data
      };

      await imageService.generateAndSendReport(reportData);

      alert(`Report generated and sent successfully to ${patientInfo.email}`);
      setShowReportModal(false);
    } catch (err) {
      setError(err.message || 'Error generating report');
    } finally {
      setGeneratingReport(false);
    }
  };

  // NEW: Handle Save Analysis Button Click
  const handleSaveAnalysisClick = () => {
    if (!image) {
      setError("Please upload an image first before saving analysis.");
      return;
    }
    setError(null);
    setShowSaveAnalysisModal(true);
  };

  // NEW: Handle Patient Search & Save Scan flow
  const handleSaveAnalysisSubmit = async (patientData) => {
    setSaveLoading(true);
    setError(null);

    try {
      // Step 1: Search patient by name + birthdate
      const existingPatient = await imageService.findPatientByNameAndBirthdate(patientData.name, patientData.birthdate);

      let patientId;

      if (existingPatient) {
        patientId = existingPatient.id;
      } else {
        // If not found, add new patient to DB
        const newPatient = await imageService.addPatient(patientData);
        patientId = newPatient.id;
      }

      // Step 2: Save scan to scans table
      // Assume current logged-in doctor/user id is available from authService or props
      const doctorId = imageService.getCurrentUserId();

      // Save the scan file - could be the same image file used earlier
      // Upload image and save DB record
      const formData = new FormData();
      formData.append('image', image);
      formData.append('patient_id', patientId);
      formData.append('doctor_id', doctorId);

      await imageService.saveScan(formData);

      alert("Analysis saved successfully.");
      setShowSaveAnalysisModal(false);
    } catch (err) {
      setError(err.message || "Failed to save analysis.");
    } finally {
      setSaveLoading(false);
    }
  };

  return (
    <div className="image-upload-container">
      <h2>Dental Image Analysis</h2>

      {/* Upload area */}
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Dental scan preview" className="image-preview" />
            <p>Drop a new image or click to change</p>
          </div>
        ) : (
          <div className="upload-message">
            <p>Drag & drop a dental X-ray or CT scan here, or click to select</p>
            <p className="upload-subtitle">Supported formats: JPG, PNG, TIF, DICOM</p>
          </div>
        )}
      </div>

      {/* Processing buttons */}
      <div className="process-buttons">
        <button 
          onClick={() => processImage('enhance')} 
          disabled={!image || processing}
          className="btn enhance"
        >
          Enhance
        </button>
        <button 
          onClick={() => processImage('colorize')} 
          disabled={!image || processing}
          className="btn colorize"
        >
          Colorize
        </button>
        <button 
          onClick={() => processImage('detect_xray')} 
          disabled={!image || processing}
          className="btn cavities"
        >
          Analyze X-ray
        </button>
        <button 
          onClick={() => processImage('detect_missing_teeth')} 
          disabled={!image || processing}
          className="btn missing"
        >
          Detect Missing Teeth
        </button>

        {/* NEW Save Analysis Button */}
        <button
          onClick={handleSaveAnalysisClick}
          disabled={!image || processing}
          className="btn save-analysis"
        >
          Save Analysis
        </button>
      </div>

      {/* Loading indicator */}
      {processing && (
        <div className="processing-indicator">
          <div className="spinner"></div>
          <p>Processing image...</p>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {/* Result display */}
      {result && !processing && (
        <div className="result-container">
          <h3>Analysis Results</h3>
          {result.type === 'image' ? (
            <div>
              <img src={result.data} alt="Processed result" className="result-image" />
              
              {result.additionalData && (
                <div className="additional-results">
                  {renderMultiLabelResults(result.additionalData)}
                  <div className="report-section">
                    <button 
                      onClick={generateReport}
                      className="btn generate-report"
                      disabled={generatingReport}
                    >
                      {generatingReport ? 'Generating Report...' : 'Generate Report'}
                    </button>
                    <p className="report-description">
                      Generate a professional dental report and send it to the patient via email
                    </p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="detection-results">
              <pre>{JSON.stringify(result.data, null, 2)}</pre>
              <div className="report-section">
                <button 
                  onClick={generateReport}
                  className="btn generate-report"
                  disabled={generatingReport}
                >
                  {generatingReport ? 'Generating Report...' : 'Generate Report'}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Report Modal */}
      {showReportModal && (
        <ReportModal
          onClose={() => setShowReportModal(false)}
          onSubmit={handleReportGeneration}
          loading={generatingReport}
        />
      )}

      {/* NEW: Save Analysis Modal (reuse ReportModal or create new modal) */}
      {showSaveAnalysisModal && (
        <ReportModal
          title="Save Analysis - Patient Info"
          onClose={() => setShowSaveAnalysisModal(false)}
          onSubmit={handleSaveAnalysisSubmit}
          loading={saveLoading}
          requirePatientFullData // you can create a prop to handle additional fields (gender, phone, email)
        />
      )}
    </div>
  );
};

export default ImageUpload;
