import streamlit as st
import google.generativeai as genai
from PIL import Image

# Setup
import os
# Get the key from the environment/system settings
api_key = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=api_key)

st.title("🌱 Agri-Bot 2026: Crop & Nutrition")

uploaded_file = st.file_uploader("Upload crop photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Target Crop", use_container_width=True)
    
    if st.button("Identify and Get Nutrition Plan"):
        # Use the specific model you found in your ListModels call
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = """
        Identify the crop in this image. 
        Provide:
        1. Crop Name
        2. Current health status (if visible)
        3. Specific Nitrogen (N), Phosphorus (P), and Potassium (K) requirements for this stage.
        4. One organic and one inorganic fertilizer recommendation.
        """
        
        try:
            with st.spinner("Analyzing with Gemini 2.5..."):
                response = model.generate_content([prompt, img])
                st.markdown("### 📋 Analysis Report")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
