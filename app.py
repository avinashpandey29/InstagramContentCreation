import streamlit as st
from openai import OpenAI
import base64

# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="AI Social Storytelling Engine",
    page_icon="✨",
    layout="wide"
)

# ================= API KEY ================= #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key not configured in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= STYLE ================= #
st.markdown("""
<style>
.title {
    font-size: 40px;
    font-weight: 800;
}
.subtitle {
    color: #666;
    font-size: 18px;
    margin-bottom: 25px;
}
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR NAV ================= #
st.sidebar.markdown("## ✨ Social Content Studio")
st.sidebar.caption("Emotion + Platform Creator Engine")

platform = st.sidebar.selectbox(
    "Choose Platform",
    ["Instagram", "LinkedIn", "X (Twitter)", "YouTube Shorts", "TikTok", "Facebook"]
)

content_type = st.sidebar.selectbox(
    "Content Type",
    {
        "Instagram": ["Post", "Reel", "Carousel"],
        "LinkedIn": ["Post", "Carousel"],
        "X (Twitter)": ["Thread"],
        "YouTube Shorts": ["Short Script"],
        "TikTok": ["Hook + Caption"],
        "Facebook": ["Post"]
    }[platform]
)

st.sidebar.markdown("---")

emotion = st.sidebar.selectbox(
    "Emotion Style",
    [
        "Motivational 💪",
        "Romantic ❤️",
        "Calm 🌿",
        "Nostalgic 🌙",
        "Sad-but-Hopeful 😌",
        "Self-love ✨",
        "Dreamy 🌅"
    ]
)

tone = st.sidebar.selectbox(
    "Writing Tone",
    ["Human & Relatable", "Poetic", "Minimal", "Funny", "Professional"]
)

goal = st.sidebar.selectbox(
    "Goal",
    ["Get followers", "More saves", "More shares", "Sell product", "Build personal brand"]
)

language = st.sidebar.selectbox(
    "Language",
    ["English", "Hinglish", "Hindi"]
)

image_style = st.sidebar.selectbox(
    "Image Mood Style",
    ["Cinematic", "Aesthetic", "Minimal", "Dark", "Soft & Warm"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built for creators who want emotional viral content.")

# ================= MAIN UI ================= #
st.markdown('<div class="title">🚀 AI Social Storytelling Engine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate emotionally powerful content + images people connect with.</div>',
    unsafe_allow_html=True
)

# ================= INPUT CARD ================= #
st.markdown('<div class="card">', unsafe_allow_html=True)
topic = st.text_input(
    "Enter your topic / feeling / niche",
    placeholder="Example: feeling lonely, gym motivation, startup struggle, travel memories..."
)
st.markdown('</div>', unsafe_allow_html=True)

# ================= GENERATE BUTTON ================= #
generate = st.button("✨ Generate Viral Content Pack", use_container_width=True)

# ================= GENERATION ================= #
if generate:

    if not topic.strip():
        st.warning("⚠️ Please enter a topic or feeling.")
        st.stop()

    with st.spinner("🧠 Creating emotionally viral content..."):

        # -------- TEXT PROMPT (EMOTION + PLATFORM) -------- #
        text_prompt = f"""
You are a viral social media storyteller.

Platform: {platform}
Content type: {content_type}

Emotion style: {emotion}
Tone: {tone}
Goal: {goal}
Language: {language}

Topic/Feeling: {topic}

Write like a real human.
Make people FEEL something.
Avoid generic marketing.

Return EXACTLY in this structure:

HOOK:
(one emotional scroll-stopper line)

CAPTION:
(3–5 short relatable lines)

HASHTAGS/TAGS:
(8–12 soft + trending hashtags)

CALL TO ACTION:
(short, natural, not salesy)

BONUS:
(1 extra line people will save/share)
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.9
        )

        text_content = text_response.choices[0].message.content

        # -------- IMAGE GENERATION (ONLY VISUAL PLATFORMS) -------- #
        image_bytes = None
        if platform in ["Instagram", "TikTok", "Facebook"]:

            image_prompt = f"""
Create a cinematic emotional social media image.

Emotion: {emotion}
Topic: {topic}

Mood style: {image_style}
Make it realistic, human, warm, scroll-stopping.
Like a viral Instagram aesthetic photo.

No text.
High quality.
"""

            image_response = client.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024"
            )

            image_bytes = base64.b64decode(
                image_response.data[0].b64_json
            )

    # ================= OUTPUT ================= #
    st.markdown("## 📦 Your Viral Content Pack")

    tabs = ["📝 Copy-Paste Text"]
    if image_bytes:
        tabs.append("🖼️ Emotional Image")

    tab_objects = st.tabs(tabs)

    # -------- TEXT TAB -------- #
    with tab_objects[0]:
        st.text_area(
            "Ready to copy & paste",
            text_content,
            height=420
        )

        st.download_button(
            "📥 Download Text Pack",
            text_content,
            file_name=f"{platform.lower()}_viral_pack.txt",
            use_container_width=True
        )

    # -------- IMAGE TAB -------- #
    if image_bytes:
        with tab_objects[1]:
            st.image(image_bytes, use_container_width=True)

            st.download_button(
                "⬇️ Download Image",
                image_bytes,
                file_name=f"{platform.lower()}_emotional_image.png",
                mime="image/png",
                use_container_width=True
            )

# ================= FOOTER ================= #
st.markdown("---")
st.caption("✨ Emotion-first content engine • Multi-platform • Creator SaaS Ready")
