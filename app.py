import streamlit as st
from openai import OpenAI
import base64

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ---------------- SIMPLE CSS (SAFE) ---------------- #
st.markdown("""
<style>
.hero {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}
.subhero {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}
.card {
    background: #fafafa;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.generate-btn button {
    font-size: 18px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- API KEY ---------------- #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- HERO ---------------- #
st.markdown('<div class="hero">📸 AI Instagram Content Machine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subhero">Create captions, images, slides & reels — 100% copy-paste ready.</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT CARD ---------------- #
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🧠 Content Setup")

c1, c2, c3 = st.columns(3)
with c1:
    niche = st.text_input("Niche", placeholder="fitness, finance, travel")
with c2:
    tone = st.selectbox("Tone", ["Professional", "Funny", "Motivational", "Casual"])
with c3:
    goal = st.selectbox("Goal", ["Grow followers", "Sell product", "Educate audience"])

language = st.radio("Language", ["English", "Hinglish", "Hindi"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ADVANCED OPTIONS ---------------- #
with st.expander("⚙️ Advanced Options"):
    a1, a2, a3 = st.columns(3)
    with a1:
        post_count = st.selectbox("Posts", [1, 3, 5])
    with a2:
        content_type = st.selectbox("Content Type", ["Post", "Carousel", "Reel"])
    with a3:
        image_style = st.selectbox("Image Style", ["Minimal", "Neon", "Dark", "Aesthetic"])

    hashtag_style = st.selectbox("Hashtag Style", ["Viral", "Niche", "Mixed"])
    cta_style = st.selectbox("CTA Style", ["Soft", "Direct", "None"])

# ---------------- GENERATE BUTTON ---------------- #
st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
generate = st.button("🚀 Generate Content Pack", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GENERATION ---------------- #
if generate:

    if not niche.strip():
        st.warning("Please enter a niche.")
        st.stop()

    with st.spinner("✨ Creating your Instagram content..."):

        prompt = f"""
Create {post_count} Instagram {content_type.lower()} content packs.

Niche: {niche}
Tone: {tone}
Goal: {goal}
Language: {language}
Hashtag Style: {hashtag_style}
CTA Style: {cta_style}

For EACH post include:
CAPTION:
HASHTAGS:
CAROUSEL SLIDES (if applicable):
ANIMATION SCRIPT:
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        text_content = text_response.choices[0].message.content

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=f"Instagram image for {niche}, {image_style} style, no text",
            size="1024x1024"
        )

        image_bytes = base64.b64decode(image_response.data[0].b64_json)

    # ---------------- OUTPUT TABS ---------------- #
    tab1, tab2, tab3 = st.tabs(["📝 Text", "🖼️ Image", "🎬 Animation"])

    with tab1:
        st.text_area("Copy text content", text_content, height=450)
        st.download_button("Download Text", text_content, "content.txt")

    with tab2:
        st.image(image_bytes, use_container_width=True)
        st.download_button("Download Image", image_bytes, "image.png")

    with tab3:
        st.markdown("Animation steps are included in the text section above.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built for creators • Clean UI • Copy-paste workflow")
