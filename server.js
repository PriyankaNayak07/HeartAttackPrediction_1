const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

// Create the Express app
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// Heart disease prediction model
const model = require('./models/heartDiseaseModel');

// Diet recommendations
const dietRecommendations = require('./models/dietRecommendations');

// API endpoint for prediction
app.post('/api/predict', (req, res) => {
  try {
    const inputData = {
      age: parseInt(req.body.age),
      sex: req.body.sex === 'Male' ? 1 : 0,
      blood_pressure: parseInt(req.body.blood_pressure),
      cholesterol: parseInt(req.body.cholesterol),
      chest_pain_type: parseInt(req.body.chest_pain_type)
    };
    
    // Make prediction
    const hasHeartDisease = model.predictHeartDisease(inputData);
    
    // Get diet recommendations
    const recommendations = dietRecommendations.getDietRecommendations(
      hasHeartDisease, 
      inputData
    );
    
    // Send response
    res.json({
      name: req.body.name,
      has_heart_disease: hasHeartDisease,
      result_message: hasHeartDisease ? 
        "You may be at risk for heart disease." : 
        "You are likely not at risk for heart disease.",
      diet_recommendations: recommendations
    });
  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({ error: 'Failed to process prediction' });
  }
});

// Generate PDF report
app.post('/api/generate-report', (req, res) => {
  try {
    // In a real implementation, this would generate a PDF
    // For now we'll just return a success message
    res.json({ 
      success: true, 
      message: 'Report would be generated here in a full implementation'
    });
  } catch (error) {
    console.error('Report generation error:', error);
    res.status(500).json({ error: 'Failed to generate report' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});