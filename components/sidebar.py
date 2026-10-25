import streamlit as st
from utils.helpers import clear_index, logout, human_size


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">✦ NOVA <span>AI</span><small>DOCUMENT ASSISTANT</small></div>', unsafe_allow_html=True)
        if st.button("＋  New chat", use_container_width=True, type="primary"):
            st.session_state.messages = []
            st.session_state.chat_id += 1
            st.rerun()
        st.markdown("### Your documents")
        if not st.session_state.documents:
            st.caption("No documents uploaded yet")
        for doc_id, doc in list(st.session_state.documents.items()):
            a, b = st.columns([4, 1], vertical_alignment="center")
            with a:
                st.markdown(f"📄 **{doc['name']}**")
                st.caption(human_size(doc["size"]))
            with b:
                if st.button("✕", key=f"remove_{doc_id}", help=f"Remove {doc['name']}"):
                    del st.session_state.documents[doc_id]
                    clear_index()
                    st.session_state.upload_generation += 1
                    st.session_state.messages = []
                    st.rerun()
        st.divider()
        with st.expander("⚙️  AI settings", expanded=False):
            model = st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"])
            size = st.slider("Chunk size", 500, 2000, 1000, 100)
            overlap = st.slider("Chunk overlap", 0, 400, 150, 50)
            k = st.slider("Retrieved chunks", 2, 10, 4)
            temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
        st.divider()
        st.caption("🔒 Your API key and documents are held in this session.")
        if st.button("↪  Log out", use_container_width=True):
            logout()
    return {"model": model, "size": size, "overlap": overlap, "k": k, "temperature": temperature}
