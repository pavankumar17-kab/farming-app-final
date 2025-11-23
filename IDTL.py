import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="🌿", layout="centered")

# Connect to Google AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. MAIN MENU (FOUR SEPARATE TOOLS) ---
st.header("🚜 Agri-Dashboard")
app_mode = st.radio("Select Tool:", [
    "💬 Agri Chatbot (Text Only)",  # 1. New pure text option
    "🟢 Plant Disease Detector", 
    "🌾 Seed Quality Checker", 
    "☁ Weather Guide"
], horizontal=True)
st.markdown("---")

# =======================================================
# --- TOOL 1: GENERAL AGRICULTURE CHATBOT (TEXT ONLY) ---
# =======================================================
if app_mode == "💬 Agri Chatbot (Text Only)":
    st.title("💬 General Agri Chatbot")
    st.write("Ask any text-based question about farming, crops, or general agriculture.")
    
    # Text Input for General Questions (like the cotton example)
    user_question = st.text_input("Your Question:", placeholder="e.g., hat amount of water I can use for growing cotton?")
    
    if st.button("Ask Agri-AI"):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # General text analysis prompt
                    prompt = f"You are an expert agriculture consultant. Answer this question for a farmer in simple English: {user_question}"
                    response = model.generate_content(prompt)
                    st.success("Agri-GPT Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# =======================================================
# --- TOOL 2: PLANT DISEASE DETECTOR (IMAGE ONLY) ---
# =======================================================
elif app_mode == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.write("Upload a photo of a sick leaf for diagnosis.")

    # Get image input (This area is for the image)
    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader("1. Upload Leaf Photo:", type=["jpg", "jpeg", "png"])
    with col2:
        camera_image = st.camera_input("Camera", label_visibility="collapsed")
        
    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Uploaded Leaf", use_column_width=True)
        
        if st.button("Identify Disease"):
            with st.spinner("Analyzing..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = "Analyze this plant leaf. Name the plant, identify the disease, and suggest a cure."
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# =======================================================
# --- TOOL 3: SEED QUALITY CHECKER (IMAGE ONLY) ---
# =======================================================
elif app_mode == "🌾 Seed Quality Checker":
    st.header("🌾 Seed Quality Checker")
    st.write("Upload a photo of seeds to check quality and count.")
    
    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader("1. Upload Seed Photo:", type=["jpg", "jpeg", "png"])
    with col2:
        camera_image = st.camera_input("Camera", label_visibility="collapsed") 
        
    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Uploaded Seeds", use_column_width=True)
        
        if st.button("Check Quality"):
            with st.spinner("Counting seeds..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "Analyze these seeds. Estimate count. Check for breakage/rot. Rate quality."
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# =======================================================
# --- TOOL 4: WEATHER GUIDE (DROPDOWN TOOL) ---
# =======================================================
elif app_mode == "☁ Weather Guide":
    st.header("☁ Weather Guide")
    st.write("Select your conditions to get farming advice.")

    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Season:", ["Summer", "Monsoon (Rainy)", "Winter"])
    with col2:
        sky = st.selectbox("Sky Look:", ["Sunny", "Cloudy", "Rainy"])

    st.markdown("### 📢 Farming Advice:")
    if sky == "Rainy":
        st.warning("⛈ *Rain Alert:* Delay pesticide spraying.")
    elif season == "Summer" and sky == "Sunny":
        st.error("☀ *Heat Alert:* Water crops in the evening.")
    elif season == "Monsoon (Rainy)":
        st.info("🌧 *Fungal Risk:* Monitor leaves closely for spots.")
    elif season == "Winter":
        st.success("❄ *Cool & Dry:* Ideal for planting leafy vegetables.")

