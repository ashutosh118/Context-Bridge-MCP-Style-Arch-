import streamlit as st
import requests
import os
import json
import mimetypes  # Add this import to detect file types
import pandas as pd  # Add this import for handling CSV and Excel files

st.title("APP ONE: MCP Resource Server UI")

API_URL = "http://localhost:8004"  # MCP resource server

st.header("Upload a File")
uploaded_file = st.file_uploader("Upload a file (PDF, CSV, Excel, DOCX)")
if uploaded_file:
    # Acts as an agent to upload files to the MCP resource server.
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{API_URL}/upload_file", files=files)
    if response.status_code == 200:
        st.success(f"File '{uploaded_file.name}' uploaded.")
    else:
        st.error("Upload failed.")

st.header("Available Files")
file_list = requests.get(f"{API_URL}/list_files").json().get("files", [])
if file_list:
    selected_file = st.selectbox("Select a file to manage:", file_list, key="file_dropdown")
    if selected_file:
        if st.button("Delete", key=f"delete_{selected_file}"):
            delete_response = requests.delete(f"{API_URL}/delete_file", params={"filename": selected_file})
            if delete_response.status_code == 200:
                st.success(f"File '{selected_file}' deleted successfully.")
                st.session_state["file_deleted"] = True
                st.write("Please refresh the page to see the updated file list.")
            else:
                st.error(f"Failed to delete file '{selected_file}'.")
else:
    st.warning("No files uploaded yet.")

st.header("Results from MCP Clients")
RESULTS_FILE = "results_from_app_two.json"
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)
    if results:
        # Acts as an agent to display and map results received from APP_TWO.
        # Organize results by filename
        files = list({r.get("filename", "[No file]") for r in results})
        selected_file = st.selectbox("Select a file to view queries:", files, index=None)
        # Filter results for the selected file and only keep those with a non-empty query
        file_results = [r for r in results if r.get("filename") == selected_file and r.get("query")]
        queries = [f"{r['query']} (Result {i+1})" for i, r in enumerate(file_results)]
        if queries:
            selected_query = st.selectbox("Select a query to view result:", queries, index=None)
            if selected_query:  # Ensure a valid query is selected
                selected_result = file_results[queries.index(selected_query)]  # Map back to the correct result
                if selected_result:
                    question = selected_result.get("query", "[No query provided]")
                    answer = selected_result.get("result", "[No answer provided]")
                    mime_type, _ = mimetypes.guess_type(selected_file)
                    st.info(f"**File:** {selected_file}\n\n**Question:** {question}\n\n**Answer:** {answer}")
                else:
                    st.write("No result found for this query.")
        else:
            st.selectbox("Select a query to view result:", ["No queries available"], disabled=True)
            st.write("No queries found for this file.")
                # Add Delete History button
        if st.button("Delete History", key="delete_history"):
            with open(RESULTS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
            st.success("All query history has been deleted.")
    else:
        st.warning("No results received yet.")
else:
    st.warning("No results received yet.")
