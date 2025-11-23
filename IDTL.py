import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="app_icon.png.png", layout="centered")

# Connect to Google AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. HELPER FUNCTIONS (VOICE) ---

# Function to make the phone speak (Text-to-Speech)
def speak_text(text):
    # Clean text to remove quotes/newlines that break JavaScript
    safe_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    
    # JavaScript to trigger browser voice
    html_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance();
        msg.text = "{safe_text}";
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(html_code, height=0, width=0)

# --- 3. LANGUAGE SELECTOR (TOP RIGHT) ---
# Use columns to push the language selector to the right
col_spacer, col_lang = st.columns((7, 3))
with col_lang:
    # Use selectbox for narrow space, with hidden label
    lang_choice = st.selectbox("Select Language:", ["English", "Kannada (ಕನ್ನಡ)"], 
                                label_visibility="collapsed")
    st.caption("Language / ಭಾಷೆ") # Small label below the box

st.header("🚜 Agri-Dashboard")

# Main Menu (4 Tools)
app_mode = st.radio("Select Tool:", [
    "💬 Agri Chatbot (Text)", 
    "🟢 Plant Disease Detector", 
    "🌾 Seed Quality Checker", 
    "☁ Weather Guide"
], horizontal=True)
st.markdown("---")


# --- TOOL 1: GENERAL AGRI CHATBOT (TEXT) ---
if app_mode == "💬 Agri Chatbot (Text)":
    st.title("💬 General Agri Chatbot")
    st.write("Ask any question about farming.")
    
    # Use columns to place the Mic icon next to the input box
    col_mic_icon, col_text_input = st.columns((1, 9))
    
    with col_mic_icon:
        st.markdown("<h3 style='margin-top: 20px;'>🎙</h3>", unsafe_allow_html=True)
        # Inform the user to use the keyboard's native mic
        st.caption("Use Keyboard Mic") 
    
    with col_text_input:
        user_question = st.text_input("Your Question:", 
                                      placeholder="e.g., hat amount of water I can use for growing cotton?",
                                      label_visibility="collapsed")
    
    if st.button("Ask Agri-AI"):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = f"You are an agriculture expert. Answer this question in KANNADA language: {user_question}"
                    else:
                        prompt = f"You are an agriculture expert. Answer this question in English: {user_question}"
                        
                    response = model.generate_content(prompt)
                    st.success("Answer:")
                    st.write(response.text)
                    
                    if st.button("🔊 Read Aloud"):
                        speak_text(response.text)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TOOL 2: PLANT DISEASE DETECTOR ---
elif app_mode == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.write("Upload a leaf photo.")

    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader("1. Upload Leaf:", type=["jpg", "png", "jpeg"])
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
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = "Analyze this leaf. 1. Name the plant. 2. Identify disease. 3. Suggest cure. Give output in KANNADA."
                    else:
                        prompt = "Analyze this leaf. 1. Name the plant. 2. Identify disease. 3. Suggest cure."
                        
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                    
                    if st.button("🔊 Read Aloud"):
                        speak_text(response.text)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TOOL 3: SEED QUALITY CHECKER ---
elif app_mode == "🌾 Seed Quality Checker":
    st.header("🌾 Seed Quality Checker")
    st.write("Upload seed photo.")
    
    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader("1. Upload Seeds:", type=["jpg", "png"])
    with col2:
        camera_image = st.camera_input("Camera", label_visibility="collapsed") 
        
    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption="Uploaded Seeds", use_column_width=True)
        
        if st.button("Check Quality"):
            with st.spinner("Counting..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = "Count these seeds. Check for breakage. Rate quality. Give output in KANNADA."
                    else:
                        prompt = "Count these seeds. Check for breakage. Rate quality."
                        
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                    
                    if st.button("🔊 Read Aloud"):
                        speak_text(response.text)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TOOL 4: WEATHER GUIDE ---
elif app_mode == "☁ Weather Guide":
    st.header("☁ Weather Guide")
    
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Season:", ["Summer", "Monsoon (Rainy)", "Winter"])
    with col2:
        sky = st.selectbox("Sky Look:", ["Sunny", "Cloudy", "Rainy"])

    st.markdown("### 📢 Farming Advice:")
    
    if sky == "Rainy":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.warning("⛈ *Rain Alert:* ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ. (Do not spray pesticides).")
        else:
            st.warning("⛈ *Rain Alert:* Delay pesticide spraying.")
            
    elif season == "Summer" and sky == "Sunny":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.error("☀ *Heat Alert:* ಸಂಜೆ ಬೆಳೆಗಳಿಗೆ ನೀರು ಹಾಕಿ. (Water crops in the evening).")
        else:
            st.error("☀ *Heat Alert:* Water crops in the evening.")
            
    elif season == "Monsoon (Rainy)":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.info("🌧 *Fungal Risk:* ಎಲೆಗಳ ಮೇಲೆ ಕಲೆಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ. (Check leaves for spots).")
        else:
            st.info("🌧 *Fungal Risk:* Monitor leaves closely for spots.")
            
    elif season == "Winter":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.success("❄ *Cool & Dry:* ಸೊಪ್ಪು ಬೆಳೆಯಲು ಉತ್ತಮ ಸಮಯ. (Good for leafy vegetables).")
        else:
            st.success("❄ *Cool & Dry:* Ideal for planting leafy vegetables.")
