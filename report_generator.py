from fpdf import FPDF
import datetime
import io

def generate_report(name, age, sex, blood_pressure, cholesterol, chest_pain_type, has_heart_disease, diet_recommendations):
    """
    Generate a PDF report with user data and heart disease prediction.
    
    Args:
        name (str): User's name
        age (int): User's age
        sex (str): User's sex
        blood_pressure (int): User's blood pressure
        cholesterol (int): User's cholesterol level
        chest_pain_type (str): User's chest pain type
        has_heart_disease (bool): Whether user has heart disease
        diet_recommendations (dict): Diet recommendations
        
    Returns:
        bytes: PDF report as bytes
    """
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(190, 10, "Heart Health Report", 0, 1, "C")
    pdf.cell(190, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
    pdf.ln(10)
    
    # Patient information
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Patient Information", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.cell(50, 10, "Name:", 0, 0, "L")
    pdf.cell(140, 10, name, 0, 1, "L")
    pdf.cell(50, 10, "Age:", 0, 0, "L")
    pdf.cell(140, 10, str(age), 0, 1, "L")
    pdf.cell(50, 10, "Sex:", 0, 0, "L")
    pdf.cell(140, 10, sex, 0, 1, "L")
    pdf.ln(5)
    
    # Health metrics
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Health Metrics", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.cell(50, 10, "Blood Pressure:", 0, 0, "L")
    pdf.cell(140, 10, f"{blood_pressure} mm Hg", 0, 1, "L")
    pdf.cell(50, 10, "Cholesterol:", 0, 0, "L")
    pdf.cell(140, 10, f"{cholesterol} mg/dl", 0, 1, "L")
    pdf.cell(50, 10, "Chest Pain Type:", 0, 0, "L")
    pdf.cell(140, 10, chest_pain_type, 0, 1, "L")
    pdf.ln(5)
    
    # Assessment result
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Heart Health Assessment", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    
    if has_heart_disease:
        pdf.set_text_color(255, 0, 0)  # Red for positive result
        pdf.cell(190, 10, "Result: You may be at risk for heart disease", 0, 1, "L")
    else:
        pdf.set_text_color(0, 128, 0)  # Green for negative result
        pdf.cell(190, 10, "Result: You are likely not at risk for heart disease", 0, 1, "L")
    
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(5)
    
    # Diet recommendations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Personalized Diet Recommendations", 0, 1, "L")
    pdf.ln(2)
    
    for category, items in diet_recommendations.items():
        pdf.set_font("Arial", "B", 11)
        pdf.cell(190, 10, category, 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        
        for item in items:
            # Use a simple dash for bullet points to avoid encoding issues
            pdf.cell(10, 7, "-", 0, 0, "R")
            # Handle possible non-ASCII characters
            safe_item = ''.join(c if ord(c) < 128 else '-' for c in item)
            pdf.multi_cell(180, 7, safe_item, 0, "L")
        
        pdf.ln(3)
    
    # Footer with disclaimer
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    disclaimer = "This report is for informational purposes only and should not replace professional medical advice. Please consult with a healthcare professional for proper diagnosis and treatment."
    pdf.multi_cell(190, 5, disclaimer, 0, "L")
    
    # Create a bytes buffer to capture the PDF content
    buffer = io.BytesIO()
    # Direct PDF to the buffer (not a file)
    buffer.write(pdf.output(dest='S').encode('latin-1', errors='replace'))
    buffer.seek(0)
    # Return the PDF as bytes
    return buffer.getvalue()
