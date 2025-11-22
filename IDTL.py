import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="app_icon.png.png", layout="centered")

# Connect to Google AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Missing API Key! Add it to Streamlit Secrets.")

# --- 2. MAIN MENU (Radio Buttons on Screen) ---
st.write("### Select Option")
app_mode = st.radio(" ", [
    "💬 Agriculture Chatbot",
    "🟢 Plant Disease Detector", 
    "🌾 Seed Quality Checker", 
    "☁ Weather Predictor"
])
st.markdown("---")

# --- OPTION 1: GENERAL AGRICULTURE CHATBOT ---
if app_mode == "💬 Agriculture Chatbot":
    st.header("💬 Ask anything about agriculture")
    
    # Text Input for General Questions
    user_question = st.text_input("Your Question:", placeholder="e.g., How much water for cotton? Best fertilizer for wheat?")
    
    if st.button("Ask Agri-AI"):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # General Agriculture Prompt
                    prompt = f"You are an expert agriculture consultant. Answer this question for a farmer in simple English: {user_question}"
                    response = model.generate_content(prompt)
                    st.success("Agri-GPT Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPTION 2: PLANT DISEASE DETECTOR ---
elif app_mode == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.write("Upload a photo of a sick leaf.")
    
    uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf", use_column_width=True)
        
        if st.button("Identify Disease"):
            with st.spinner("Analyzing..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Analyze this plant leaf. Name the plant. Identify disease. Suggest cure."
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPTION 3: SEED QUALITY CHECKER ---
elif app_mode == "🌾 Seed Quality Checker":
    st.header("🌾 Seed Quality Checker")
    st.write("Upload a photo of seeds.")
    
    uploaded_seed = st.file_uploader("Choose seed image...", type=["jpg", "png"])
    
    if uploaded_seed:
        image = Image.open(uploaded_seed)
        st.image(image, caption="Uploaded Seeds", use_column_width=True)
        
        if st.button("Check Quality"):
            with st.spinner("Counting..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Count these seeds. Check for breakage/rot. Rate quality."
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPTION 4: WEATHER PREDICTOR ---
elif app_mode == "☁ Weather Predictor":
    st.header("☁ Weather Predictor")
    
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Season", ["Summer", "Monsoon", "Winter"])
    with col2:
        sky = st.selectbox("Sky", ["Sunny", "Cloudy", "Rainy"])
        
    if st.button("Get Forecast"):
        if sky == "Rainy":
            st.warning("⚠ Heavy Rain Alert. Stop watering.")
        elif sky == "Sunny" and season == "Summer":
            st.error("☀ High Heat. Water frequently.")
        else:
            st.success("✅ Weather is good for farming.")

