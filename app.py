import streamlit as st
from chatbot import get_response
from pdf_chat import read_pdf

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

    # ================================
# CHAT HISTORY
# ================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ================= MAIN APP ================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99,102,241,0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(14,165,233,0.07),
                transparent 30%
            ),
            #f8fafc;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* ================= SIDEBAR ================= */

    [data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    color: #1e293b !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    color: #1e293b !important;
    background: #ffffff !important;
}

    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }

    /* Upload button and uploader text */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] * {
        color: #1e293b !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        color: #1e293b !important;
        background: #ffffff !important;
    }

    /* Chat History */
    [data-testid="stSidebar"] h3 {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stCaption p {
        color: #64748b !important;
    }

    /* Sidebar section heading */
    [data-testid="stSidebar"] .sidebar-section {
        color: #94a3b8 !important;
    }

    .sidebar-brand {
        text-align: center;
        padding: 15px 5px 25px 5px;
    }

    .sidebar-logo {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: #94a3b8 !important;
        margin-top: 5px;
    }

    .sidebar-section {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #94a3b8 !important;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    /* ================= HEADER ================= */

    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 5px 20px 5px;
    }

    .brand-area {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .brand-icon {
        width: 58px;
        height: 58px;
        border-radius: 18px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 30px;

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed
            );

        box-shadow:
            0 10px 25px rgba(79,70,229,0.25);
    }

    .brand-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1.2px;

        color: #1e293b;
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

        background: #ffffff;

        padding: 9px 15px;

        border-radius: 30px;

        border: 1px solid #e2e8f0;

        font-size: 13px;
        font-weight: 600;

        color: #475569;

        box-shadow:
            0 5px 15px rgba(15,23,42,0.05);
    }

    .status-dot {
        width: 9px;
        height: 9px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 0 4px rgba(34,197,94,0.12);
    }

    /* ================= WELCOME CARD ================= */

    .welcome-card {
        margin-top: 15px;

        padding: 35px;

        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                #eef2ff,
                #f8fafc
            );

        border: 1px solid #e0e7ff;

        box-shadow:
            0 12px 35px rgba(15,23,42,0.06);
    }

    .welcome-title {
        font-size: 27px;
        font-weight: 750;
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
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px 14px;
        color: #475569;
        font-size: 13px;
        font-weight: 600;
    }

    /* ================= CHAT AREA ================= */

    .chat-heading {
        font-size: 16px;
        font-weight: 700;
        color: #334155;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 12px;
        padding: 14px 18px;

        box-shadow:
            0 5px 18px rgba(15,23,42,0.04);
    }

    /* ================= INPUT ================= */

    [data-testid="stTextInput"] input {
        height: 58px !important;

        border-radius: 16px !important;

        border: 1px solid #dbe2ea !important;

        background: #ffffff !important;

        font-size: 15px !important;

        padding-left: 18px !important;

        box-shadow:
            0 7px 22px rgba(15,23,42,0.05);

        color: #1e293b !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 4px rgba(99,102,241,0.10),
            0 8px 25px rgba(15,23,42,0.06);
    }

    /* ================= BUTTONS ================= */

    .stButton > button {
        height: 50px;

        border-radius: 14px;

        font-weight: 650;

        border: 1px solid #e2e8f0;

        background: #ffffff;

        color: #334155;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color: #818cf8;

        color: #4f46e5;

        box-shadow:
            0 8px 22px rgba(79,70,229,0.12);
    }

    /* ================= UPLOAD ================= */

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.06);

        border-radius: 16px;

        padding: 8px;

        border: 1px solid rgba(255,255,255,0.10);
    }

    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #6366f1 !important;

        border-radius: 13px !important;
    }

    /* ================= DOCUMENT CARD ================= */

    .document-card {
        background: rgba(255,255,255,0.08);

        border: 1px solid rgba(255,255,255,0.10);

        border-radius: 14px;

        padding: 14px;

        margin-top: 15px;
    }

    .document-icon {
        font-size: 25px;
        margin-bottom: 5px;
    }

    .document-title {
        font-size: 13px;
        font-weight: 700;
    }

    .document-status {
        color: #86efac !important;
        font-size: 11px;
        margin-top: 4px;
    }

    /* ================= FOOTER ================= */

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 12px;

        margin-top: 35px;

        padding-top: 18px;

        border-top: 1px solid #e2e8f0;
    }

    /* ================= MOBILE ================= */

    @media (max-width: 768px) {

        .brand-title {
            font-size: 25px;
        }

        .online-status {
            display: none;
        }

        .welcome-card {
            padding: 25px;
        }

        .welcome-title {
            font-size: 23px;
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

    st.markdown("### 💬 Chat History")

    if st.session_state.chat_history:
        for chat in reversed(st.session_state.chat_history[-10:]):
            st.caption(f"💭 {chat}")
    else:
        st.caption("No previous questions yet.")

    st.markdown(
        '<div class="sidebar-section">Document</div>',
        unsafe_allow_html=True
    )

    pdf_text = ""

    if uploaded_file is not None:
        pdf_text = read_pdf(uploaded_file)

        st.markdown(
            f"""
            <div class="document-card">
                <div class="document-icon">📄</div>
                <div class="document-title">
                    {uploaded_file.name}
                </div>
                <div class="document-status">
                    ● PDF ready for questions
                </div>
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
        ">
            IntelliAssist AI helps you understand
            your PDF documents and get quick,
            AI-powered answers.
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
        <h1 style="
            margin-bottom:0;
            font-size:38px;
            color:#1e293b;
        ">
            🤖 IntelliAssist AI
        </h1>

        <p style="
            color:#64748b;
            margin-top:5px;
            font-size:14px;
        ">
            Your intelligent document assistant
        </p>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="
            margin-top:12px;
            padding:10px 15px;
            background:white;
            border:1px solid #e2e8f0;
            border-radius:25px;
            text-align:center;
            font-size:13px;
            font-weight:600;
            color:#475569;
        ">
            🟢 AI Assistant Online
        </div>
        """,
        unsafe_allow_html=True
    )



# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown("## 👋 Welcome to IntelliAssist AI")

    st.write(
        "Upload a PDF and ask questions about your document. "
        "IntelliAssist AI will help you understand the content "
        "quickly and clearly."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("📄 **PDF Analysis**")

    with col2:
        st.info("💬 **Smart Q&A**")

    with col3:
        st.info("⚡ **Fast Answers**")

    with col4:
        st.info("🔒 **Document Based**")
# =========================================================
# CHAT HISTORY
# =========================================================

if st.session_state.messages:

    st.markdown(
        '<div class="chat-heading">💬 Conversation</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

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
    label_visibility="collapsed"
)

# =========================================================
# ACTION BUTTONS
# =========================================================

c1, c2 = st.columns(2)

with c1:

    search = st.button(
        "🚀  Search",
        use_container_width=True
    )

with c2:

    clear = st.button(
        "🗑️  Clear Chat",
        use_container_width=True
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

        # Add user message

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        st.session_state.chat_history.append(question)

        # PDF based question

        if uploaded_file is not None:

            prompt = f"""
Answer ONLY from the uploaded PDF.

PDF CONTENT:
{pdf_text}

QUESTION:
{question}

If the answer is not available in the PDF, reply exactly:

I couldn't find that information in the uploaded PDF.

Keep the answer clear and easy to understand.
"""

            answer = get_response(prompt)

        else:

            answer = get_response(question)

        # Add AI response

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🤖 IntelliAssist AI &nbsp;•&nbsp;
    AI-Powered PDF Assistant
</div>
""", unsafe_allow_html=True)
