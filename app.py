import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ---------------- LOAD API KEY ---------------- #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- HEADER ---------------- #
st.title("📸 AI Instagram Content Machine")
st.caption("Create content, images, and reel animations — copy & paste ready.")

st.markdown("---")

# ---------------- INPUTS ---------------- #
st.markdown("### ✍️ Content Settings")

col1, col2, col3 = st.columns(3)

with col1:
    niche = st.text_input("Niche", placeholder="fitness, finance, travel")

with col2:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Funny", "Motivational", "Casual"]
    )

with col3:
    goal = st.selectbox(
        "Goal",
        ["Grow followers", "Sell product", "Educate audience"]
    )

language = st.radio(
    "Language",
    ["English", "Hinglish", "Hindi"],
    horizontal=True
)

st.markdown("---")

# ---------------- GENERATE BUTTON ---------------- #
generate = st.button(
    "🚀 Generate Instagram Content",
    use_container_width=True
)

# ---------------- MAIN GENERATION ---------------- #
if generate:

    if not niche.strip():
        st.warning("⚠️ Please enter a niche.")
        st.stop()

    # ---------- TEXT CONTENT ---------- #
    with st.spinner("🧠 Generating captions & hashtags..."):

        text_prompt = f"""
You are an expert Instagram content strategist.

Create 5 Instagram post ideas.

Niche: {niche}
Tone: {tone}
Goal: {goal}
Language: {language}

For EACH post include:
- Hook (1 strong line)
- Caption (2–3 short lines)
- Hashtags (5–8)
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.8
        )

        text_content = text_response.choices[0].message.content

    st.markdown("## ✨ Captions & Hashtags")
    st.text_area(
        "Copy–paste content",
        text_content,
        height=350
    )

    st.download_button(
        "📥 Download Captions",
        data=text_content,
        file_name="instagram_captions.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")

    # ---------- IMAGE GENERATION ---------- #
    with st.spinner("🖼️ Generating Instagram image..."):

        image_prompt = f"""
Create a high-quality Instagram image.
Niche: {niche}
Tone: {tone}
Style: modern, aesthetic, clean
Mood: scroll-stopping
No text on image
"""

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )

        image_url = image_response.data[0].url

    st.markdown("## 🖼️ AI Image (Post / Reel Cover)")
    st.image(image_url, use_container_width=True)
    st.markdown(
        f"[⬇️ Download Image]({image_url})",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------- SLIDE CONTENT ---------- #
    with st.spinner("🧩 Creating carousel slide text..."):

        slide_prompt = f"""
Create Instagram carousel slide content.

Niche: {niche}
Tone: {tone}
Goal: {goal}

Create 5 slides:
Slide 1: Strong hook
Slide 2: Problem
Slide 3: Insight
Slide 4: Solution
Slide 5: CTA

Each slide must be under 12 words.
"""

        slide_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": slide_prompt}],
            temperature=0.7
        )

        slide_content = slide_response.choices[0].message.content

    st.markdown("## 🧩 Carousel Slide Text (Canva Ready)")
    st.text_area(
        "Copy each slide into Canva",
        slide_content,
        height=250
    )

    st.markdown("---")

    # ---------- ANIMATION SCRIPT ---------- #
    with st.spinner("🎬 Creating slow reel animation steps..."):

        animation_prompt = f"""
Create a slow Instagram Reel animation plan.

Niche: {niche}
Tone: {tone}

Duration: 10–12 seconds
Style: smooth, aesthetic, calm

Provide:
Scene number
Time range
Text on screen
Animation type (fade, slide up, zoom)
"""

        animation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": animation_prompt}],
            temperature=0.7
        )

        animation_content = animation_response.choices[0].message.content

    st.markdown("## 🎬 Slow Animation Script (CapCut / Canva)")
    st.text_area(
        "Copy–paste animation steps",
        animation_content,
        height=300
    )

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built with ❤️ for creators | Streamlit + OpenAI")