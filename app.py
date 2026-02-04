import streamlit as st
from openai import OpenAI
import base64

# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="AI Social Content Engine",
    page_icon="✨",
    layout="wide"
)

# ================= API KEY ================= #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= GLOBAL STYLE ================= #
st.markdown("""
<style>
.app-title {
    font-size: 34px;
    font-weight: 800;
}
.subtitle {
    color: #666;
    margin-bottom: 20px;
}
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR (LIKE REACT NAV) ================= #
st.sidebar.markdown("## ✨ AI Social Content Engine")
st.sidebar.caption("Creator Mode")

platform = st.sidebar.selectbox(
    "Choose Platform",
    [
        "Instagram",
        "LinkedIn",
        "X (Twitter)",
        "YouTube Shorts",
        "TikTok",
        "Facebook"
    ]
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

tone = st.sidebar.selectbox(
    "Tone",
    ["Professional", "Casual", "Motivational", "Funny", "Educational"]
)

goal = st.sidebar.selectbox(
    "Goal",
    ["Grow audience", "Engagement", "Sell product", "Build brand"]
)

language = st.sidebar.selectbox(
    "Language",
    ["English", "Hinglish", "Hindi"]
)

image_style = st.sidebar.selectbox(
    "Image Style",
    ["Minimal", "Aesthetic", "Dark", "Neon"]
)

# ================= MAIN AREA ================= #
st.markdown('<div class="app-title">🚀 Creator Content Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate platform-specific content packs — copy, paste, post.</div>',
    unsafe_allow_html=True
)

# ================= INPUT CARD ================= #
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Content Idea</div>', unsafe_allow_html=True)

niche = st.text_input(
    "Niche / Topic",
    placeholder="fitness, AI tools, personal branding, startup life"
)

st.markdown('</div>', unsafe_allow_html=True)

# ================= GENERATE ================= #
generate = st.button("✨ Generate Content Pack", use_container_width=True)

if generate:

    if not niche.strip():
        st.warning("Please enter a niche or topic.")
        st.stop()

    with st.spinner("Creating content..."):

        # -------- TEXT PROMPT (PLATFORM AWARE) -------- #
        text_prompt = f"""
Create content for {platform}.

Content type: {content_type}
Niche: {niche}
Tone: {tone}
Goal: {goal}
Language: {language}

Return a CLEAN, COPY-PASTE READY format.

Include:
- Hook
- Main content
- CTA (if applicable)
- Hashtags or tags (platform-appropriate)
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.8
        )

        text_content = text_response.choices[0].message.content

        # -------- IMAGE (ONLY FOR VISUAL PLATFORMS) -------- #
        image_bytes = None
        if platform in ["Instagram", "TikTok", "Facebook"]:

            image_prompt = f"""
Create a high-quality image for {platform}.
Topic: {niche}
Style: {image_style}
No text on image
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
    st.markdown("## 📦 Generated Content Pack")

    tabs = ["📝 Text"]
    if image_bytes:
        tabs.append("🖼️ Image")

    tab_objects = st.tabs(tabs)

    with tab_objects[0]:
        st.text_area(
            "Copy text",
            text_content,
            height=420
        )
        st.download_button(
            "Download Text",
            text_content,
            file_name=f"{platform.lower()}_content.txt"
        )

    if image_bytes:
        with tab_objects[1]:
            st.image(image_bytes, use_container_width=True)
            st.download_button(
                "Download Image",
                image_bytes,
                file_name=f"{platform.lower()}_image.png",
                mime="image/png"
            )

# ================= FOOTER ================= #
st.markdown("---")
st.caption("Creator-mode • Multi-platform • React-style UX • Built with Streamlit + OpenAI")
