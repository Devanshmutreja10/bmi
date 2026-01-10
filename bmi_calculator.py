import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #5D5D5D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .bmi-value {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .bmi-category {
        font-size: 1.5rem;
        text-align: center;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton button {
        width: 100%;
        background-color: #2E86AB;
        color: white;
        font-weight: bold;
    }
    .info-box {
        background-color: #F0F8FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<p class="main-header">⚖️ BMI Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculate your Body Mass Index and understand what it means for your health</p>', unsafe_allow_html=True)

# BMI category information
bmi_categories = {
    "Underweight": {"range": (0, 18.4), "color": "#3498DB", "risk": "Low (but risk of other clinical problems increased)"},
    "Normal weight": {"range": (18.5, 24.9), "color": "#2ECC71", "risk": "Average"},
    "Overweight": {"range": (25, 29.9), "color": "#F39C12", "risk": "Increased"},
    "Obesity Class I": {"range": (30, 34.9), "color": "#E74C3C", "risk": "Moderate"},
    "Obesity Class II": {"range": (35, 39.9), "color": "#C0392B", "risk": "Severe"},
    "Obesity Class III": {"range": (40, 100), "color": "#922B21", "risk": "Very severe"}
}

# Sidebar for additional info
with st.sidebar:
    st.header("ℹ️ About BMI")
    st.write("Body Mass Index (BMI) is a person's weight in kilograms divided by the square of height in meters.")
    st.write("It is a simple screening method for weight categories that may lead to health problems.")
    
    st.header("📊 BMI Categories")
    for category, info in bmi_categories.items():
        st.markdown(f"**{category}**: {info['range'][0]} - {info['range'][1]}", 
                   help=f"Health risk: {info['risk']}")
    
    st.header("⚙️ Settings")
    unit_system = st.radio("Measurement System", ["Metric (kg, cm)", "Imperial (lbs, inches)"])
    
    st.markdown("---")
    st.caption("**Note:** BMI is a screening tool, not a diagnostic one. It does not account for muscle mass, bone density, overall body composition, and racial/sex differences.")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Details")
    
    if unit_system == "Metric (kg, cm)":
        # Metric system inputs
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
        height_m = height / 100  # Convert cm to meters
    else:
        # Imperial system inputs
        weight_lbs = st.number_input("Weight (lbs)", min_value=20.0, max_value=660.0, value=154.0, step=1.0)
        height_in = st.number_input("Height (inches)", min_value=20.0, max_value=100.0, value=67.0, step=0.5)
        # Convert to metric for BMI calculation
        weight = weight_lbs * 0.453592
        height_m = height_in * 0.0254

with col2:
    st.subheader("Your Results")
    
    if st.button("Calculate BMI"):
        # Calculate BMI
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 1)
        
        # Determine BMI category
        category = ""
        category_color = ""
        for cat, info in bmi_categories.items():
            if info["range"][0] <= bmi <= info["range"][1]:
                category = cat
                category_color = info["color"]
                risk = info["risk"]
                break
        
        # Display BMI value
        st.markdown(f'<div class="bmi-value" style="background-color:{category_color}20; color:{category_color};">{bmi}</div>', 
                   unsafe_allow_html=True)
        
        # Display BMI category
        st.markdown(f'<div class="bmi-category" style="background-color:{category_color}30; color:{category_color};">{category}</div>', 
                   unsafe_allow_html=True)
        
        # Health risk info
        st.markdown(f'<div class="info-box"><strong>Health Risk:</strong> {risk}</div>', unsafe_allow_html=True)
        
        # Display BMI chart
        st.subheader("BMI Chart")
        
        # Create a simple visualization
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Create gradient background for BMI categories
        y_pos = 0.5
        for cat, info in bmi_categories.items():
            ax.barh(y_pos, info["range"][1] - info["range"][0], 
                   left=info["range"][0], 
                   height=0.5, 
                   color=info["color"], 
                   alpha=0.7,
                   label=cat)
        
        # Add marker for user's BMI
        ax.axvline(x=bmi, color='black', linewidth=3, linestyle='--', alpha=0.8)
        ax.text(bmi+0.5, y_pos, f'Your BMI: {bmi}', va='center', fontweight='bold')
        
        ax.set_xlabel('BMI')
        ax.set_yticks([])
        ax.set_xlim(15, 45)
        ax.set_title('BMI Categories')
        
        # Add legend
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig)
        
        # Additional health information
        with st.expander("📋 Health Recommendations"):
            if category == "Underweight":
                st.write("""
                - Consult with a healthcare provider to rule out underlying conditions
                - Consider increasing calorie intake with nutrient-dense foods
                - Incorporate strength training to build muscle mass
                """)
            elif category == "Normal weight":
                st.write("""
                - Maintain your current healthy lifestyle
                - Continue regular physical activity (at least 150 minutes per week)
                - Eat a balanced diet with plenty of fruits and vegetables
                """)
            elif category == "Overweight":
                st.write("""
                - Aim for gradual weight loss (0.5-1 kg per week)
                - Increase physical activity to 150-300 minutes per week
                - Reduce portion sizes and limit high-calorie foods
                - Consider consulting a nutritionist
                """)
            else:  # Obesity categories
                st.write("""
                - Consult with a healthcare professional for guidance
                - Consider a medically supervised weight loss program
                - Aim for 300+ minutes of moderate-intensity activity per week
                - Focus on sustainable lifestyle changes rather than quick fixes
                - Behavioral therapy may help address eating habits
                """)
        
        # Save result to session state for tracking
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        st.session_state.history.append({
            "BMI": bmi,
            "Category": category,
            "Weight": weight,
            "Height": height_m
        })

# Display history if available
if 'history' in st.session_state and len(st.session_state.history) > 0:
    st.markdown("---")
    st.subheader("📈 Your BMI History")
    
    history_df = pd.DataFrame(st.session_state.history)
    
    # Show latest entries
    st.dataframe(history_df.tail(5), use_container_width=True)
    
    # Show trend if enough data
    if len(history_df) > 1:
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(range(len(history_df)), history_df["BMI"], marker='o', linewidth=2, color='#2E86AB')
        ax2.axhline(y=18.5, color='red', linestyle='--', alpha=0.5, label='Underweight threshold')
        ax2.axhline(y=25, color='orange', linestyle='--', alpha=0.5, label='Overweight threshold')
        ax2.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Obesity threshold')
        ax2.fill_between(range(len(history_df)), 18.5, 25, alpha=0.1, color='green', label='Healthy range')
        ax2.set_xlabel('Measurement')
        ax2.set_ylabel('BMI')
        ax2.set_title('Your BMI Trend')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>⚠️ <strong>Disclaimer:</strong> This BMI calculator is for informational purposes only. 
    It is not a substitute for professional medical advice, diagnosis, or treatment.</p>
    <p>BMI may not be accurate for athletes, pregnant women, children, and the elderly.</p>
    </div>
    """, 
    unsafe_allow_html=True
)