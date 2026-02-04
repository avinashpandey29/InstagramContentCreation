import streamlit as st
from openai import OpenAI
import base64

# ================== CONFIG ================== #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ================== API KEY ================== #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================== STYLE ================== #
st.markdown("""
<style>
.hero-title {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 20px;
    color: #666;
    margin-bottom: 40px;
}
.center-btn button {
    font-size: 20px;
    height: 3.2em;
}
.section {
    margin-top: 50px;
}
.metric {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
}
.metric h3 {
    margin-bottom: 5px;
}
.footer {
    margin-top: 60px;
    color: #888;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ================== HERO ================== #
st.markdown('<div class="hero-title">📸 AI Instagram Content Machine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Create ready-to-post Instagram content in under 60 seconds.</div>',
    unsafe_allow_html=True
)

# ================== WHO IT IS FOR ================== #
st.markdown("### Built for")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="metric"><h3>Creators</h3><p>Grow faster</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric"><h3>Businesses</h3><p>Sell more</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric"><h3>Agencies</h3><p>Scale content</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric"><h3>Solopreneurs</h3><p>Save time</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ================== DEMO SETUP (FIXED INPUTS) ================== #
st.markdown("### Live Demo (Investor View)")
st.write("This demo shows what a user gets with **one click**.")

DEMO_NICHE = "Fitness"
DEMO_TONE = "Motivational"
DEMO_GOAL = "Grow followers"
DEMO_LANGUAGE = "English"

st.info(
    f"**Niche:** {DEMO_NICHE}  |  "
    f"**Tone:** {DEMO_TONE}  |  "
    f"**Goal:** {DEMO_GOAL}"
)

# ================== CTA ================== #
st.markdown('<div class="center-btn">', unsafe_allow_html=True)
generate = st.button("🚀 Generate Demo Content Pack", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================== GENERATION ================== #
if generate:

    with st.spinner("Creating content…"):

        # -------- TEXT -------- #
        text_prompt = f"""
You are an Instagram growth expert.

Create ONE Instagram post.

Niche: {DEMO_NICHE}
Tone: {DEMO_TONE}
Goal: {DEMO_GOAL}
Language: {DEMO_LANGUAGE}

Return EXACTLY this format:

CAPTION:
(2–3 short lines)

HASHTAGS:
(8–10 hashtags)

REEL PLAN:
Scene 1 (0–3s):
Scene 2 (3–7s):
Scene 3 (7–12s):
"""

        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text_prompt}],
            temperature=0.7
        )

        text_content = text_response.choices[0].message.content

        # -------- IMAGE -------- #
        image_prompt = f"""
Create a high-quality Instagram image.
Niche: {DEMO_NICHE}
Style: modern, aesthetic, scroll-stopping
No text on image
"""

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )

        image_bytes = base64.b64decode(image_response.data[0].b64_json)

    # ================== OUTPUT ================== #
    st.markdown("## Demo Output")

    tab1, tab2 = st.tabs(["📝 Content", "🖼️ Image"])

    with tab1:
        st.text_area(
            "Ready-to-copy text",
            text_content,
            height=350
        )
        st.caption("This is exactly what a creator pastes into Instagram.")

    with tab2:
        st.image(image_bytes, use_container_width=True)
        st.caption("AI-generated post image.")

# ================== BUSINESS SECTION ================== #
st.markdown("---")
st.markdown("### Business Model")

b1, b2, b3 = st.columns(3)
with b1:
    st.markdown('<div class="metric"><h3>₹499/month</h3><p>Creator Plan</p></div>', unsafe_allow_html=True)
with b2:
    st.markdown('<div class="metric"><h3>Agency Plans</h3><p>Bulk content</p></div>', unsafe_allow_html=True)
with b3:
    st.markdown('<div class="metric"><h3>API / White-label</h3><p>Scalable</p></div>', unsafe_allow_html=True)

# ================== FOOTER ================== #
st.markdown(
    '<div class="footer">Live MVP • Deployed • Scalable • Investor-ready</div>',
    unsafe_allow_html=True
)
