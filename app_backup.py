import streamlit as st
from chatbot import get_response
from pdf_chat import read_pdf
import html

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IntelliAssist AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
/* -------------------- APP BACKGROUND -------------------- */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.08), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(14,165,233,.07), transparent 30%),
        #f7f9fc;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 28px;
    padding-bottom: 55px;
}

/* -------------------- SIDEBAR -------------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f1f5f9 0%, #eef2f7 100%);
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    color: #1e293b !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    color: #1e293b !important;
    background: #ffffff !important;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption p {
    color: #64748b !important;
}

.sidebar-section {
    color: #94a3b8 !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin: 24px 0 10px 0;
}

.history-card {
    background: rgba(255,255,255,.82);
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 11px 12px;
    margin: 7px 0;
    box-shadow: 0 4px 12px rgba(15,23,42,.035);
}

.history-card-title {
    color: #334155;
    font-size: 12.5px;
    font-weight: 650;
    line-height: 1.45;
}

.document-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border: 1px solid #dbe4ef;
    border-radius: 17px;
    padding: 16px;
    margin-top: 12px;
    box-shadow: 0 8px 22px rgba(15,23,42,.05);
}

.document-icon {
    font-size: 27px;
    margin-bottom: 7px;
}

.document-title {
    color: #1e293b;
    font-size: 13px;
    font-weight: 750;
    word-break: break-word;
}

.document-status {
    color: #16a34a !important;
    font-size: 11px;
    font-weight: 650;
    margin-top: 6px;
}

/* -------------------- HEADER -------------------- */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 8px;
}

.brand-area {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-icon {
    width: 56px;
    height: 56px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    box-shadow: 0 10px 25px rgba(79,70,229,.22);
}

.brand-title {
    font-size: 35px;
    font-weight: 850;
    letter-spacing: -1.2px;
    color: #172033;
}

.brand-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-top: 2px;
}

.online-status {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,.92);
    padding: 10px 16px;
    border-radius: 30px;
    border: 1px solid #e2e8f0;
    font-size: 13px;
    font-weight: 700;
    color: #475569;
    box-shadow: 0 6px 18px rgba(15,23,42,.05);
}

.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 0 4px rgba(34,197,94,.12);
}

/* -------------------- WELCOME -------------------- */
.welcome-card {
    margin-top: 18px;
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 58%, #eff6ff 100%);
    border: 1px solid #dfe7ff;
    box-shadow: 0 12px 35px rgba(15,23,42,.055);
}

.welcome-title {
    font-size: 27px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 8px;
}

.welcome-text {
    color: #64748b;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 20px;
}

.feature-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.feature-pill {
    flex: 1 1 180px;
    background: rgba(255,255,255,.78);
    border: 1px solid #dbe5f0;
    border-radius: 13px;
    padding: 13px 15px;
    color: #0f5da8;
    font-size: 13px;
    font-weight: 750;
    text-align: center;
}

/* -------------------- PDF CONTEXT -------------------- */
.pdf-context {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    color: #166534;
    border-radius: 13px;
    padding: 10px 14px;
    margin: 18px 0 10px 0;
    font-size: 13px;
    font-weight: 700;
}

.pdf-context-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
}

/* -------------------- CHAT -------------------- */
.chat-heading {
    font-size: 17px;
    font-weight: 800;
    color: #334155;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* Streamlit chat message containers */
[data-testid="stChatMessage"] {
    border-radius: 18px !important;
    margin: 10px 0 !important;
    padding: 16px 18px !important;
    border: 1px solid #e5eaf1 !important;
    box-shadow: 0 7px 22px rgba(15,23,42,.045) !important;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #eef2ff, #f8faff) !important;
    border-color: #d9defd !important;
}

/* Assistant message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #ffffff !important;
}

/* Message text */
[data-testid="stChatMessage"] p {
    color: #263246;
    font-size: 15px;
    line-height: 1.75;
}

/* -------------------- INPUT -------------------- */
[data-testid="stTextInput"] input {
    height: 58px !important;
    border-radius: 16px !important;
    border: 1px solid #dbe2ea !important;
    background: #ffffff !important;
    font-size: 15px !important;
    padding-left: 18px !important;
    box-shadow: 0 7px 22px rgba(15,23,42,.05);
    color: #1e293b !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,.10),
                0 8px 25px rgba(15,23,42,.06);
}

/* -------------------- BUTTONS -------------------- */
.stButton > button {
    min-height: 50px;
    border-radius: 14px;
    font-weight: 700;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    color: #334155;
    transition: all .2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #818cf8;
    color: #4f46e5;
    box-shadow: 0 8px 22px rgba(79,70,229,.12);
}

/* -------------------- COPY RESPONSE -------------------- */
.copy-label {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 700;
    margin: 4px 0 5px 4px;
}

/* st.code gives a reliable native Copy button */
[data-testid="stCodeBlock"] {
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
}

/* -------------------- FOOTER -------------------- */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 38px;
    padding-top: 18px;
    border-top: 1px solid #e2e8f0;
}

/* -------------------- MOBILE -------------------- */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 18px;
    }

    .brand-title {
        font-size: 26px;
    }

    .online-status {
        display: none;
    }

    .welcome-card {
        padding: 22px;
    }

    .welcome-title {
        font-size: 22px;
    }

    .feature-pill {
        flex-basis: 100%;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"],
        help="Upload a PDF document to ask questions about it.",
        key="pdf_uploader"
    )

    st.markdown('<div class="sidebar-section">Chat History</div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        for chat in reversed(st.session_state.chat_history[-10:]):
            safe_chat = html.escape(str(chat))
            st.markdown(
                f'<div class="history-card">'
                f'<div class="history-card-title">💬 {safe_chat}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("No previous questions yet.")

    st.markdown('<div class="sidebar-section">Document</div>', unsafe_allow_html=True)

    pdf_text = ""

    if uploaded_file is not None:
        pdf_text = read_pdf(uploaded_file)

        safe_name = html.escape(uploaded_file.name)

        st.markdown(
            f"""
            <div class="document-card">
                <div class="document-icon">📄</div>
                <div class="document-title">{safe_name}</div>
                <div class="document-status">● PDF ready for questions</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="
            color:#475569;
            font-size:13px;
            line-height:1.7;
            margin-top:16px;
        ">
            IntelliAssist AI helps you understand your PDF
            documents and get quick, AI-powered answers.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# MAIN HEADER
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(
        """
        <div class="app-header">
            <div class="brand-area">
                <div class="brand-icon">🤖</div>
                <div>
                    <div class="brand-title">IntelliAssist AI</div>
                    <div class="brand-subtitle">Your intelligent document assistant</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="online-status">
            <span class="status-dot"></span>
            AI Assistant Online
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# PDF CONTEXT INDICATOR
# =========================================================

if uploaded_file is not None:
    safe_name = html.escape(uploaded_file.name)
    st.markdown(
        f"""
        <div class="pdf-context">
            <span class="pdf-context-dot"></span>
            📄 Active PDF context: <strong>{safe_name}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">👋 Welcome to IntelliAssist AI</div>
            <div class="welcome-text">
                Upload a PDF and ask questions about your document.
                IntelliAssist AI will help you understand the content
                quickly and clearly.
            </div>

            <div class="feature-row">
                <div class="feature-pill">📄 PDF Analysis</div>
                <div class="feature-pill">💬 Smart Q&amp;A</div>
                <div class="feature-pill">⚡ Fast Answers</div>
                <div class="feature-pill">🔒 Document Based</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# CONVERSATION
# =========================================================

if st.session_state.messages:
    st.markdown(
        '<div class="chat-heading">💬 Conversation</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)

        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)

                # Native Streamlit code block provides a Copy button.
                st.markdown('<div class="copy-label">📋 Copy response</div>',
                            unsafe_allow_html=True)
                st.code(content, language=None, wrap_lines=True)

# =========================================================
# QUESTION INPUT
# =========================================================

st.markdown(
    '<div class="chat-heading">💭 Ask your question</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "",
    placeholder="Ask anything about your PDF...",
    label_visibility="collapsed",
    key="question_input"
)

# =========================================================
# ACTION BUTTONS
# =========================================================

c1, c2 = st.columns(2)

with c1:
    search = st.button(
        "🚀  Search",
        use_container_width=True,
        key="search_button"
    )

with c2:
    clear = st.button(
        "🗑️  Clear Chat",
        use_container_width=True,
        key="clear_button"
    )

# =========================================================
# CLEAR CHAT
# =========================================================

if clear:
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.rerun()

# =========================================================
# SEARCH / AI RESPONSE
# =========================================================

if search:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        clean_question = question.strip()

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": clean_question
        })

        st.session_state.chat_history.append(clean_question)

        # PDF based question
        if uploaded_file is not None:
            prompt = f"""
Answer ONLY from the uploaded PDF.

PDF CONTENT:
{pdf_text}

QUESTION:
{clean_question}

If the answer is not available in the PDF, reply exactly:

I couldn't find that information in the uploaded PDF.

Keep the answer clear, professional, and easy to understand.
"""
        else:
            prompt = clean_question

        # Loading animation while AI works
        with st.spinner("🤖 IntelliAssist AI is thinking..."):
            answer = get_response(prompt)

        # Add AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🤖 IntelliAssist AI &nbsp;•&nbsp;
        AI-Powered PDF Assistant
    </div>
    """,
    unsafe_allow_html=True
)