import streamlit as st
from openai import OpenAI
import base64

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ---------------- API KEY ---------------- #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- HEADER ---------------- #
st.title("📸 AI Instagram Content Machine")
st.caption("100% copy-paste Instagram content packs — images, captions, hashtags & animations.")

st.markdown("---")

# ---------------- USER OPTIONS ---------------- #
st.markdown("## ⚙️ Content Options")

col1, col2, col3, col4 = st.columns(4)

with col1:
    niche = st.text_input("Niche", placeholder="fitness, finance, travel")

with col2:
    tone = st.selectbox("Tone", ["Professional", "Funny", "Motivational", "Casual"])

with col3:
    goal = st.selectbox("Goal", ["Grow followers", "Sell product", "Educate audience"])

with col4:
    language = st.selectbox("Language", ["English", "Hinglish", "Hindi"])

st.markdown("### 🔧 Advanced Controls")

c1, c2, c3, c4 = st.columns(4)

with c1:
    post_count = st.selectbox("Number of Posts", [1, 3, 5])

with c2:
    content_type = st.selectbox("Content Type", ["Single Post", "Carousel", "Reel"])

with c3:
    image_style = st.selectbox("Image Style", ["Minimal", "Neon", "Dark", "Aesthetic"])

with c4:
    hashtag_style = st.selectbox("Hashtag Style", ["Viral", "Niche-specific", "Mixed"])

cta_style = st.selectbox("CTA Style", ["Soft", "Direct", "No CTA"])

st.markdown("---")

# ---------------- GENERATE ---------------- #
generate = st.button("🚀 Generate Full Content Pack", use_container_width=True)

if generate:

    if not niche.strip():
        st.warning("Please enter a niche.")
        st.stop()

    # ================= TEXT PACK ================= #
    with st.spinner("🧠 Generating captions, hashtags & structure..."):

        text_prompt = f"""
Create {post_count} Instagram {content_type.lower()} content packs.

Niche: {niche}
Tone: {tone}
Goal: {goal}
Language: {language}
CTA Style: {cta_style}
Hashtag Style: {hashtag_style}

For EACH post provide this EXACT structure:

POST X
CAPTION:
(2–3 lines)

HASHTAGS:
(8–12 hashtags)

CAROUSEL SLIDES:
(if applicable, 5 short slides)

ANIMATION SCRIPT:
(scene-by-scene, slow & smooth)
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.8
        )

        text_content = text_response.choices[0].message.content

    st.markdown("## 📝 Copy-Paste Content Pack")
    st.text_area("Full Content (Organized)", text_content, height=500)

    st.download_button(
        "📥 Download Text Pack",
        data=text_content,
        file_name="instagram_content_pack.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")

    # ================= IMAGE ================= #
    with st.spinner("🖼️ Generating image..."):

        image_prompt = f"""
Create an Instagram image.
Niche: {niche}
Tone: {tone}
Style: {image_style}
Content type: {content_type}
No text on image
High quality, scroll-stopping
"""

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(image_response.data[0].b64_json)

    st.markdown("## 🖼️ Copy-Paste Image")
    st.image(image_bytes, use_container_width=True)

    st.download_button(
        "⬇️ Download Image",
        data=image_bytes,
        file_name="instagram_image.png",
        mime="image/png",
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built for creators • Fully copy-paste • Streamlit + OpenAI")
