import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SETUP: MOBILE FRIENDLY CONFIG ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="🌿", layout="centered")

# Connect to the Google AI Brain (Gemini)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. SIDEBAR MENU (The Old Options Restored) ---
st.sidebar.title("🚜 Agri-Dashboard")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("Select Tool:", [
    "🌿 Plant Disease Doctor",
    "🌰 Smart Seed Checker",
    "🌤 Weather Detector"
])

# --- OPTION 1: PLANT DISEASE DOCTOR (Heavy AI) ---
if app_mode == "🌿 Plant Disease Doctor":
    st.title("🌿 Plant Disease Doctor")
    st.markdown("Upload a leaf photo. The AI will diagnose diseases and suggest medicines.")

    uploaded_file = st.file_uploader("Upload Leaf Photo", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf", use_column_width=True)
        
        if st.button("Diagnose Disease"):
            with st.spinner("Consulting the AI Expert..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (
                        "You are an expert agricultural botanist. Analyze this image of a plant leaf. "
                        "1. Identify the plant name. "
                        "2. detailed analysis of the disease (or confirm if healthy). "
                        "3. Suggest specific chemical or organic fertilizers/medicines to cure it. "
                        "4. Provide prevention tips."
                    )
                    response = model.generate_content([prompt, image])
                    st.success("Diagnosis Complete!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPTION 2: SEED CHECKER (Upgraded to AI) ---
elif app_mode == "🌰 Smart Seed Checker":
    st.title("🌰 Smart Seed Checker")
    st.markdown("Upload a photo of your seeds. The AI will check quality and breakage.")

    uploaded_seed = st.file_uploader("Upload Seed Photo", type=["jpg", "jpeg", "png"])
    
    if uploaded_seed:
        image = Image.open(uploaded_seed)
        st.image(image, caption="Uploaded Seeds", use_column_width=True)
        
        if st.button("Check Quality"):
            with st.spinner("Analyzing seeds..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # This replaces your old "Yellow Pixel" math with real intelligence
                    prompt = (
                        "Analyze this image of seeds. "
                        "1. Estimate the approximate count. "
                        "2. Detect if there are broken, discolored, or shriveled seeds. "
                        "3. Rate the overall quality (High/Medium/Low) for farming."
                    )
                    response = model.generate_content([prompt, image])
                    st.info("Seed Quality Report:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPTION 3: WEATHER DETECTOR (Restored) ---
elif app_mode == "🌤 Weather Detector":
    st.title("🌤 Weather Detector & Guide")
    st.write("Select your current conditions to get farming advice.")

    # This mimics your old manual detector since phones can't sense weather directly
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Current Season:", ["Summer", "Monsoon (Rainy)", "Winter", "Spring"])
    with col2:
        sky = st.selectbox("Sky Condition:", ["Sunny/Clear", "Cloudy", "Rainy/Stormy"])

    st.markdown("### 📢 Farming Advice:")
    
    # Logic for advice
    if sky == "Rainy/Stormy":
        st.warning("⛈ *Storm Alert:* Stop spraying pesticides immediately (they will wash off). Ensure field drainage is clear to prevent waterlogging.")
    elif season == "Summer" and sky == "Sunny/Clear":
        st.error("☀ *Heat Alert:* High evaporation rate. Irrigate crops early morning or late evening.")
    elif season == "Monsoon (Rainy)":
        st.info("🌧 *Fungal Risk:* High humidity promotes fungus. Monitor leaves closely for spots.")
    elif season == "Winter":
        st.success("❄ *Frost Watch:* Protect young seedlings from cold winds.")
    else:
        st.success("✅ Conditions are good for standard farming activities.")
