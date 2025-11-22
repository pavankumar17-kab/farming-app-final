import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Agri-GPT", page_icon="🌱")

# ---------------------------------------------
# SIMPLE IMAGE-BASED DISEASE CHECKER (RULE-BASED)
# ---------------------------------------------
def detect_disease(image):
    # Convert to small size
    img = image.resize((50, 50))
    pixels = list(img.getdata())

    green_count = 0
    brown_black_count = 0
    yellow_count = 0

    for p in pixels:
        r, g, b = p
        if g > r and g > b:
            green_count += 1
        if r < 80 and g < 80 and b < 80:
            brown_black_count += 1
        if r > 150 and g > 150 and b < 80:
            yellow_count += 1

    if brown_black_count > 500:
        return "Fungal Disease", "Spray Mancozeb or Copper Oxychloride. Avoid over-watering. Improve air flow."
    if yellow_count > 500:
        return "Nutrient Deficiency", "Add Nitrogen or Iron fertilizer. Use compost or NPK 19-19-19."
    if green_count > 1000:
        return "Healthy", "Plant is healthy. Continue normal watering and sunlight."

    return "Uncertain", "Image unclear. Try uploading a close leaf photo."

# ---------------------------------------------
# SIMPLE SEED QUALITY CHECKER
# ---------------------------------------------
def check_seed_quality(image):
    img = image.resize((30, 30))
    pixels = list(img.getdata())

    dark = 0
    bright = 0

    for p in pixels:
        r, g, b = p
        if r < 80 and g < 80 and b < 80:
            dark += 1
        if r > 150 and g > 150 and b > 150:
            bright += 1

    if bright > dark:
        return "Good Seeds", "These seeds are likely healthy and suitable for sowing."
    else:
        return "Bad Seeds", "These seeds may be old or infected. Avoid planting."

# ---------------------------------------------
# WEATHER PREDICTOR (VERY SIMPLE)
# ---------------------------------------------
def predict_weather():
    tomorrow = datetime.now() + timedelta(days=1)
    day = tomorrow.day

    if day % 3 == 0:
        return "Rain Expected Tomorrow ☔", "Avoid spraying fertilizers or pesticides tomorrow."
    if day % 2 == 0:
        return "Hot Day Tomorrow 🌞", "Irrigate your plants early morning."
    return "Cloudy Weather Tomorrow ☁", "Good day for fertilizer application."

# ---------------------------------------------
# AGRI-GPT AGRICULTURE CHATBOT
# ---------------------------------------------
def agri_chatbot(question):
    question = question.lower()

    if "fertilizer" in question:
        return "Use NPK 19-19-19 for overall growth. For flowering plants use NPK 0-52-34."

    if "water" in question:
        return "Water early in the morning. Avoid wetting leaves to prevent fungal diseases."

    if "soil" in question:
        return "Use well-drained loamy soil mixed with compost for best plant growth."

    if "pest" in question:
        return "Use neem oil or soap spray every 7 days to control common pests."

    if "disease" in question:
        return "Upload an image of the leaf to diagnose the disease accurately."

    return "I am Agri-GPT. Ask me anything about farming, seeds, soil, water, fertilizer, or pests."

# ---------------------------------------------
# STREAMLIT UI
# ---------------------------------------------
st.title("🌱 Agri-GPT: AI Agriculture Assistant")

menu = st.radio("Select Option", 
                ["💬 Agriculture Chatbot", 
                 "🟢 Plant Disease Detector", 
                 "🌾 Seed Quality Checker",
                 "☁ Weather Predictor"])

# ---------------------------------------------
# CHATBOT
# ---------------------------------------------
if menu == "💬 Agriculture Chatbot":
    st.subheader("Ask anything about agriculture")
    q = st.text_input("Your Question:")
    if q:
        st.write("**Agri-GPT:**", agri_chatbot(q))

# ---------------------------------------------
# PLANT DISEASE DETECTOR
# ---------------------------------------------
elif menu == "🟢 Plant Disease Detector":
    img = st.camera_input("Take a photo of the plant leaf")
    if img:
        from PIL import Image
        image = Image.open(img)
        disease, solution = detect_disease(image)
        st.write(f"### Result: **{disease}**")
        st.write(f"### Solution: {solution}")

# ---------------------------------------------
# SEED QUALITY CHECKER
# ---------------------------------------------
elif menu == "🌾 Seed Quality Checker":
    img = st.camera_input("Take a photo of the seeds")
    if img:
        from PIL import Image
        image = Image.open(img)
        quality, advice = check_seed_quality(image)
        st.write(f"### Seed Quality: **{quality}**")
        st.write(f"### Advice: {advice}")

# ---------------------------------------------
# WEATHER
# ---------------------------------------------
elif menu == "☁ Weather Predictor":
    result, tip = predict_weather()
    st.write(f"### {result}")
    st.write(f"### Tip: {tip}")
