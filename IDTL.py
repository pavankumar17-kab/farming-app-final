import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# --- 1. SETUP ---
st.set_page_config(page_title="Agri-GPT", page_icon="🌱")

# ------------------------------------------------------------------
# 🔑 PASTE YOUR KEY HERE
# Replace "YOUR_API_KEY" with the long code from Google
# ✅ CORRECT:
GOOGLE_API_KEY = "AIzaSyD-5mPq8-Kj9... (your real code)"
# ------------------------------------------------------------------

# Configure AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Key Error: {e}")

# --- 2. SIDEBAR ---
st.sidebar.title("Agri-GPT Menu")
option = st.sidebar.radio(
    "Select Feature:",
    [
        "💬 Chatbot / ಚಾಟ್‌ಬಾಟ್", 
        "🟢 Disease Detector / ರೋಗ ಪತ್ತೆ", 
        "🌾 Seed Quality / ಬೀಜ ಗುಣಮಟ್ಟ", 
        "☁️ Weather / ಹವಾಮಾನ"
    ]
)

# --- 3. MAIN APP ---

if option == "💬 Chatbot / ಚಾಟ್‌ಬಾಟ್":
    st.header("💬 General Agri Chatbot")
    st.write("Ask any question about farming (Type or Speak).")
    
    # --- VOICE SECTION ---
    st.write("---")
    st.write("🎙️ **Speak / ಮಾತನಾಡಿ:**")
    
    voice_text = speech_to_text(
        language='en', # You can change to 'kn' for Kannada voice recognition if needed
        start_prompt="Click to Record / ರೆಕಾರ್ಡ್ ಮಾಡಿ",
        stop_prompt="Stop / ನಿಲ್ಲಿಸಿ",
        just_once=True,
        key='STT'
    )

    if voice_text:
        st.success(f"🗣️ Heard: {voice_text}")

    # --- TEXT SECTION ---
    st.write("⌨️ **Or Type / ಅಥವಾ ಬರೆಯಿರಿ:**")
    text_input = st.text_input("Your Question:", placeholder="How to grow apple / ಸೇಬು ಬೆಳೆಯುವುದು ಹೇಗೆ?")

    # --- BUTTON TO ASK ---
    if st.button("Ask Agri-AI / ಕೇಳಿ"):
        # Decide input
        user_question = voice_text if voice_text else text_input
        
        if not user_question:
            st.warning("Please speak or type a question first.")
        else:
            # Check for API Key
            if "YOUR_API_KEY" in GOOGLE_API_KEY:
                st.error("⚠️ Error: Please insert your Google API Key in the code (Line 11).")
            else:
                with st.spinner("Agri-GPT is thinking..."):
                    try:
                        # Prompt
                        prompt = (
                            f"You are an expert agricultural scientist. "
                            f"Answer this question simply: {user_question}"
                        )
                        response = model.generate_content(prompt)
                        st.markdown("### 💡 Answer / ಉತ್ತರ:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

# (Other placeholders kept simple for now)
elif option == "🟢 Disease Detector / ರೋಗ ಪತ್ತೆ":
    st.header("🟢 Plant Disease Detector")
    st.file_uploader("Upload Leaf / ಎಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ", type=['jpg', 'png'])

elif option == "🌾 Seed Quality / ಬೀಜ ಗುಣಮಟ್ಟ":
    st.header("🌾 Seed Quality Checker")
    st.write("Coming Soon...")

elif option == "☁️ Weather / ಹವಾಮಾನ":
    st.header("☁️ Weather Predictor")
    st.write("Coming Soon...")

