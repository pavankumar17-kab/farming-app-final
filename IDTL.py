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
    :root { --forest:#143d2b; --leaf:#2e704d; --lime:#d9ec8b; --ink:#19291f; --muted:#748176; --line:#e6e9df; --paper:#f2f2e8; }
    .stApp { background:radial-gradient(ellipse at 88% 4%,rgba(164,194,125,.19),transparent 34%),radial-gradient(ellipse at 4% 72%,rgba(197,181,127,.13),transparent 39%),linear-gradient(135deg,#f3f3e9 0%,#edf1e3 52%,#f4f1e6 100%); color:var(--ink); }
    [data-testid="stHeader"] { background:transparent; }
    [data-testid="stToolbar"], #MainMenu, footer { visibility:hidden; }
    [data-testid="stAppViewContainer"] > .main .block-container { max-width:1120px; padding:1.2rem 2.2rem 3rem; }
    html, body, [class*="css"] { font-family:Inter,ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif; }
    h1,h2,h3 { color:var(--forest); letter-spacing:-.04em; }
    h1 { font-size:2rem !important; font-weight:750 !important; }
    h2 { font-size:1.45rem !important; font-weight:720 !important; }
    h3 { font-size:1.12rem !important; font-weight:700 !important; }
    [data-testid="stVerticalBlock"] { gap:.8rem; }
    .brandbar { display:flex; justify-content:space-between; align-items:center; padding:.35rem 0 1.05rem; }
    .brand { display:flex; gap:.65rem; align-items:center; font-weight:750; letter-spacing:-.03em; color:var(--forest); font-size:1.08rem; }
    .brandmark { display:grid; place-items:center; width:38px; height:38px; border-radius:13px; color:#eff8c8; background:var(--forest); font-size:1.25rem; }
    .brandmeta { color:var(--muted); font-size:.79rem; letter-spacing:.02em; }
    .hero { position:relative; overflow:hidden; display:flex; min-height:208px; align-items:center; justify-content:space-between; padding:2.15rem 2.4rem; border:1px solid #d6e2ce; border-radius:25px; color:var(--forest); background:linear-gradient(110deg,#e5eed6 0%,#edf2df 72%,#e2edcf 100%); box-shadow:0 14px 35px #173d2a0b; margin:.15rem 0 1.15rem; }
    .hero:after { content:''; position:absolute; width:300px; height:300px; right:-72px; top:-125px; border:1px solid #486c3b28; border-radius:50%; box-shadow:0 0 0 36px #486c3b0c,0 0 0 72px #486c3b08; }
    .hero-copy { position:relative; z-index:1; max-width:660px; }
    .eyebrow { color:#355b34; font-size:.72rem; letter-spacing:.16em; font-weight:750; text-transform:uppercase; margin-bottom:.7rem; }
    .hero h1 { color:var(--forest); margin:0; font-size:2.5rem !important; line-height:1.1; }
    .hero p { color:#344b3a; font-size:1rem; margin:.65rem 0 0; max-width:520px; line-height:1.55; }
    .hero-art { position:relative; z-index:1; width:190px; height:145px; flex:none; margin-left:1.2rem; }
    .section-kicker { color:#819083; text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; font-weight:750; margin:.4rem 0 .2rem; }
    div[role="radiogroup"] { gap:.55rem !important; flex-wrap:wrap; }
    div[role="radiogroup"] > label { padding:.68rem .95rem; border:1px solid #cbd8cb !important; border-radius:13px; background:#e8efe7 !important; color:#294635 !important; box-shadow:0 2px 8px #183b2508; transition:all .16s ease; }
    div[role="radiogroup"] > label, div[role="radiogroup"] > label * { color:#20372a !important; }
    [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stRadio"] [role="radiogroup"] label * { color:#172a21 !important; }
    div[role="radiogroup"] > label:hover { border-color:#789b7e !important; background:#dce9dc !important; color:var(--forest) !important; }
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) { border-color:#789748 !important; background:var(--lime) !important; color:#183b27 !important; box-shadow:0 5px 15px #143d2b20; }
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) p,
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) span,
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) div { color:#183b27 !important; }
    [data-testid="stRadio"] > label { display:none; }
    .stButton>button { border-radius:12px; font-weight:700; min-height:2.75rem; border-color:#dce4dc; }
    .stButton>button[kind="primary"] { background:var(--lime); border-color:#a9c66d; color:#183b27 !important; }
    .stButton>button[kind="primary"]:hover { background:#cce27b; border-color:#91ad59; color:#183b27 !important; }
    [data-testid="stForm"] { padding:1rem 1.1rem .75rem; border:1px solid var(--line); border-radius:18px; background:#fff; box-shadow:0 6px 20px #173d2a08; }
    [data-testid="stTextInput"] input { border:1px solid #dfe5dc; border-radius:12px; background:#fff; min-height:3rem; }
    [data-testid="stTextInput"] input:focus { border-color:#6f9b79; box-shadow:0 0 0 3px #2e704d17; }
    [data-testid="stFileUploader"] { border:1px dashed #c9d6c9; border-radius:16px; background:#fff; padding:.5rem; }
    [data-testid="stCameraInput"] button { border-radius:12px; }
    [data-testid="stCameraInput"] { border-radius:16px; }
    [data-testid="stAlert"] { border-radius:14px; }
    [data-testid="stImage"] img { border-radius:16px; }
    [data-testid="stCaptionContainer"] { color:var(--muted); }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color:#26392d !important; }
    [data-testid="stTextInput"] label, [data-testid="stTextInput"] label p { color:#20372a !important; }
    hr { border-color:var(--line); }
    @media(max-width:700px) { [data-testid="stAppViewContainer"] > .main .block-container { padding:.7rem 1rem 2rem; } .hero { padding:1.6rem; min-height:175px; } .hero-art { width:100px; opacity:.8; } .hero h1 { font-size:2rem !important; } }
    </style>
    """,
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "English": {
        "hero_title": "Grow with confidence.",
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
        "hero_title": "ಆತ್ಮವಿಶ್ವಾಸದಿಂದ ಬೆಳೆಸಿ.",
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
        <button id="speak-{key}" style="background:#e8efe7;color:#183b27;border:1px solid #cbd8cb;border-radius:10px;padding:10px 16px;font:600 15px sans-serif;cursor:pointer">🔊 {"ಕೇಳಿ" if lang_choice == "ಕನ್ನಡ" else "Read aloud"}</button>
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


header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown('<div class="brandbar"><div class="brand"><span class="brandmark">🌱</span><span>Agri-Smart AI<br><small class="brandmeta">Your farm, one step smarter</small></span></div></div>', unsafe_allow_html=True)
with header_right:
    lang_choice = st.selectbox("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ"], label_visibility="collapsed")
T = TRANSLATIONS[lang_choice]
st.markdown(
    f'''<section class="hero"><div class="hero-copy"><div class="eyebrow">{T["tag"]}</div><h1>{T["hero_title"]}</h1><p>{T["welcome"]}</p></div><svg class="hero-art" viewBox="0 0 220 170" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="169" cy="37" r="21" fill="#D9EC8B"/><path d="M4 119C39 88 62 93 92 111C118 127 143 125 216 82V170H4V119Z" fill="#75A66B"/><path d="M4 137C45 112 75 111 111 135C143 155 170 143 216 116V170H4V137Z" fill="#A9C979"/><path d="M24 170C53 148 86 143 121 170M75 170C101 150 131 151 157 170M132 170C151 159 174 158 195 170" stroke="#E5F1BF" stroke-width="3" stroke-linecap="round"/><path d="M114 110C114 91 125 76 144 69M115 108C102 91 91 87 79 89M114 109C123 92 138 85 156 87" stroke="#E7F1C2" stroke-width="5" stroke-linecap="round"/><path d="M142 71C141 57 152 49 167 51C166 65 158 72 142 71ZM81 89C69 76 73 62 86 55C98 66 97 79 81 89ZM155 87C158 73 171 67 184 72C181 86 170 91 155 87Z" fill="#D9EC8B"/></svg></section>''',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="section-kicker">{T["nav"]}</div>', unsafe_allow_html=True)
tool = st.radio(T["nav"], [T["chat"], T["disease"], T["seed"], T["weather"]], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)

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

