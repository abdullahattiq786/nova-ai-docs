import streamlit as st
from utils.rag_pipeline import answer_question


def render_chat(settings):
    st.markdown("### Ask Nova")
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="✦" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources retrieved"):
                    for source in message["sources"]:
                        st.caption("• " + source)
            if message["role"] == "assistant":
                st.button("Copy answer", key=f"copy_{st.session_state.chat_id}_{i}", on_click=lambda s=message["content"]: st.session_state.update({"copy_text": s}), help="Select the answer text below to copy")
                if st.session_state.get("copy_text") == message["content"]:
                    st.code(message["content"], language=None)
    question = st.chat_input("Ask anything about your documents...", disabled=st.session_state.vectorstore is None)
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)
        with st.chat_message("assistant", avatar="✦"):
            try:
                with st.spinner("Finding relevant passages..."):
                    answer, sources = answer_question(
                        st.session_state.vectorstore, question, st.session_state.api_key,
                        settings["model"], settings["temperature"], settings["k"]
                    )
                st.markdown(answer)
                with st.expander("Sources retrieved"):
                    for source in sources:
                        st.caption("• " + source)
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
            except Exception:
                st.error("Unable to generate an answer. Check your OpenAI quota, API access, and connection.")
