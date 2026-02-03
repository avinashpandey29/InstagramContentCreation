import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ---------------- LOAD API KEY FROM SECRETS ---------------- #
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key is not configured. Please contact the app owner.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- HEADER ---------------- #
st.title("📸 AI Instagram Content Machine")
st.caption("Create viral Instagram content in seconds — no thinking, no stress.")

# ---------------- INPUT SECTION ---------------- #
st.markdown("### ✍️ Content Details")

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

# ---------------- GENERATION ---------------- #
if generate:

    if not niche.strip():
        st.warning("⚠️ Please enter a niche.")
        st.stop()

    with st.spinner("🧠 AI is crafting your content..."):

        prompt = f"""
You are an expert Instagram content strategist.

Create 5 Instagram post ideas.

Niche: {niche}
Tone: {tone}
Goal: {goal}
Language: {language}

For EACH post include:
- Hook (1 powerful line)
- Caption (2–3 short lines)
- Hashtags (5–8 relevant hashtags)

Make it engaging, scroll-stopping, and practical.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        content = response.choices[0].message.content

    # ---------------- OUTPUT ---------------- #
    st.markdown("### ✨ Generated Instagram Content")

    st.text_area(
        "Copy your content",
        content,
        height=420
    )

    st.download_button(
        "📥 Download as TXT",
        data=content,
        file_name="instagram_content.txt",
        mime="text/plain",
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("Built with ❤️ using AI")