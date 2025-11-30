import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# --- 1. SETUP ---
st.set_page_config(page_title="Agri-AI Assistant", page_icon="🌱")

# PASTE YOUR API KEY HERE
GOOGLE_API_KEY = "YOUR_API_KEY"

# Configure the AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ Error configuring AI. Please check your API Key.")

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("Agri-GPT Menu")
option = st.sidebar.radio(
    "Go to:",
    [
        "💬 Agriculture Chatbot", 
        "🟢 Plant Disease Detector", 
        "🌾 Seed Quality Checker", 
        "☁️ Weather Predictor"
    ]
)

# --- 3. MAIN APP LOGIC ---

if option == "💬 Agriculture Chatbot":
    st.header("💬 Agri-GPT Chatbot")
    st.write("Ask any question about farming, crops, or fertilizers.")

    # --- VOICE INPUT SECTION ---
    st.write("---")
    st.write("🎤 **Option 1: Speak your question**")
    
    # This button listens to your voice
    text_from_voice = speech_to_text(
        language='en',
        start_prompt="Click to Record",
        stop_prompt="Stop Recording",
        just_once=True,
        key='STT'
    )
    
    if text_from_voice:
        st.success(f"🗣️ Heard: {text_from_voice}")

    # --- TEXT INPUT SECTION ---
    st.write("**Option 2: Type your question**")
    text_from_box = st.text_input("Type here:", placeholder="e.g., How to grow tomatoes?")

    # --- DECIDE WHICH INPUT TO USE ---
    user_question = text_from_voice if text_from_voice else text_from_box

    # --- SEND TO AI ---
    if user_question:
        if "YOUR_API_KEY" in GOOGLE_API_KEY:
            st.warning("⚠️ Please put your Google API Key in the code.")
        else:
            with st.spinner("Agri-GPT is thinking..."):
                try:
                    # Specific instructions for the AI
                    prompt = (
                        f"You are an expert farmer and agricultural scientist. "
                        f"Answer this question simply and clearly: {user_question}"
                    )
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("### 💡 Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

elif option == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.info("Upload a photo of a plant leaf to detect diseases.")
    st.file_uploader("Upload Leaf Image", type=['jpg', 'png', 'jpeg'])

elif option == "🌾 Seed Quality Checker":
    st.header("🌾 Seed Quality Checker")
    st.write("Upload seed images to check quality (Feature in progress).")

elif option == "☁️ Weather Predictor":
    st.header("☁️ Weather Predictor")
    st.write("Weather forecast feature coming soon.")
