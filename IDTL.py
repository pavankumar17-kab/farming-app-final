import json
import os

import google.generativeai as genai
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from streamlit_mic_recorder import speech_to_text


st.set_page_config(page_title="Agri-Smart AI", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    :root { --green: #176b45; --deep: #103f2d; --mint: #eaf5ee; --ink: #172a21; }
    .stApp { background: linear-gradient(180deg,#f7fbf7 0%,#f4f7f2 100%); color:var(--ink); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stSidebar"] { background:#103f2d; }
    [data-testid="stSidebar"] * { color:#f5fff8 !important; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    h1,h2,h3 { font-family:'Manrope',sans-serif; color:var(--deep); letter-spacing:-.035em; }
    .hero { padding:2rem 2.2rem; border-radius:24px; color:white; background:linear-gradient(115deg,#103f2d,#1d7650 65%,#5b9b58); box-shadow:0 18px 50px #174a3022; margin-bottom:1.2rem; }
    .hero h1 { color:white; margin:0 0 .25rem; font-size:2.3rem; }
    .hero p { color:#e5f5e9; font-size:1.04rem; margin:.25rem 0 0; }
    .tag { display:inline-block; padding:.35rem .7rem; border:1px solid #ffffff55; border-radius:20px; font-size:.8rem; margin-bottom:.75rem; }
    .stButton>button { border-radius:12px; font-weight:700; min-height:2.8rem; }
    .stButton>button[kind="primary"] { background:var(--green); border-color:var(--green); }
    [data-testid="stChatMessage"] { border:1px solid #e3ece4; border-radius:18px; background:#fff; }
    [data-testid="stFileUploader"] { border-radius:16px; }
    .hint { color:#53675b; font-size:.92rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "English": {
        "welcome": "Your smart companion for healthier crops and better decisions.",
        "tag": "FARMING, MADE SMARTER",
        "language": "Language",
        "nav": "Choose a tool",
        "chat": "💬 Ask Agri-Smart",
        "disease": "🌿 Plant health",
        "seed": "🌾 Seed check",
        "weather": "☀️ Weather guide",
        "chat_title": "Ask your farming question",
        "chat_help": "Type a question or record it. You can ask in English or Kannada.",
        "record": "Speak your question",
        "record_hint": "Allow microphone access in your browser when prompted.",
        "input": "What would you like help with?",
        "placeholder": "For example: How often should I water tomato plants?",
        "send": "Get farming advice",
        "answer": "Agri-Smart advice",
        "disease_title": "Check a plant leaf",
        "disease_help": "Upload a clear leaf photo or take one with your camera.",
        "upload_leaf": "Choose a leaf photo",
        "camera": "Take a photo",
        "identify": "Analyze leaf",
        "seed_title": "Check seed quality",
        "seed_help": "Upload a clear photo of the seeds you want to inspect.",
        "upload_seed": "Choose a seed photo",
        "analyze_seed": "Analyze seeds",
        "weather_title": "A quick weather based guide",
        "weather_help": "Choose the conditions you see for a general farming reminder.",
        "season": "Season",
        "sky": "Current sky",
        "advice": "Farming reminder",
        "busy": "Preparing your answer...",
        "thinking": "Analyzing your photo...",
        "error_key": "Add GOOGLE_API_KEY in your Streamlit secrets to enable AI features.",
    },
    "ಕನ್ನಡ": {
        "welcome": "ಆರೋಗ್ಯಕರ ಬೆಳೆ ಮತ್ತು ಉತ್ತಮ ನಿರ್ಧಾರಗಳಿಗೆ ನಿಮ್ಮ ಸ್ಮಾರ್ಟ್ ಸಹಾಯಕ.",
        "tag": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",
        "language": "ಭಾಷೆ",
        "nav": "ಸಾಧನ ಆಯ್ಕೆಮಾಡಿ",
        "chat": "💬 ಕೃಷಿ ಪ್ರಶ್ನೆ ಕೇಳಿ",
        "disease": "🌿 ಸಸ್ಯ ಆರೋಗ್ಯ",
        "seed": "🌾 ಬೀಜ ಪರೀಕ್ಷೆ",
        "weather": "☀️ ಹವಾಮಾನ ಸಲಹೆ",
        "chat_title": "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆ ಕೇಳಿ",
        "chat_help": "ಪ್ರಶ್ನೆಯನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಧ್ವನಿಯಲ್ಲಿ ಹೇಳಿ. ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಕೇಳಬಹುದು.",
        "record": "ಪ್ರಶ್ನೆಯನ್ನು ಮಾತನಾಡಿ",
        "record_hint": "ಬ್ರೌಸರ್ ಕೇಳಿದಾಗ ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ನೀಡಿ.",
        "input": "ನಿಮಗೆ ಯಾವ ಸಹಾಯ ಬೇಕು?",
        "placeholder": "ಉದಾಹರಣೆ: ಟೊಮೇಟೊ ಗಿಡಕ್ಕೆ ಎಷ್ಟು ಬಾರಿ ನೀರು ಹಾಕಬೇಕು?",
        "send": "ಕೃಷಿ ಸಲಹೆ ಪಡೆಯಿರಿ",
        "answer": "ಕೃಷಿ ಸಲಹೆ",
        "disease_title": "ಎಲೆಯ ಆರೋಗ್ಯ ಪರಿಶೀಲಿಸಿ",
        "disease_help": "ಸ್ಪಷ್ಟವಾದ ಎಲೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಕ್ಯಾಮೆರಾದಲ್ಲಿ ತೆಗೆಯಿರಿ.",
        "upload_leaf": "ಎಲೆಯ ಫೋಟೋ ಆಯ್ಕೆಮಾಡಿ",
        "camera": "ಫೋಟೋ ತೆಗೆಯಿರಿ",
        "identify": "ಎಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "seed_title": "ಬೀಜದ ಗುಣಮಟ್ಟ ಪರಿಶೀಲಿಸಿ",
        "seed_help": "ಪರಿಶೀಲಿಸಬೇಕಾದ ಬೀಜಗಳ ಸ್ಪಷ್ಟವಾದ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ.",
        "upload_seed": "ಬೀಜದ ಫೋಟೋ ಆಯ್ಕೆಮಾಡಿ",
        "analyze_seed": "ಬೀಜಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "weather_title": "ಹವಾಮಾನಕ್ಕೆ ತಕ್ಕ ಸರಳ ಸಲಹೆ",
        "weather_help": "ನೀವು ಗಮನಿಸಿದ ಹವಾಮಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "season": "ಋತು",
        "sky": "ಈಗಿನ ಆಕಾಶ",
        "advice": "ಕೃಷಿ ನೆನಪಿನ ಸಲಹೆ",
        "busy": "ಉತ್ತರ ಸಿದ್ಧವಾಗುತ್ತಿದೆ...",
        "thinking": "ಫೋಟೋ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "error_key": "AI ವೈಶಿಷ್ಟ್ಯಗಳಿಗಾಗಿ Streamlit secrets ನಲ್ಲಿ GOOGLE_API_KEY ಸೇರಿಸಿ.",
    },
}


def get_model():
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    except Exception:
        api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.error(T["error_key"])
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def speak_button(text, lang_choice, key):
    """Keep button and speech code in one iframe; separate Streamlit frames cannot call each other."""
    lang_code = "kn-IN" if lang_choice == "ಕನ್ನಡ" else "en-US"
    safe_text = json.dumps(text)
    safe_lang = json.dumps(lang_code)
    components.html(
        f"""<!doctype html><meta charset="utf-8">
        <button id="speak-{key}" style="background:#176b45;color:white;border:0;border-radius:10px;padding:10px 16px;font:600 15px sans-serif;cursor:pointer">🔊 {"ಕೇಳಿ" if lang_choice == "ಕನ್ನಡ" else "Read aloud"}</button>
        <script>
        (() => {{
          const button = document.getElementById("speak-{key}");
          button.addEventListener("click", () => {{
            if (!("speechSynthesis" in window)) {{ button.textContent = "Speech playback is not supported in this browser"; return; }}
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance({safe_text});
            utterance.lang = {safe_lang};
            const voices = window.speechSynthesis.getVoices();
            const voice = voices.find(v => v.lang.toLowerCase().startsWith({safe_lang}.slice(0,2)));
            if (voice) utterance.voice = voice;
            window.speechSynthesis.speak(utterance);
          }});
        }})();
        </script>""",
        height=52,
    )


lang_choice = st.sidebar.selectbox("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ"])
T = TRANSLATIONS[lang_choice]
st.markdown(
    f'<div class="hero"><span class="tag">{T["tag"]}</span><h1>🌱 Agri-Smart AI</h1><p>{T["welcome"]}</p></div>',
    unsafe_allow_html=True,
)

tool = st.radio(T["nav"], [T["chat"], T["disease"], T["seed"], T["weather"]], horizontal=True, label_visibility="collapsed")
st.divider()

if tool == T["chat"]:
    st.header(T["chat_title"])
    st.caption(T["chat_help"])
    st.markdown(f"**🎙️ {T['record']}**")
    st.caption(T["record_hint"])
    voice_lang = "kn-IN" if lang_choice == "ಕನ್ನಡ" else "en-US"
    voice_input = speech_to_text(
        language=voice_lang,
        start_prompt="🔴 Record / ರೆಕಾರ್ಡ್",
        stop_prompt="⏹️ Stop / ನಿಲ್ಲಿಸಿ",
        just_once=True,
        key=f"speech_{voice_lang}",
    )
    if voice_input:
        st.info(f"🗣️ {voice_input}")
    with st.form("question_form", clear_on_submit=False):
        text_input = st.text_input(T["input"], placeholder=T["placeholder"])
        submitted = st.form_submit_button(T["send"], type="primary", use_container_width=True)
    if submitted:
        question = (voice_input or text_input or "").strip()
        if not question:
            st.warning(T["input"])
        else:
            model = get_model()
            if model:
                prompt = (
                    "You are Agri-Smart AI, a careful agriculture assistant for Indian farmers. "
                    "Answer accurately, simply, and with practical steps. Reply in the same language as the user's question (Kannada questions in natural Kannada; English questions in English), "
                    f"regardless of the interface language. The selected interface language is {lang_choice}. "
                    "Do not invent live weather, prices, diagnoses, or local government schemes. State uncertainty and ask for location/crop details when needed. "
                    f"User question: {question}"
                )
                with st.spinner(T["busy"]):
                    try:
                        response = model.generate_content(prompt)
                        answer = (response.text or "").strip()
                        if answer:
                            st.markdown(f"### {T['answer']}")
                            st.markdown(answer)
                            answer_lang = "ಕನ್ನಡ" if any("\u0c80" <= ch <= "\u0cff" for ch in answer) else "English"
                            speak_button(answer, answer_lang, "chat-answer")
                        else:
                            st.error("The model returned an empty response. Please try again.")
                    except Exception as exc:
                        st.error(f"Unable to get an answer: {exc}")

elif tool == T["disease"]:
    st.header(T["disease_title"])
    st.caption(T["disease_help"])
    left, right = st.columns([3, 2])
    with left:
        uploaded = st.file_uploader(T["upload_leaf"], type=["jpg", "jpeg", "png"], key="leaf_upload")
    with right:
        camera = st.camera_input(T["camera"], key="leaf_camera")
    photo = uploaded or camera
    if photo:
        image = Image.open(photo).convert("RGB")
        st.image(image, caption=T["upload_leaf"], use_container_width=True)
        if st.button(T["identify"], type="primary"):
            model = get_model()
            if model:
                language_instruction = "Write the full response in Kannada." if lang_choice == "ಕನ್ನಡ" else "Write the response in English."
                with st.spinner(T["thinking"]):
                    try:
                        answer = model.generate_content([
                            "Inspect this plant image. If it is not a clear plant photo, say so. Otherwise describe visible symptoms, give likely causes with uncertainty, and suggest safe next steps. Do not claim certainty from an image alone. " + language_instruction,
                            image,
                        ]).text or ""
                        st.markdown(answer)
                        speak_button(answer, lang_choice, "leaf-answer")
                    except Exception as exc:
                        st.error(f"Unable to analyze the photo: {exc}")

elif tool == T["seed"]:
    st.header(T["seed_title"])
    st.caption(T["seed_help"])
    photo = st.file_uploader(T["upload_seed"], type=["jpg", "jpeg", "png"], key="seed_upload")
    if photo:
        image = Image.open(photo).convert("RGB")
        st.image(image, caption=T["upload_seed"], use_container_width=True)
        if st.button(T["analyze_seed"], type="primary"):
            model = get_model()
            if model:
                language_instruction = "Write the full response in Kannada." if lang_choice == "ಕನ್ನಡ" else "Write the response in English."
                with st.spinner(T["thinking"]):
                    try:
                        answer = model.generate_content([
                            "Inspect this seed photo. Explain visible quality indicators and limitations; only estimate the count if individual seeds are clearly visible. Do not claim a reliable germination test from a photo. " + language_instruction,
                            image,
                        ]).text or ""
                        st.markdown(answer)
                        speak_button(answer, lang_choice, "seed-answer")
                    except Exception as exc:
                        st.error(f"Unable to analyze the photo: {exc}")

else:
    st.header(T["weather_title"])
    st.caption(T["weather_help"])
    if lang_choice == "ಕನ್ನಡ":
        seasons, skies = ["ಬೇಸಿಗೆ", "ಮುಂಗಾರು", "ಚಳಿಗಾಲ"], ["ಬಿಸಿಲು", "ಮೋಡ", "ಮಳೆ"]
    else:
        seasons, skies = ["Summer", "Monsoon", "Winter"], ["Sunny", "Cloudy", "Rainy"]
    col1, col2 = st.columns(2)
    season = col1.selectbox(T["season"], seasons)
    sky = col2.selectbox(T["sky"], skies)
    st.subheader(T["advice"])
    if sky in ("Rainy", "ಮಳೆ"):
        st.warning("ಮಳೆಯ ಸಮಯದಲ್ಲಿ ಸಿಂಪಡಣೆ ತಪ್ಪಿಸಿ; ಮಳೆ ನಿಂತ ನಂತರ ಲೇಬಲ್ ಸೂಚನೆ ನೋಡಿ." if lang_choice == "ಕನ್ನಡ" else "Avoid spraying during rain; check the product label after rain passes.")
    elif season in ("Summer", "ಬೇಸಿಗೆ") and sky in ("Sunny", "ಬಿಸಿಲು"):
        st.info("ಬಿಸಿಲು ಕಡಿಮೆಯಿರುವ ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಸಂಜೆ ನೀರು ಹಾಕಿ; ಮಣ್ಣಿನ ತೇವಾಂಶ ಪರಿಶೀಲಿಸಿ." if lang_choice == "ಕನ್ನಡ" else "Water during cooler morning or evening hours and check soil moisture first.")
    elif season in ("Monsoon", "ಮುಂಗಾರು"):
        st.info("ಹೊಲದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು ಎಲೆಗಳ ಮೇಲೆ ರೋಗದ ಲಕ್ಷಣ ಗಮನಿಸಿ." if lang_choice == "ಕನ್ನಡ" else "Check field drainage and monitor leaves for signs of disease.")
    else:
        st.success("ನಿಮ್ಮ ಬೆಳೆಗೆ ತಕ್ಕ ನೀರು ಮತ್ತು ಆರೈಕೆ ವೇಳಾಪಟ್ಟಿಯನ್ನು ಮುಂದುವರಿಸಿ." if lang_choice == "ಕನ್ನಡ" else "Continue a watering and care schedule suited to your crop.")

st.caption("🌱 AI suggestions are general guidance. Confirm important crop treatments with a local agriculture officer or KVK.")

