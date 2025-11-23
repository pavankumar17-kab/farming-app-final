import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components # Required for Voice Assistant

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="🌿", layout="centered")

# Connect to Google AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. HELPER FUNCTIONS (VOICE) ---

# This function uses a dedicated JavaScript component to reliably trigger TTS on mobile.
def TTS_Button(text_to_speak, lang_choice):
    # Sanitize text for JavaScript
    safe_text = text_to_speak.replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
    
    # Set the appropriate language code for better native accent support
    if lang_choice == "Kannada (ಕನ್ನಡ)":
        lang_code = 'kn-IN'
    else:
        lang_code = 'en-US'

    # The actual TTS JavaScript logic, wrapped in a function call
    js_code = f"""
    <script>
        function speakNow() {{
            var msg = new SpeechSynthesisUtterance();
            msg.text = '{safe_text}';
            msg.lang = '{lang_code}'; 
            
            // Attempt to find a native voice
            var voices = window.speechSynthesis.getVoices();
            var selectedVoice = voices.find(v => v.lang.includes('{lang_code}')) || voices.find(v => v.default);
            if (selectedVoice) {{
                msg.voice = selectedVoice;
            }}

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    # Inject the script only once (optional, but clean)
    components.html(js_code, height=0)

    # Use a standard Streamlit button that calls the JS function when clicked
    # This is the most reliable way to ensure the click is recognized by the browser
    if st.button("🔊 Read Aloud"):
        # We execute the speakNow function from the injected script
        st.components.v1.html("""
            <script>
                // Need to re-trigger the function call after the button click is registered
                document.addEventListener("DOMContentLoaded", function(event) {
                    if (window.speakNow) {
                        window.speakNow();
                    }
                });
                // Immediate call attempt
                if (window.speakNow) {
                    window.speakNow();
                }
            </script>
        """, height=0, width=0)


# --- 3. LANGUAGE SELECTOR (TOP RIGHT) ---
# Use columns to push the language selector to the right and above the dashboard
col_spacer, col_lang = st.columns((6, 4))
with col_lang:
    # Selectbox for narrow space
    lang_choice = st.selectbox("Select Language:", ["English", "Kannada (ಕನ್ನಡ)"], 
                                label_visibility="collapsed")
    st.caption("Language / ಭಾಷೆ") 

st.header("🚜 Agri-Dashboard")

# Main Menu (4 Tools)
app_mode = st.radio("Select Tool:", [
    "💬 Agri Chatbot (Text)", 
    "🟢 Plant Disease Detector", 
    "🌾 Seed Quality Checker", 
    "☁ Weather Guide"
], horizontal=True)
st.markdown("---")

# =======================================================
# --- TOOL 1: GENERAL AGRICULTURE CHATBOT (TEXT ONLY) ---
# =======================================================
if app_mode == "💬 Agri Chatbot (Text)":
    st.title("💬 General Agri Chatbot")
    st.write("Ask any text-based question about farming.")
    
    # Use columns to place the Mic icon (🎙) to the left of the input box
    col_mic_icon, col_text_input = st.columns((1, 9))
    
    with col_mic_icon:
        # Markdown for the icon and a bit of vertical spacing
        st.markdown("<h3 style='margin-top: 20px; text-align: center;'>🎙</h3>", unsafe_allow_html=True)
    
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
                        prompt = f"You are an expert agriculture consultant. Answer this question in DETAILED KANNADA language: {user_question}"
                    else:
                        prompt = f"You are an expert agriculture consultant. Answer this question in simple English: {user_question}"
                        
                    response = model.generate_content(prompt)
                    st.success("Agri-GPT Answer:")
                    st.write(response.text)
                    
                    # Voice Button injected immediately after the answer
                    TTS_Button(response.text, lang_choice)

                except Exception as e:
                    st.error(f"Error: {e}")

# =======================================================
# --- TOOL 2: PLANT DISEASE DETECTOR (IMAGE ONLY) ---
# =======================================================
elif app_mode == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.write("Upload a photo of a sick leaf for diagnosis.")

    # Get image input (Upload is LARGE, Camera is small)
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
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = "Analyze this plant leaf. Name the plant, identify the disease, and suggest a cure. Provide the full analysis in KANNADA."
                    else:
                        prompt = "Analyze this plant leaf. Name the plant, identify the disease, and suggest a cure."
                        
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                    
                    # Voice Button injected immediately after the answer
                    TTS_Button(response.text, lang_choice)

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
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = "Analyze these seeds. Estimate count. Check for breakage/rot. Rate quality. Provide the full analysis in KANNADA."
                    else:
                        prompt = "Analyze these seeds. Estimate count. Check for breakage/rot. Rate quality."
                        
                    response = model.generate_content([prompt, image])
                    st.write(response.text)
                    
                    # Voice Button injected immediately after the answer
                    TTS_Button(response.text, lang_choice)
                        
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
    
    # Static advice with embedded Kannada translation
    if sky == "Rainy":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.warning("⛈ ಮಳೆ ಎಚ್ಚರಿಕೆ: ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ. (Do not spray pesticides).")
        else:
            st.warning("⛈ Rain Alert: Delay pesticide spraying.")
            
    elif season == "Summer" and sky == "Sunny":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.error("☀ ಬಿಸಿಲಿನ ಎಚ್ಚರಿಕೆ: ಸಂಜೆ ಬೆಳೆಗಳಿಗೆ ನೀರು ಹಾಕಿ. (Water crops in the evening).")
        else:
            st.error("☀ Heat Alert: Water crops in the evening.")
            
    elif season == "Monsoon (Rainy)":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.info("🌧 ಶಿಲೀಂಧ್ರದ ಅಪಾಯ: ಎಲೆಗಳ ಮೇಲೆ ಕಲೆಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ. (Check leaves for spots).")
        else:
            st.info("🌧 Fungal Risk: Monitor leaves closely for spots.")
            
    elif season == "Winter":
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.success("❄ ತಂಪು ಮತ್ತು ಶುಷ್ಕ: ಸೊಪ್ಪು ಬೆಳೆಯಲು ಉತ್ತಮ ಸಮಯ. (Ideal for planting leafy vegetables).")
        else:
            st.success("❄ Cool & Dry: Ideal for planting leafy vegetables.")
