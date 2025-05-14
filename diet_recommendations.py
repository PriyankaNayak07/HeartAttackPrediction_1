def get_diet_recommendations(has_heart_disease, input_data):
    """
    Get personalized diet recommendations based on heart disease prediction and user data.
    
    Args:
        has_heart_disease (bool): Whether the user has heart disease
        input_data (dict): Dictionary containing user health information
        
    Returns:
        dict: Dictionary of diet recommendations by category
    """
    age = input_data['age']
    cholesterol = input_data['cholesterol']
    blood_pressure = input_data['blood_pressure']
    
    # Basic recommendations for everyone
    recommendations = {
        "Recommended Foods": [
            "Fresh fruits and vegetables",
            "Whole grains (brown rice, oats, whole wheat)",
            "Lean proteins (chicken, fish, legumes)",
            "Low-fat dairy products",
            "Nuts and seeds (in moderation)"
        ],
        "Hydration": [
            "Drink 8-10 glasses of water daily",
            "Herbal teas without added sugar",
            "Fresh vegetable juices"
        ]
    }
    
    # Customized recommendations based on heart disease status
    if has_heart_disease:
        recommendations["Foods to Limit"] = [
            "Salt and high-sodium foods (processed foods, canned soups)",
            "Saturated fats (fatty meats, full-fat dairy)",
            "Trans fats (fried foods, baked goods)",
            "Added sugars (desserts, sodas, candies)",
            "Alcohol (limit to occasional consumption)"
        ]
        
        recommendations["Heart-Healthy Options"] = [
            "Omega-3 rich fish (salmon, mackerel, sardines)",
            "Heart-healthy oils (olive oil, avocado oil)",
            "Berries (strawberries, blueberries, raspberries)",
            "Leafy greens (spinach, kale, collard greens)",
            "Garlic and onions",
            "Dark chocolate (70% or higher cocoa content, in moderation)"
        ]
    else:
        recommendations["Maintenance Tips"] = [
            "Maintain a balanced diet with diverse food groups",
            "Practice portion control",
            "Cook at home more often to control ingredients",
            "Read nutrition labels when shopping",
            "Limit processed and ultra-processed foods"
        ]
    
    # Age-specific recommendations
    if age > 50:
        recommendations["Age-Specific Suggestions"] = [
            "Increase calcium and vitamin D intake for bone health",
            "Consider B12 supplementation (consult with healthcare provider)",
            "Reduce sodium intake further to support blood pressure control",
            "Prioritize fiber-rich foods for digestive health"
        ]
    
    # Cholesterol-specific recommendations
    if cholesterol > 200:
        if "Cholesterol Management" not in recommendations:
            recommendations["Cholesterol Management"] = []
        
        recommendations["Cholesterol Management"].extend([
            "Increase soluble fiber intake (oats, beans, fruits)",
            "Include plant sterols/stanols (fortified foods)",
            "Consume fatty fish twice a week",
            "Add ground flaxseeds to meals",
            "Consider reducing animal protein consumption"
        ])
    
    # Blood pressure specific recommendations
    if blood_pressure > 130:
        if "Blood Pressure Control" not in recommendations:
            recommendations["Blood Pressure Control"] = []
            
        recommendations["Blood Pressure Control"].extend([
            "Follow the DASH diet approach",
            "Limit sodium to less than 1,500mg daily",
            "Increase potassium-rich foods (bananas, potatoes, beans)",
            "Include magnesium-rich foods (nuts, seeds, whole grains)",
            "Consider regular consumption of beetroot juice or beets"
        ])
    
    return recommendations
