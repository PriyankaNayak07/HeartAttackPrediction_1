import streamlit as st
import pandas as pd
import base64
from heart_disease_model import predict_heart_disease
from diet_recommendations import get_diet_recommendations
from report_generator import generate_report

# Set page config
st.set_page_config(
    page_title="Early Detection for Better Heart Health",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Add styling to match the provided design
st.markdown("""
<style>
    .main {
        background-color: #f1f5fa !important;
        padding: 0;
    }
    body {
        background-color: #f1f5fa;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .reportBlock {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
        border-bottom: 1px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 0;
        color: #666;
        padding-top: 10px;
        padding-bottom: 10px;
        margin-right: 30px;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom: 2px solid #FF4B4B;
        color: #FF4B4B;
        font-weight: 500;
    }
    div[role="tablist"] button[role="tab"] {
        position: relative;
    }
    div[role="tablist"] button[aria-selected="true"]::after {
        content: "";
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: #FF4B4B;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #f0f5f9;
        padding-top: 2rem;
    }
    .assessment-notice {
        background-color: #e8f4fd;
        padding: 15px 20px;
        border-radius: 5px;
        margin: 20px 0;
        text-align: left;
        color: #333;
        font-size: 15px;
    }
    .highlight-container {
        text-align: center;
        margin: 20px 0;
    }
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;
        max-width: 100%;
        height: auto;
    }
    h1, h2, h3 {
        color: #333;
        font-weight: 500;
    }
    .diet-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #333;
    }
    .diet-subtitle {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    /* Style form inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    /* Make the form card like in the screenshot */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    /* Make header match screenshot */
    header[data-testid="stHeader"] {
        background-color: #f1f5fa;
        border-bottom: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# App title and main image
st.markdown("<h1 style='text-align: center; font-weight: 500; font-size: 32px; margin-bottom: 20px;'>Early Detection for Better Heart Health</h1>", unsafe_allow_html=True)

# Center the heart image
st.markdown("""
<div class="highlight-container">
    <img src="https://pixabay.com/get/g7bd51d4f06a9c7c9f1d866d0a96d57f4f2a2f5d583adbd9cef4aa76a74f08903afe8f5f5b7a5a6e61ee6bdb2764b76c5_1280.jpg" class="centered-image" style="width: 300px;">
</div>
""", unsafe_allow_html=True)

# Create tabs similar to the design
tab1, tab2 = st.tabs(["Health Assessment", "Diet Recommendations"])

with tab1:
    # Create a form for user input
    with st.form("heart_disease_prediction_form"):
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Enter Your Health Information</h3>", unsafe_allow_html=True)
        
        # User input fields
        name = st.text_input("Name", placeholder="Enter your name")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
            sex = st.selectbox("Sex", options=["Male", "Female"])
        
        with col2:
            blood_pressure = st.number_input("Blood Pressure (systolic mm Hg)", min_value=50, max_value=300, value=120, step=1)
            cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200, step=1)
        
        # Chest pain type with descriptions
        chest_pain_options = {
            "0": "No Pain (Asymptomatic)",
            "1": "Mild Pain (Atypical Angina)",
            "2": "Moderate Pain (Non-anginal)",
            "3": "Severe Pain (Typical Angina)"
        }
        
        chest_pain_type = st.selectbox(
            "Chest Pain Type", 
            options=list(chest_pain_options.keys()),
            format_func=lambda x: chest_pain_options[x]
        )
        
        # Submit button
        submit_button = st.form_submit_button("Predict Heart Disease Risk")

    # Process form submission
    if submit_button:
        # Validate inputs
        if not name:
            st.error("Please enter your name.")
        else:
            # Convert sex to binary (1 for Male, 0 for Female)
            sex_binary = 1 if sex == "Male" else 0
            
            # Convert inputs to appropriate format
            input_data = {
                'age': age,
                'sex': sex_binary,
                'blood_pressure': blood_pressure,
                'cholesterol': cholesterol,
                'chest_pain_type': int(chest_pain_type)
            }
            
            # Show loading spinner
            with st.spinner("Analyzing your health data..."):
                # Make prediction
                has_heart_disease = predict_heart_disease(input_data)
                
                # Get diet recommendations
                diet_recommendations = get_diet_recommendations(has_heart_disease, input_data)
                
                # Determine result color and message
                if has_heart_disease:
                    result_color = "red"
                    result_message = "You may be at risk for heart disease."
                else:
                    result_color = "green"
                    result_message = "You are likely not at risk for heart disease."
            
            # Display result with appropriate styling
            st.markdown(f"""
            <div style='background-color: {result_color}; padding: 20px; border-radius: 10px; color: white; margin: 20px 0px;'>
                <h2 style='text-align: center;'>Results for {name}</h2>
                <h3 style='text-align: center;'>{result_message}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display diet recommendations in a styled container
            st.markdown("""
            <div class='reportBlock'>
                <h3 style='text-align: center; color: #ff4b4b;'>Personalized Diet Recommendations</h3>
            """, unsafe_allow_html=True)
            
            for category, items in diet_recommendations.items():
                st.markdown(f"<h4 style='color: #2c3e50;'>{category}</h4>", unsafe_allow_html=True)
                for item in items:
                    st.markdown(f"- {item}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Generate PDF report
            try:
                pdf_data = generate_report(
                    name=name,
                    age=age,
                    sex=sex,
                    blood_pressure=blood_pressure,
                    cholesterol=cholesterol,
                    chest_pain_type=chest_pain_options[chest_pain_type],
                    has_heart_disease=has_heart_disease,
                    diet_recommendations=diet_recommendations
                )
                
                # Create styled download button for PDF report
                b64_pdf = base64.b64encode(pdf_data).decode()
                href = f"""
                <div style='text-align: center; margin: 30px 0px;'>
                    <a href="data:application/pdf;base64,{b64_pdf}" download="heart_health_report.pdf" 
                    style="display: inline-block; padding: 12px 24px; background-color: #4CAF50; 
                    color: white; text-align: center; text-decoration: none; font-size: 18px; 
                    border-radius: 5px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    Download Heart Health Report
                    </a>
                </div>
                """
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Could not generate report: {str(e)}")

with tab2:
    # Diet recommendations tab similar to the screenshot
    
    # Assessment notice
    st.markdown("""
    <div class="assessment-notice">
        Please complete the Health Assessment to receive personalized diet recommendations.
    </div>
    """, unsafe_allow_html=True)
    
    # Diet Recommendations title and name (similar to the screenshot)
    st.markdown("""
    <h2 style='text-align: left; margin-top: 20px; margin-bottom: 10px;'>Diet Recommendations for You</h2>
    """, unsafe_allow_html=True)
    
    # Show the heart-healthy foods image
    st.markdown("""
    <div class="highlight-container">
        <img src="https://pixabay.com/get/g0ef05bddbfe95d14aa44b3f50af7b8b1d5e1cf2c3b1d4ebfc7c61eb5b14d1ae7ad5d2c0fd2ed96a2c80c5d59fa2f4cb1fc0f23b0c9cb6cd39c74ba5acdebb1a5_1280.jpg" class="centered-image" style="width: 400px; border-radius: 10px; margin: 20px auto;">
        <p style="text-align: center; color: #666; font-style: italic;">Heart-Healthy Foods</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='diet-title'>Dietary Guidelines</h3>", unsafe_allow_html=True)
    st.markdown("<p class='diet-subtitle'>A heart-healthy diet focuses on foods that can help lower cholesterol, manage blood pressure, maintain healthy weight, and reduce risk of heart disease.</p>", unsafe_allow_html=True)
    
    # Diet planning content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #185a9d;'>Foods to Include</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Fruits and Vegetables**: Aim for 5+ servings daily
        - **Whole Grains**: Brown rice, oats, whole wheat bread
        - **Lean Proteins**: Fish, skinless poultry, legumes
        - **Healthy Fats**: Olive oil, avocados, nuts, seeds
        - **Low-fat Dairy**: Milk, yogurt, cheese in moderation
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #185a9d;'>Heart-Healthy Eating Patterns</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Mediterranean Diet**: Rich in olive oil, nuts, fish, fruits and vegetables
        - **DASH Diet**: Designed to lower blood pressure
        - **Plant-Based Diet**: Focus on plants with limited animal products
        - **Low Sodium Diet**: Reducing salt intake below 2,300mg daily
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #ff4b4b;'>Foods to Limit</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Processed Foods**: Packaged snacks, frozen meals
        - **Added Sugars**: Sodas, candies, desserts
        - **Saturated Fats**: Fatty meats, full-fat dairy
        - **Trans Fats**: Fried foods, some baked goods
        - **High-Sodium Foods**: Canned soups, fast food
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #185a9d;'>Weekly Meal Planning</h3>", unsafe_allow_html=True)
        st.markdown("""
        - Plan for 2 servings of fatty fish weekly (salmon, mackerel)
        - Include a meatless day focusing on legumes
        - Prepare meals at home to control ingredients
        - Use herbs and spices instead of salt for flavor
        - Stay hydrated with water instead of sugary drinks
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #43cea2;'>Heart-Healthy Portion Guide</h3>", unsafe_allow_html=True)
    
    portions_col1, portions_col2, portions_col3 = st.columns(3)
    
    with portions_col1:
        st.markdown("""
        **Proteins**
        - Size of a deck of cards (3oz)
        - Fish, poultry, lean meat
        - 1/2 cup of beans or lentils
        """)
    
    with portions_col2:
        st.markdown("""
        **Grains & Starches**
        - 1/2 cup cooked rice or pasta
        - 1 slice of bread
        - 1 small potato
        """)
    
    with portions_col3:
        st.markdown("""
        **Fruits & Vegetables**
        - 1 cup raw leafy vegetables
        - 1/2 cup chopped vegetables
        - 1 medium fruit
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Risk factors section is now incorporated into the diet tab
    st.markdown("<h2 style='text-align: center; color: #ff4b4b; margin-top: 30px;'>Understanding Heart Disease Risk Factors</h2>", unsafe_allow_html=True)
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #185a9d;'>Major Risk Factors</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Age**: Risk increases with age
        - **Sex**: Men have higher risk than pre-menopausal women
        - **Family History**: Genetic factors play a role
        - **High Blood Pressure**: Damages arterial walls
        - **High Cholesterol**: Leads to plaque buildup
        - **Smoking**: Damages blood vessels
        - **Diabetes**: Increases risk significantly
        - **Obesity**: Strains the heart
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with risk_col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #185a9d;'>Protective Factors</h3>", unsafe_allow_html=True)
        st.markdown("""
        - **Regular Exercise**: At least 150 minutes per week
        - **Healthy Diet**: Rich in fruits, vegetables, whole grains
        - **Maintaining Healthy Weight**: BMI between 18.5-24.9
        - **No Smoking**: Quitting reduces risk substantially
        - **Limited Alcohol**: Moderate consumption only
        - **Stress Management**: Regular relaxation practices
        - **Regular Check-ups**: Monitoring health metrics
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>Warning Signs of Heart Disease</h3>", unsafe_allow_html=True)
    
    warning_col1, warning_col2, warning_col3 = st.columns(3)
    
    with warning_col1:
        st.markdown("""
        - Chest pain or discomfort
        - Shortness of breath
        - Pain in the arms, back, neck, or jaw
        """)
    
    with warning_col2:
        st.markdown("""
        - Feeling weak, lightheaded, or faint
        - Heart palpitations
        - Swelling in the legs, ankles, or feet
        """)
    
    with warning_col3:
        st.markdown("""
        - Rapid or irregular heartbeat
        - Extreme fatigue
        - Nausea or vomiting
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-top: 20px;'>
        <p style='text-align: center;'>Regular checkups with healthcare professionals are essential for maintaining heart health.</p>
    </div>
    """, unsafe_allow_html=True)