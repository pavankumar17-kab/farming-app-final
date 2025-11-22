import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONNECT TO GOOGLE AI
# This looks for the key you just saved in Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing Google API Key. Please add it to Streamlit Secrets.")

# 2. PAGE SETUP
st.set_page_config(page_title="Farmer Assistant", page_icon="🌿")
st.title("🌿 AI Farmer Assistant")
st.write("Upload a photo of a plant. The AI will identify diseases and suggest medicines.")

# 3. UPLOAD IMAGE
uploaded_file = st.file_uploader("Choose a plant image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Photo", use_column_width=True)
    
    # 4. BUTTON TO ANALYZE
    if st.button("Identify Disease"):
        with st.spinner("Asking the AI Expert..."):
            try:
                # Connect to Gemini Model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # The Question we ask the AI
                my_question = (
                    "You are an expert farmer. Look at this plant. "
                    "1. What is the name of this plant? "
                    "2. Is it healthy or sick? "
                    "3. If sick, what is the disease name? "
                    "4. What medicine or fertilizer should I use? "
                    "Answer in simple English."
                )
                
                # Get the Answer
                response = model.generate_content([my_question, image])
                st.success("Analysis Complete!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
