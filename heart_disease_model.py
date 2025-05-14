import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Create a simple but effective heart disease prediction model
def create_model():
    # Using simplified weights based on medical literature
    # This is not a production-grade model, but serves as a demonstration
    # In a real application, you would use a properly trained ML model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Create some synthetic data to train the model
    # This would be replaced with real training data in a production environment
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic features (age, sex, bp, cholesterol, chest pain)
    ages = np.random.randint(20, 80, n_samples)
    sex = np.random.randint(0, 2, n_samples)  # 0 female, 1 male
    blood_pressure = np.random.randint(90, 180, n_samples)
    cholesterol = np.random.randint(150, 350, n_samples)
    chest_pain = np.random.randint(0, 4, n_samples)
    
    # Create target based on medical heuristics
    target = (
        (ages > 50) * 1 +
        (sex == 1) * 1 +
        (blood_pressure > 140) * 2 +
        (cholesterol > 240) * 2 +
        (chest_pain > 1) * 3
    )
    target = (target >= 5).astype(int)  # Threshold for diagnosis
    
    # Create training data
    X = pd.DataFrame({
        'age': ages,
        'sex': sex,
        'blood_pressure': blood_pressure,
        'cholesterol': cholesterol,
        'chest_pain_type': chest_pain
    })
    
    # Train model
    model.fit(X, target)
    
    return model

# Global model instance
MODEL = create_model()

def predict_heart_disease(input_data):
    """
    Predict heart disease risk based on input data.
    
    Args:
        input_data (dict): Dictionary containing user health information
        
    Returns:
        bool: True if heart disease is predicted, False otherwise
    """
    # Convert input to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Make prediction
    prediction = MODEL.predict(input_df)[0]
    
    # Return prediction as boolean
    return bool(prediction)
