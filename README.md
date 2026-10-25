# Nova AI — Document Assistant

A Streamlit RAG app with OpenAI, LangChain, FAISS, and PDF / DOCX / TXT / MD / CSV / XLSX / PPTX support.

## Run locally (macOS / VS Code)

```bash
cd nova-ai-document-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Enter your OpenAI API key on the welcome screen. Your key must have API access and available billing/quota. Indexing creates paid embeddings and chat uses paid model calls.

## Deploy on Streamlit Community Cloud

1. Push the project folder's contents to a **private** GitHub repository (without `.env` or API keys).
2. On Streamlit Community Cloud, select the repository and `app.py` as the entrypoint.
3. Deploy. The user supplies their own OpenAI API key in the welcome screen.
4. No server-side API key is required.

## Limitations

- PDF extraction is text-only. Scanned PDFs require OCR (not included).
- Upload limit: 25 MB per file, 60 MB total in the current session. Hosting memory and upload caps may be lower.
- FAISS index, documents, chat and API key are stored in **Streamlit session state**, not persisted to a database. Browser reconnects/restarts can reset them.
- Source references identify retrieved chunks, not guaranteed proof that every claim in the generated answer is supported.
- The API key screen validates access, but is **not user authentication**. Don't use it as a security boundary for multi-tenant deployments.
- For copying an answer, click “Copy answer” to expose a selectable text block, then copy it manually.
- When changing chunk settings, click **Build knowledge base** to re-index.
