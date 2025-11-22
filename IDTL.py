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

# --- 2. MAIN MENU (VISIBLE ON FRONT PAGE) ---
st.header("🚜 Agri-Dashboard")
app_mode = st.radio("Select Tool:", [
    "🌿 AI Plant Doctor (Chat)", 
    "🌰 Smart Seed Checker", 
    "🌤 Weather Guide"
], horizontal=True)
st.markdown("---")


# --- TOOL 1: PLANT DOCTOR (Chatbot Style) ---
if app_mode == "🌿 AI Plant Doctor (Chat)":
    st.title("🌿 AI Plant Doctor")
    
    with st.chat_message("assistant"):
        st.write("Hello! Upload a photo below and ask me any question about the plant.")

    # Get image input (Upload is LARGE, Camera is small)
    col1, col2 = st.columns((3, 1)) # 3/4 width for file uploader, 1/4 for camera
    with col1:
        # Full width, large button
        uploaded_file = st.file_uploader("1. Upload Leaf Photo:", type=["jpg", "jpeg", "png"]) 
    with col2:
        # Narrow column makes this button small
        camera_image = st.camera_input("Camera", label_visibility="collapsed") 

    input_image = uploaded_file or camera_image # Logic to use either source

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Your Photo", use_column_width=True)
        
        user_question = st.chat_input("Ask a question about this plant...")
        
        if user_question:
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([user_question, image])
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")


# --- TOOL 2: SEED CHECKER ---
elif app_mode == "🌰 Smart Seed Checker":
    st.title("🌰 Smart Seed Checker")
    
    # Get image input (Upload is LARGE, Camera is small)
    col1, col2 = st.columns((3, 1)) # 3/4 width for file uploader, 1/4 for camera
    with col1:
        # Full width, large button
        uploaded_file = st.file_uploader("1. Upload Seed Photo:", type=["jpg", "jpeg", "png"]) 
    with col2:
        # Narrow column makes this button small
        camera_image = st.camera_input("Camera", label_visibility="collapsed") 

    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Your Seeds", use_column_width=True)
        
        if st.button("Check Quality"):
            with st.chat_message("assistant"):
                with st.spinner("Counting seeds..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = "Analyze this image of seeds. Estimate count. Check for breakage/rot. Give a quality rating."
                        response = model.generate_content([prompt, image])
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")


# --- TOOL 3: WEATHER GUIDE ---
elif app_mode == "🌤 Weather Guide":
    st.title("🌤 Weather Guide")
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
