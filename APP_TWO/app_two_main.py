import streamlit as st
import requests
import os
import pandas as pd  # Add this import for handling Excel files
from llm_utils import ask_llama3
from vectorstore_utils import VectorStore
from send_result_utils import send_result_to_app_one
from mcp_client_utils import list_files, get_file_content, write_summary
import io
import base64
from PyPDF2 import PdfReader
import pdfplumber
from docx import Document
import json

st.title("APP TWO: MCP Client/Agent UI")

API_URL = "http://localhost:8004"  # MCP resource server

st.header("Import Data/Context from MCP Resource Server")

# Add error handling for server connection issues
try:
    file_list = list_files()
except requests.exceptions.ConnectionError as e:
    st.error(f"Failed to connect to MCP Resource Server: {e}")
    file_list = []

if not file_list:
    st.warning("No resource received from server.")

selected_file = st.selectbox("Select a file from MCP Resource Server", file_list, index=None, key="mcp_file_select") if file_list else None

if "extracted_content" not in st.session_state:
    st.session_state["extracted_content"] = ""

if "imported_content" not in st.session_state:
    st.session_state["imported_content"] = ""


# Define a mapping of file extensions to MIME types
EXTENSION_TO_MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".csv": "text/csv",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


# Enhanced file handling with fallback mechanisms and Streamlit widgets
if selected_file:
    try:
        # Decode JSON response from get_file_content
        response = get_file_content(selected_file)
        if isinstance(response, (bytes, str)):
            response = json.loads(response)  # Parse JSON if needed

        # Handle inconsistent encoding in the server response
        content = response["content"]
        try:
            # Attempt to decode as base64
            file_content = base64.b64decode(content)
        except Exception:
            # Fallback to raw text if base64 decoding fails
            file_content = content.encode("utf-8")

        file_extension = os.path.splitext(selected_file)[1].lower()
        mime_type = EXTENSION_TO_MIME.get(file_extension)

        if not file_content:
            raise ValueError("File content is empty or could not be retrieved.")

        # Enhanced handling for PDF and DOCX files
        with st.expander("File Content"):
            if mime_type == "application/pdf":
                try:
                    # Check if the content is raw text
                    if not file_content.startswith(b"%PDF"):
                        st.warning("The file does not appear to be a valid PDF. Displaying as plain text.")
                        st.info("Raw PDF Content", file_content.decode(errors="ignore"), height=400)
                    else:
                        pdf_reader = PdfReader(io.BytesIO(file_content))
                        if not pdf_reader.pages:
                            raise ValueError("The PDF file has no readable pages.")
                        pdf_text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                        st.info(pdf_text)
                        st.session_state["extracted_content"] = pdf_text
                        # pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(file_content).decode()}" width="700" height="1000" type="application/pdf"></iframe>'
                        # st.markdown(pdf_display, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error reading PDF file: {e}")

            elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                try:
                    if not file_content.startswith(b"PK"):
                        st.warning("The file does not appear to be a valid Word document. Displaying as plain text.")
                        st.info(file_content.decode(errors="ignore"))
                    else:
                        doc = Document(io.BytesIO(file_content))
                        doc_text = "\n".join([p.text for p in doc.paragraphs])
                        if not doc_text.strip():
                            raise ValueError("The Word document is empty or corrupted.")
                        st.info(doc_text)
                        st.session_state["extracted_content"] = doc_text
                except Exception as e:
                    st.error(f"Error reading Word file: {e}")
            elif mime_type in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                try:
                    # Validate tabular content
                    if mime_type == "text/csv":
                        # Decode bytes to string for CSV
                        csv_str = file_content.decode("utf-8", errors="ignore")
                        df = pd.read_csv(io.StringIO(csv_str))
                        st.session_state["extracted_content"] = csv_str
                    else:
                        df = pd.read_excel(io.BytesIO(file_content), engine="openpyxl")
                        st.session_state["extracted_content"] = df.to_csv(index=False)
                    if df.empty:
                        raise ValueError("The tabular file is empty or corrupted.")
                    st.dataframe(df)
                    # st.session_state["extracted_content"] = df
                except Exception as e:
                    st.error(f"Error reading tabular file: {e}")
 

        # st.session_state["imported_content"] = file_content.decode(errors="ignore")
        st.session_state["imported_content"] = st.session_state["extracted_content"]
        st.session_state["extracted_content"]=""

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Extract Content", key="extract_content_btn"):
            st.info("Indexing document for semantic search...")
            vs = VectorStore()
            vs.clear()
            chunks = [c.strip() for c in st.session_state["imported_content"].split("\n\n") if c.strip()]
            if not chunks:
                chunks = [st.session_state["imported_content"].strip()]
            docs = [{"text": chunk, "filename": selected_file} for chunk in chunks]
            vs.add_docs(docs)
            st.success("Document indexed for Q&A.")
    with col2:
        if st.button("Clear Vectorstore", key="clear_vectorstore_btn"):
            vs = VectorStore()
            vs.clear()
            st.success("Vectorstore cleared successfully.")

if file_list:
    st.header("Chat with LLM")
    # Clear the input if needed
    with st.form("query_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question or request analysis:", key="query_input")
        submitted = st.form_submit_button("Submit")

    # Orchestrating agents: Querying and generating responses
    if user_input:
        st.info(f"Query: {user_input}")
        # Agent 4: Query the VectorStore for relevant context
        vs = VectorStore()
        retrieved_chunks = vs.search(user_input, top_k=3)
        context = "\n---\n".join([f"[{r['filename']}]\n{r['text']}" for r in retrieved_chunks])
        full_prompt = user_input
        if context:
            full_prompt = f"Context:\n{context}\n\nQuestion: {user_input}"
        with st.spinner("Thinking..."):
            # Agent 5: Query the LLM for a response
            answer = ask_llama3(full_prompt)
        st.success(f"LLM: {answer}")
        if selected_file:
            # Agent 6: Send results back to APP_ONE
            send_result_to_app_one(selected_file, user_input, answer)
    
