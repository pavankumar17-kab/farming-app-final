import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components 
from streamlit_mic_recorder import speech_to_text # <--- ONLY CHANGE: Added Import

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agri-Smart AI", page_icon="🌿", layout="centered")

# Connect to Google AI (KEPT YOUR ORIGINAL SECRETS CODE)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠ Google API Key missing! Please add it to Streamlit Secrets.")

# --- 2. TRANSLATION DICTIONARY ---

TRANSLATIONS = {
    "English": {
        "dashboard_header": "🚜 Agri-Dashboard",
        "select_tool": "Select Tool:",
        "tool_chat": "💬 Agri Chatbot (Text)",
        "tool_disease": "🟢 Plant Disease Detector",
        "tool_seed": "🌾 Seed Quality Checker",
        "tool_weather": "☁ Weather Guide",
        "chat_title": "💬 General Agri Chatbot",
        "chat_description": "Ask any text-based question about farming.",
        "your_question": "Your Question:",
        "ask_button": "Ask Agri-AI",
        "answer_title": "Agri-GPT Answer:",
        "question_placeholder": "e.g., hat amount of water I can use for growing cotton?",
        "voice_label": "🎤 Tap to Speak:", # Added label
        
        "detector_header": "🟢 Plant Disease Detector",
        "detector_description": "Upload a photo of a sick leaf for diagnosis.",
        "upload_leaf": "1. Upload Leaf Photo:",
        "camera_label": "Camera",
        "identify_button": "Identify Disease",
        "uploaded_leaf_caption": "Uploaded Leaf",
        
        "checker_header": "🌾 Seed Quality Checker",
        "checker_description": "Upload a photo of seeds to check quality and count.",
        "upload_seed": "1. Upload Seed Photo:",
        "check_button": "Check Quality",
        "uploaded_seed_caption": "Uploaded Seeds",

        "weather_header": "☁ Weather Guide",
        "weather_description": "Select your conditions to get farming advice.",
        "season": "Season:",
        "sky_look": "Sky Look:",
        "summer": "Summer",
        "monsoon": "Monsoon (Rainy)",
        "winter": "Winter",
        "sunny": "Sunny",
        "cloudy": "Cloudy",
        "rainy": "Rainy",
        "advice_header": "📢 Farming Advice:",
    },
    "Kannada (ಕನ್ನಡ)": {
        "dashboard_header": "🚜 ಕೃಷಿ-ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "select_tool": "ಸಾಧನ ಆಯ್ಕೆಮಾಡಿ:",
        "tool_chat": "💬 ಕೃಷಿ ಚಾಟ್‌ಬಾಟ್ (ಪಠ್ಯ)",
        "tool_disease": "🟢 ಸಸ್ಯ ರೋಗ ಪತ್ತೆ",
        "tool_seed": "🌾 ಬೀಜ ಗುಣಮಟ್ಟ ಪರೀಕ್ಷಕ",
        "tool_weather": "☁ ಹವಾಮಾನ ಮಾರ್ಗದರ್ಶಿ",
        "chat_title": "💬 ಸಾಮಾನ್ಯ ಕೃಷಿ ಚಾಟ್‌ಬಾಟ್",
        "chat_description": "ಕೃಷಿಯ ಬಗ್ಗೆ ಯಾವುದೇ ಪಠ್ಯ ಆಧಾರಿತ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ.",
        "your_question": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ:",
        "ask_button": "ಕೃಷಿ-AI ಗೆ ಕೇಳಿ",
        "answer_title": "ಕೃಷಿ-GPT ಉತ್ತರ:",
        "question_placeholder": "ಉದಾ. ಹತ್ತಿ ಬೆಳೆಯಲು ಎಷ್ಟು ನೀರು ಬಳಸಬಹುದು?",
        "voice_label": "🎤 ಮಾತನಾಡಲು ಕ್ಲಿಕ್ ಮಾಡಿ:", # Added label

        "detector_header": "🟢 ಸಸ್ಯ ರೋಗ ಪತ್ತೆ",
        "detector_description": "ರೋಗಗ್ರಸ್ತ ಎಲೆಯ ಫೋಟೋವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ.",
        "upload_leaf": "1. ಎಲೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ:",
        "camera_label": "ಕ್ಯಾಮೆರಾ",
        "identify_button": "ರೋಗವನ್ನು ಗುರುತಿಸಿ",
        "uploaded_leaf_caption": "ಅಪ್ಲೋಡ್ ಮಾಡಿದ ಎಲೆ",

        "checker_header": "🌾 ಬೀಜ ಗುಣಮಟ್ಟ ಪರೀಕ್ಷಕ",
        "checker_description": "ಗುಣಮಟ್ಟ ಮತ್ತು ಎಣಿಕೆ ಪರೀಕ್ಷಿಸಲು ಬೀಜಗಳ ಫೋಟೋವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ.",
        "upload_seed": "1. ಬೀಜಗಳ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ:",
        "check_button": "ಗುಣಮಟ್ಟ ಪರಿಶೀಲಿಸಿ",
        "uploaded_seed_caption": "ಅಪ್ಲೋಡ್ ಮಾಡಿದ ಬೀಜಗಳು",

        "weather_header": "☁ ಹವಾಮಾನ ಮಾರ್ಗದರ್ಶಿ",
        "weather_description": "ಕೃಷಿ ಸಲಹೆ ಪಡೆಯಲು ನಿಮ್ಮ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "season": "ಋತು:",
        "sky_look": "ಆಕಾಶದ ನೋಟ:",
        "summer": "ಬೇಸಿಗೆ",
        "monsoon": "ಮುಂಗಾರು (ಮಳೆ)",
        "winter": "ಚಳಿಗಾಲ",
        "sunny": "ಬಿಸಿಲು",
        "cloudy": "ಮೋಡ",
        "rainy": "ಮಳೆ",
        "advice_header": "📢 ಕೃಷಿ ಸಲಹೆ:",
    }
}

# --- 3. HELPER FUNCTIONS (VOICE) ---

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
        // Necessary to load voices property on Android/iOS
        window.speechSynthesis.getVoices(); 
        window.speakNow = speakNow; // Make function globally accessible
    </script>
    """
    # Inject the script 
    components.html(js_code, height=0)

    # Use a standard Streamlit button that calls the JS function when clicked
    if st.button("🔊 Read Aloud"):
        # Execute the speakNow function from the injected script
        st.components.v1.html("""
            <script>
                if (window.speakNow) {
                    window.speakNow();
                }
            </script>
        """, height=0, width=0)

# --- 4. LANGUAGE SELECTION AND MAPPING ---

# Use columns to push the language selector to the right and above the dashboard
col_spacer, col_lang = st.columns((6, 4))
with col_lang:
    # Selectbox for narrow space
    lang_choice = st.selectbox("Select Language:", ["English", "Kannada (ಕನ್ನಡ)"], 
                                label_visibility="collapsed")
    st.caption("Language / ಭಾಷೆ") 

# Get the current set of translations based on user choice
T = TRANSLATIONS[lang_choice]

st.header(T["dashboard_header"])

# Main Menu (4 Tools) - Use translated labels for the radio buttons
app_mode = st.radio(T["select_tool"], [
    T["tool_chat"], 
    T["tool_disease"], 
    T["tool_seed"], 
    T["tool_weather"]
], horizontal=True)
st.markdown("---")

# =======================================================
# --- TOOL 1: GENERAL AGRICULTURE CHATBOT (TEXT ONLY) ---
# =======================================================
if app_mode == T["tool_chat"]:
    st.title(T["chat_title"])
    st.write(T["chat_description"])
    
    # --- ONLY CHANGE: Added Voice Recorder Here ---
    st.write(f"**{T['voice_label']}**")
    voice_input = speech_to_text(
        language='en',
        start_prompt="🔴 Record / ರೆಕಾರ್ಡ್",
        stop_prompt="⬛ Stop / ನಿಲ್ಲಿಸಿ",
        just_once=True,
        key='STT'
    )
    if voice_input:
        st.info(f"🗣️ Heard: {voice_input}")
    # ---------------------------------------------
    
    # Use columns to place the Mic icon (🎙) to the left of the input box
    col_mic_icon, col_text_input = st.columns((1, 9))
    
    with col_mic_icon:
        st.markdown("<h3 style='margin-top: 20px; text-align: center;'>🎙</h3>", unsafe_allow_html=True)
    
    with col_text_input:
        text_input_val = st.text_input(T["your_question"], 
                                      placeholder=T["question_placeholder"],
                                      label_visibility="collapsed")
    
    # Logic: Use voice input if available, otherwise use text input
    user_question = voice_input if voice_input else text_input_val
    
    if st.button(T["ask_button"]):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    # KEPT YOUR ORIGINAL MODEL NAME
                    model = genai.GenerativeModel('gemini-2.5-flash') 
                    
                    if lang_choice == "Kannada (ಕನ್ನಡ)":
                        prompt = f"You are an expert agriculture consultant. Answer this question in DETAILED KANNADA language: {user_question}"
                    else:
                        prompt = f"You are an expert agriculture consultant. Answer this question in simple English: {user_question}"
                        
                    response = model.generate_content(prompt)
                    st.success(T["answer_title"])
                    st.write(response.text)
                    
                    # Voice Button injected immediately after the answer
                    TTS_Button(response.text, lang_choice)

                except Exception as e:
                    st.error(f"Error: {e}")

# =======================================================
# --- TOOL 2: PLANT DISEASE DETECTOR (IMAGE ONLY) ---
# =======================================================
elif app_mode == T["tool_disease"]:
    st.header(T["detector_header"])
    st.write(T["detector_description"])

    # Get image input (Upload is LARGE, Camera is small)
    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader(T["upload_leaf"], type=["jpg", "jpeg", "png"])
    with col2:
        camera_image = st.camera_input(T["camera_label"], label_visibility="collapsed")
        
    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption=T["uploaded_leaf_caption"], use_container_width=True)
        
        if st.button(T["identify_button"]):
            with st.spinner("Analyzing..."):
                try:
                    # KEPT YOUR ORIGINAL MODEL NAME
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
elif app_mode == T["tool_seed"]:
    st.header(T["checker_header"])
    st.write(T["checker_description"])
    
    col1, col2 = st.columns((3, 1))
    with col1:
        uploaded_file = st.file_uploader(T["upload_seed"], type=["jpg", "jpeg", "png"])
    with col2:
        camera_image = st.camera_input(T["camera_label"], label_visibility="collapsed") 
        
    input_image = uploaded_file or camera_image

    if input_image:
        image = Image.open(input_image)
        st.image(image, caption=T["uploaded_seed_caption"], use_container_width=True)
        
        if st.button(T["check_button"]):
            with st.spinner("Counting seeds..."):
                try:
                    # KEPT YOUR ORIGINAL MODEL NAME
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
elif app_mode == T["tool_weather"]:
    st.header(T["weather_header"])
    st.write(T["weather_description"])

    # Translate Dropdown Options
    season_options = [T["summer"], T["monsoon"], T["winter"]]
    sky_options = [T["sunny"], T["cloudy"], T["rainy"]]
    
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox(T["season"], season_options)
    with col2:
        sky = st.selectbox(T["sky_look"], sky_options)

    st.markdown(f"### {T['advice_header']}")
    
    # Check conditions using the translated strings
    is_rainy = sky == T["rainy"]
    is_summer_sunny = (season == T["summer"]) and (sky == T["sunny"])
    is_monsoon = season == T["monsoon"]
    is_winter = season == T["winter"]

    # Display advice based on translated conditions
    if is_rainy:
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.warning("⛈ ಮಳೆ ಎಚ್ಚರಿಕೆ: ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ. (Do not spray pesticides).")
        else:
            st.warning("⛈ Rain Alert: Delay pesticide spraying.")
            
    elif is_summer_sunny:
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.error("☀ ಬಿಸಿಲಿನ ಎಚ್ಚರಿಕೆ: ಸಂಜೆ ಬೆಳೆಗಳಿಗೆ ನೀರು ಹಾಕಿ. (Water crops in the evening).")
        else:
            st.error("☀ Heat Alert: Water crops in the evening.")
            
    elif is_monsoon:
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.info("🌧 ಶಿಲೀಂಧ್ರದ ಅಪಾಯ: ಎಲೆಗಳ ಮೇಲೆ ಕಲೆಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ. (Check leaves for spots).")
        else:
            st.info("🌧 Fungal Risk: Monitor leaves closely for spots.")
            
    elif is_winter:
        if lang_choice == "Kannada (ಕನ್ನಡ)":
            st.success("❄ ತಂಪು ಮತ್ತು ಶುಷ್ಕ: ಸೊಪ್ಪು ಬೆಳೆಯಲು ಉತ್ತಮ ಸಮಯ. (Ideal for planting leafy vegetables).")
        else:
            st.success("❄ Cool & Dry: Ideal for planting leafy vegetables.")
