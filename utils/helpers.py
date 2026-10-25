import hashlib
import streamlit as st

SUPPORTED_TYPES = ["pdf", "docx", "txt", "md", "csv", "xlsx", "pptx"]
MAX_FILE_MB = 25
MAX_TOTAL_MB = 60


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def human_size(size: int) -> str:
    return f"{size / 1024 / 1024:.2f} MB" if size >= 1024 * 1024 else f"{size / 1024:.1f} KB"


def initialize_state():
    defaults = {
        "api_key": None,
        "documents": {},  # hash -> {name, bytes, size}
        "vectorstore": None,
        "index_signature": None,
        "messages": [],
        "chat_id": 0,
        "upload_generation": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_index():
    st.session_state.vectorstore = None
    st.session_state.index_signature = None


def logout():
    for key in ["api_key", "documents", "vectorstore", "index_signature", "messages", "chat_id", "login_key"]:
        st.session_state.pop(key, None)
    st.rerun()
