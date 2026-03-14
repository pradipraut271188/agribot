import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Setup API Key (Use secrets in production!)
# For local testing, replace "YOUR_API_KEY" with your actual key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the model (using the 2.5-flash you found)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="Agri-Smart Pro", layout="wide")
st.title("🌱 Agri-Smart Pro: AI Farmer Assistant")

# Create Tabs for different features
tab1, tab2 = st.tabs(["📸 Crop Analyzer", "💬 Agri-Chatbot"])

# --- TAB 1: Image Analysis ---
with tab1:
    st.header("Identify Crop & Get Nutrition")
    uploaded_file = st.file_uploader("Upload a crop photo...", type=["jpg", "jpeg", "png"], key="analyzer")

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", width=400)
        
        if st.button("Analyze Health & Nutrition"):
            prompt = """
            Identify this crop. Provide:
            1. Crop Name & Scientific Name.
            2. Health Status: Does it look healthy or deficient?
            3. Nutrition Plan: Suggest NPK requirements and 
               organic/chemical fertilizer options.
            """
            with st.spinner("Analyzing..."):
                response = model.generate_content([prompt, img])
                st.markdown("### 📋 Expert Report")
                st.write(response.text)

# --- TAB 2: General Chatbot ---
with tab2:
    st.header("Agri-Chat: Ask about Weather, Soil, or Crops")
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Agri-Expert. Ask me about crop seasons, weather advice, or soil health."}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant response
        with st.chat_message("assistant"):
            # We give the AI a "System Context" so it stays focused on Agriculture
            full_prompt = f"You are a professional agricultural expert. Answer this query based on farming best practices and current knowledge: {prompt}"
            
            with st.spinner("Thinking..."):
                # Note: For simple text, we don't need the image list
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response.text})
