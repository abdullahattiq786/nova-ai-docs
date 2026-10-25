import streamlit as st
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError


def render_login():
    st.markdown('<div class="login-brand">✦ NOVA <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-eyebrow">YOUR INTELLIGENT WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">Chat with your <span>documents</span> using AI.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Upload PDFs, Word files, spreadsheets and presentations. Find answers in seconds, with source references.</p>', unsafe_allow_html=True)
    st.markdown('<div class="feature-row">✧ Multi-file knowledge base &nbsp; · &nbsp; ◈ Private session &nbsp; · &nbsp; ⌁ Source-aware answers</div>', unsafe_allow_html=True)
    _, middle, _ = st.columns([1, 1.45, 1])
    with middle:
        with st.form("login_form"):
            st.markdown("#### Connect your OpenAI account")
            key = st.text_input("OpenAI API key", type="password", placeholder="sk-...", key="login_key")
            submitted = st.form_submit_button("Launch Assistant  →", use_container_width=True, type="primary")
        st.caption("Your key stays in this Streamlit session. API usage may incur OpenAI charges.")
        if submitted:
            if not key.strip():
                st.warning("Please enter an API key.")
                return
            try:
                with st.spinner("Validating your API key..."):
                    OpenAI(api_key=key.strip(), timeout=15).models.list()
                st.session_state.api_key = key.strip()
                st.session_state.pop("login_key", None)
                st.rerun()
            except AuthenticationError:
                st.error("The API key was rejected. Please check it and try again.")
            except RateLimitError:
                st.error("OpenAI is rate-limiting requests. Please try again shortly.")
            except APIConnectionError:
                st.error("Could not connect to OpenAI. Check your internet connection.")
            except APIStatusError:
                st.error("OpenAI could not validate the key right now. Please try again.")
            except Exception:
                st.error("Unable to validate the API key. Please try again.")
