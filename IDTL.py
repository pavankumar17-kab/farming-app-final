import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# --- 1. SETUP ---
st.set_page_config(page_title="Agri-AI Assistant", page_icon="🌱")

# ------------------------------------------------------------------
# CRITICAL: PASTE YOUR GOOGLE API KEY BELOW
# Delete "YOUR_API_KEY" and paste your real key inside the quotes.
GOOGLE_API_KEY = "YOUR_API_KEY" 
# ------------------------------------------------------------------

# Configure the AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Key Error: {e}")

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

# FEATURE 1: CHATBOT
if option == "💬 Agriculture Chatbot":
    st.header("💬 Agri-GPT Chatbot")
    st.markdown("Ask any question about farming, crops, or fertilizers.")

    # --- VOICE INPUT SECTION ---
    st.write("---")
    st.write("🎤 **Option 1: Speak your question**")
    
    # The Voice Button
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
    # Logic: If voice was used, use that. If not, use the text box.
    user_question = text_from_voice if text_from_voice else text_from_box

    # --- SEND TO AI ---
    if user_question:
        with st.spinner("Agri-GPT is thinking..."):
            try:
                # Direct prompt to the AI
                prompt = (
                    f"You are an expert farmer and agricultural scientist. "
                    f"Answer this question simply and clearly for a farmer: {user_question}"
                )
                
                response = model.generate_content(prompt)
                
                # Display Answer
                st.markdown("### 💡 Answer:")
                st.write(response.text)
                
            except Exception as e:
                # If the key is wrong, this error will show
                st.error(f"⚠️ Error: The AI could not reply. Check your API Key. Details: {e}")

# FEATURE 2: DISEASE DETECTOR
elif option == "🟢 Plant Disease Detector":
    st.header("🟢 Plant Disease Detector")
    st.info("Upload a photo of a plant leaf to detect diseases.")
    st.file_uploader("Upload Leaf Image", type=['jpg', 'png', 'jpeg'])

# FEATURE 3: SEED CHECKER
elif option == "🌾 Seed Quality Checker":
    st.header("🌾 Seed Quality Checker")
    st.write("Upload seed images to check quality (Feature in progress).")

# FEATURE 4: WEATHER
elif option == "☁️ Weather Predictor":
    st.header("☁️ Weather Predictor")
    st.write("Weather forecast feature coming soon.")
