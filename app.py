import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    .stApp {
        background-color: #FAF8FF;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem;
        max-width: 820px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2A1F47 0%, #1F1733 100%);
        border-right: 1px solid #3A2E5C;
    }
    [data-testid="stSidebar"] * {
        color: #E9E2FB !important;
    }
    [data-testid="stSidebar"] .sidebar-brand {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF !important;
        padding: 4px 0 18px 0;
        letter-spacing: -0.3px;
    }
    [data-testid="stSidebar"] .sidebar-section-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9C8FC2 !important;
        margin: 22px 0 10px 0;
    }
    [data-testid="stSidebar"] .history-item {
        padding: 9px 12px;
        border-radius: 10px;
        font-size: 13.5px;
        color: #D7CFF0 !important;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        border: 1px solid transparent;
        transition: background 0.15s ease, border-color 0.15s ease;
    }
    [data-testid="stSidebar"] .history-item:hover {
        background: #34294F;
        border-color: #4A3A73;
    }
    [data-testid="stSidebar"] .history-empty {
        font-size: 12.5px;
        color: #7D6FA3 !important;
        font-style: italic;
        padding: 4px 2px;
    }
    [data-testid="stSidebar"] .feature-row {
        font-size: 13px;
        color: #CFC5EE !important;
        padding: 3px 0;
    }
    [data-testid="stSidebar"] .model-badge {
        display: inline-block;
        background: #3A2E5C;
        color: #E9E2FB !important;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 600;
        margin-top: 4px;
    }
    [data-testid="stSidebar"] .stButton button {
        border-radius: 14px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 11px 16px !important;
        transition: transform 0.15s ease, opacity 0.15s ease !important;
        width: 100%;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-1px);
        opacity: 0.92;
    }
    [data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(1) button {
        background: linear-gradient(135deg, #8B5CF6, #6D4EA8) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #3A2E5C;
        margin: 10px 0;
    }

    /* Header */
    .app-header {
        text-align: center;
        padding: 12px 0 28px 0;
    }
    .app-header h1 {
        font-size: 34px;
        font-weight: 800;
        color: #1F1B2E;
        letter-spacing: -0.6px;
        margin-bottom: 6px;
    }
    .app-header p {
        font-size: 15px;
        color: #6B7280;
        font-weight: 400;
        margin: 0;
    }

    /* Chat bubbles */
    .msg-row {
        display: flex;
        margin-bottom: 18px;
        animation: fadeIn 0.25s ease;
    }
    .msg-row.user { justify-content: flex-end; }
    .msg-row.assistant { justify-content: flex-start; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .msg-bubble-wrap {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        max-width: 78%;
    }
    .msg-row.user .msg-bubble-wrap { flex-direction: row-reverse; }

    .avatar {
        width: 32px;
        height: 32px;
        min-width: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        margin-top: 2px;
    }
    .avatar.user-avatar {
        background: #EFE7FF;
        border: 1px solid #E9DDFC;
    }
    .avatar.ai-avatar {
        background: linear-gradient(135deg, #8B5CF6, #6D4EA8);
        color: #fff;
    }

    .bubble {
        padding: 13px 17px;
        border-radius: 22px;
        font-size: 15px;
        line-height: 1.55;
        color: #1F1B2E;
        transition: box-shadow 0.15s ease;
    }
    .bubble.user-bubble {
        background: #EFE7FF;
        border: 1px solid #E9DDFC;
        border-top-right-radius: 6px;
        box-shadow: 0 1px 4px rgba(109, 78, 168, 0.08);
    }
    .bubble.ai-bubble {
        background: #FFFFFF;
        border: 1px solid #E9DDFC;
        border-top-left-radius: 6px;
        box-shadow: 0 2px 10px rgba(109, 78, 168, 0.07);
    }
    .bubble.user-bubble:hover, .bubble.ai-bubble:hover {
        box-shadow: 0 4px 14px rgba(109, 78, 168, 0.14);
    }
    .bubble p { margin: 0 0 8px 0; }
    .bubble p:last-child { margin-bottom: 0; }

    .msg-meta {
        font-size: 11px;
        color: #6B7280;
        margin-top: 5px;
        padding: 0 4px;
    }
    .msg-row.user .msg-meta { text-align: right; }

    .grounding-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 11px;
        font-weight: 600;
        color: #6D4EA8;
        background: #F3EDFF;
        border: 1px solid #E9DDFC;
        padding: 4px 10px;
        border-radius: 999px;
        margin-top: 10px;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        margin: 0 auto;
        max-width: 820px;
        padding: 14px 16px 22px 16px;
        background: linear-gradient(180deg, rgba(250,248,255,0) 0%, #FAF8FF 28%);
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 26px !important;
        border: 1.5px solid #E9DDFC !important;
        background: #FFFFFF !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        box-shadow: 0 4px 18px rgba(109, 78, 168, 0.10) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 4px 22px rgba(139, 92, 246, 0.18) !important;
    }
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #8B5CF6, #6D4EA8) !important;
        border-radius: 50% !important;
        transition: transform 0.15s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.06);
    }

    .stSpinner > div {
        color: #6D4EA8 !important;
    }

    @media (max-width: 700px) {
        .msg-bubble-wrap { max-width: 92%; }
        .app-header h1 { font-size: 26px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="sidebar-brand">✨ Gemini AI Assistant</div>', unsafe_allow_html=True)

    new_chat_clicked = st.button("➕ New Chat", use_container_width=True)

    st.markdown('<div class="sidebar-section-label">Conversation History</div>', unsafe_allow_html=True)
    if "messages" in st.session_state and st.session_state.messages:
        user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        if user_msgs:
            for m in user_msgs[-8:][::-1]:
                preview = (m[:38] + "…") if len(m) > 38 else m
                st.markdown(f'<div class="history-item">💬 {preview}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="history-empty">No conversations yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="history-empty">No conversations yet.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Model</div>', unsafe_allow_html=True)
    st.markdown('<span class="model-badge">Gemini 2.5 Flash</span>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Features</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="feature-row">✔ Conversation Memory</div>
        <div class="feature-row">✔ Google Search Grounding</div>
        <div class="feature-row">✔ Streamlit</div>
        <div class="feature-row">✔ Gemini API</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    clear_chat_clicked = st.button("🗑 Clear Chat", use_container_width=True)

st.markdown(
    """
    <div class="app-header">
        <h1>Gemini AI Assistant</h1>
        <p>Intelligent conversations powered by Gemini 2.5 Flash with live Google Search.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "⚠️ GEMINI_API_KEY not found. Please create a `.env` file in the project root "
        "with the line:\n\nGEMINI_API_KEY=your_api_key_here"
    )
    st.stop()

@st.cache_resource(show_spinner=False)
def get_genai_client(_api_key):
    return genai.Client(api_key=_api_key)


try:
    client = get_genai_client(api_key)
except Exception as e:
    st.error(f"⚠️ Failed to initialize Gemini client: {e}")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

if new_chat_clicked or clear_chat_clicked:
    st.session_state.messages = []
    st.rerun()


def build_contents(history, latest_prompt):
    """Rebuild the full conversation as a list of Content objects from
    session_state history so the model retains memory across reruns,
    without relying on a stateful chat session object."""
    contents = []
    for m in history:
        role = "user" if m["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=m["content"])],
            )
        )
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=latest_prompt)],
        )
    )
    return contents


def render_message(role, content, timestamp=None, grounded=None):
    timestamp = timestamp or ""
    if role == "user":
        st.markdown(
            f"""
            <div class="msg-row user">
                <div class="msg-bubble-wrap">
                    <div class="avatar user-avatar">🧑</div>
                    <div>
                        <div class="bubble user-bubble"><p>{content}</p></div>
                        <div class="msg-meta">{timestamp}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        badge_html = ""
        if grounded is True:
            badge_html = '<div class="grounding-badge">🌐 Grounded with Google Search</div>'
        elif grounded is False:
            badge_html = '<div class="grounding-badge">🧠 Conversation Memory</div>'
        st.markdown(
            f"""
            <div class="msg-row assistant">
                <div class="msg-bubble-wrap">
                    <div class="avatar ai-avatar">✨</div>
                    <div>
                        <div class="bubble ai-bubble"><p>{content}</p>{badge_html}</div>
                        <div class="msg-meta">{timestamp}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


for msg in st.session_state.messages:
    render_message(
        msg["role"],
        msg["content"],
        timestamp=msg.get("timestamp", ""),
        grounded=msg.get("grounded"),
    )

user_prompt = st.chat_input("Message Gemini AI Assistant...")

if user_prompt is not None:
    cleaned_prompt = user_prompt.strip()

    if not cleaned_prompt:
        st.warning("⚠️ Please enter a valid message before sending.")
    else:
        user_timestamp = datetime.datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append(
            {"role": "user", "content": cleaned_prompt, "timestamp": user_timestamp}
        )
        render_message("user", cleaned_prompt, timestamp=user_timestamp)

        thinking_placeholder = st.empty()
        with thinking_placeholder.container():
            st.markdown(
                """
                <div class="msg-row assistant">
                    <div class="msg-bubble-wrap">
                        <div class="avatar ai-avatar">✨</div>
                        <div class="bubble ai-bubble"><p style="color:#6B7280;">Thinking...</p></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.spinner(""):
                grounded = False
                try:
                    grounding_tool = types.Tool(google_search=types.GoogleSearch())
                    generation_config = types.GenerateContentConfig(tools=[grounding_tool])
                    history_before_latest = st.session_state.messages[:-1]
                    contents = build_contents(history_before_latest, cleaned_prompt)
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=contents,
                        config=generation_config,
                    )
                    reply_text = response.text if response and response.text else (
                        "I'm sorry, I couldn't generate a response. Please try again."
                    )
                    try:
                        candidates = getattr(response, "candidates", None)
                        if candidates:
                            grounding_metadata = getattr(candidates[0], "grounding_metadata", None)
                            if grounding_metadata is not None:
                                grounded = True
                    except Exception:
                        grounded = False
                except Exception as e:
                    error_message = str(e).lower()
                    if "api key" in error_message or "permission" in error_message or "unauthorized" in error_message:
                        reply_text = "⚠️ Authentication error: Please check your GEMINI_API_KEY in the .env file."
                    elif "network" in error_message or "connection" in error_message or "timeout" in error_message:
                        reply_text = "⚠️ Network error: Unable to reach Gemini API. Please check your internet connection."
                    elif "quota" in error_message or "rate" in error_message or "resource_exhausted" in error_message:
                        reply_text = "⚠️ API quota exceeded or rate limited. Please try again later."
                    else:
                        reply_text = f"⚠️ An unexpected error occurred: {e}"
                    grounded = None

        thinking_placeholder.empty()

        ai_timestamp = datetime.datetime.now().strftime("%I:%M %p")
        render_message("assistant", reply_text, timestamp=ai_timestamp, grounded=grounded)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply_text,
                "timestamp": ai_timestamp,
                "grounded": grounded,
            }
        )
