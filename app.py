import streamlit as st
from components.login import render_login
from components.sidebar import render_sidebar
from components.chat import render_chat
from utils.helpers import initialize_state, SUPPORTED_TYPES, MAX_FILE_MB, MAX_TOTAL_MB, digest, human_size, clear_index
from utils.document_loader import load_document
from utils.rag_pipeline import build_index, index_signature

st.set_page_config(page_title="Nova AI | Document Assistant", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
with open("styles/custom.css", encoding="utf-8") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
initialize_state()

if not st.session_state.api_key:
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    render_login()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

settings = render_sidebar()
st.markdown('<div class="eyebrow">✦ AI-POWERED DOCUMENT INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<h1 class="dashboard-title">Your AI Document <span>Workspace</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subtitle">Upload your documents and start asking intelligent questions.</p>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### ↥ Upload documents")
    st.caption("PDF · DOCX · TXT · MD · CSV · XLSX · PPTX — up to 25 MB each, 60 MB total")
    uploads = st.file_uploader("Drag and drop files or browse", type=SUPPORTED_TYPES, accept_multiple_files=True, key=f"uploads_{st.session_state.upload_generation}")
    if uploads:
        added, skipped, errors = 0, 0, []
        for upload in uploads:
            data = upload.getvalue()
            file_id = digest(data)
            if file_id in st.session_state.documents:
                skipped += 1
                continue
            if len(data) > MAX_FILE_MB * 1024 * 1024:
                errors.append(f"{upload.name}: exceeds {MAX_FILE_MB} MB limit")
                continue
            current_total = sum(item["size"] for item in st.session_state.documents.values())
            if current_total + len(data) > MAX_TOTAL_MB * 1024 * 1024:
                errors.append(f"{upload.name}: total upload limit exceeded")
                continue
            try:
                load_document(upload.name, data)  # Validate before adding.
                st.session_state.documents[file_id] = {"name": upload.name, "bytes": data, "size": len(data)}
                added += 1
            except Exception as exc:
                errors.append(f"{upload.name}: {exc}")
        if added:
            clear_index()
            st.session_state.messages = []
            st.toast(f"Added {added} document(s)", icon="✅")
            st.rerun()
        for error in errors:
            st.warning(error)

count = len(st.session_state.documents)
if count:
    st.markdown(f"**{count} document(s) ready** · {human_size(sum(d['size'] for d in st.session_state.documents.values()))} total")
    signature = index_signature(st.session_state.documents, settings["size"], settings["overlap"], st.session_state.api_key)
    if st.session_state.index_signature != signature:
        st.session_state.vectorstore = None
        if st.button("✦  Build knowledge base", type="primary", use_container_width=True):
            try:
                with st.spinner("Extracting text, splitting documents, and creating embeddings..."):
                    store, chunks = build_index(st.session_state.documents, settings["size"], settings["overlap"], st.session_state.api_key)
                st.session_state.vectorstore = store
                st.session_state.index_signature = signature
                st.session_state.messages = []
                st.success(f"Knowledge base ready — {chunks} text chunks indexed.")
                st.rerun()
            except Exception:
                st.error("Could not index the documents. Check file contents, API access, billing, and connection.")
    else:
        st.success("Knowledge base ready. Ask your questions below.")
else:
    st.markdown('<div class="empty-state"><div class="empty-icon">✦</div><h3>All your knowledge. One conversation.</h3><p>Upload a file to create a searchable AI knowledge base.</p></div>', unsafe_allow_html=True)
    st.markdown("**Try asking:**  *Summarize the key findings* · *What are the main recommendations?* · *Compare these documents*")

render_chat(settings)
