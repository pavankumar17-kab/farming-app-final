import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="app_icon.png.png", layout="centered")
# Connect to Google AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. SIDEBAR MENU ---
st.sidebar.header("🚜 Agri-Dashboard")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("Select Tool:", [
    "🌿 AI Plant Doctor (Chat)", 
    "🌰 Smart Seed Checker", 
    "🌤 Weather Guide"
])

# --- FUNCTION TO GET INPUT ---
def get_image_input():
    col_upload, col_camera = st.columns(2)
    with col_upload:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    with col_camera:
        # This forces the camera option to be visible
        camera_image = st.camera_input("Take Photo Directly") 
        
    return uploaded_file or camera_image # Returns one or the other

# --- TOOL 1: PLANT DOCTOR (Chatbot Style) ---
if app_mode == "🌿 AI Plant Doctor (Chat)":
    st.title("🌿 AI Plant Doctor")
    
    with st.chat_message("assistant"):
        st.write("Hello! I am your AI Expert. Use the buttons below to upload or take a photo, then ask me anything.")

    # Get image input using the new combined function
    input_image = get_image_input()
    
    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Your Photo", use_column_width=True)
        
        user_question = st.chat_input("Ask a question about this plant...")
        
        if user_question:
            # Show User Question
            with st.chat_message("user"):
                st.write(user_question)
            
            # Show AI Response
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
    st.write("Upload or take a photo of seeds to check quality.")

    # Get image input using the new combined function
    input_seed_image = get_image_input()

    if input_seed_image:
        image = Image.open(input_seed_image)
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
