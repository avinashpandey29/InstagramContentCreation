import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Instagram Content Machine",
    page_icon="📸",
    layout="wide"
)

# ---------------- BASIC UI (ALWAYS RENDER) ---------------- #
st.title("📸 AI Instagram Content Machine")
st.caption("Create viral Instagram content in seconds — no thinking, no stress.")

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("🔐 OpenAI API Key")

user_api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    type="password",
    help="Used only for this session. Not stored."
)

# ---------------- API KEY RESOLUTION ---------------- #
api_key = None

if user_api_key:
    api_key = user_api_key
elif "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

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

# ---------------- VALIDATION MESSAGE ---------------- #
if not api_key:
    st.warning("⚠️ Please add your OpenAI API key in the sidebar or Streamlit Secrets.")

# ---------------- GENERATE BUTTON ---------------- #
generate = st.button(
    "🚀 Generate Instagram Content",
    use_container_width=True,
    disabled=not api_key
)

# ---------------- GENERATION ---------------- #
if generate:

    if not niche.strip():
        st.warning("Please enter a niche.")
        st.stop()

    client = OpenAI(api_key=api_key)

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
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        content = response.choices[0].message.content

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
st.caption("Built with ❤️ using Streamlit & OpenAI")
