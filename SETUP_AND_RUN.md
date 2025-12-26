# Setup and Run Instructions for MCP POC

## Prerequisites
- Python 3.8+
- pip
- Ollama installed and running (for local LLMs)
- (Optional) Tesseract OCR if you want to support image-based PDFs

## 1. Clone or Download the Project

## 2. Install Dependencies
For each app, open a terminal and run:

### APP_ONE
```
cd APP_ONE
pip install -r requirements.txt
pip install PyPDF2 streamlit-autorefresh
```

### APP_TWO
```
cd APP_TWO
pip install -r requirements.txt
pip install faiss-cpu sentence-transformers
```

ollama serve

## 3. Start the Backends

### APP_ONE FastAPI backend (file API)
```
cd APP_ONE
python run_api.py
```

### APP_ONE Results Receiver (for results from APP_TWO)
```
cd APP_ONE
uvicorn receive_results_api:app --host 0.0.0.0 --port 8003 --reload
uvicorn mcp_resource_api:app --host 0.0.0.0 --port 8004 --reload```

### APP_TWO FastAPI backend (optional, for future extensions)
```
cd APP_TWO
python run_api.py
```

## 4. Start the Streamlit UIs

### APP_ONE UI
```
cd APP_ONE
streamlit run app_one_main.py
```

### APP_TWO UI
```
cd APP_TWO
streamlit run app_two_main.py
```

## 5. Start the Agent (optional, for automation)
```
cd APP_TWO
python agent.py
```

## 6. Workflow
- Upload files in APP_ONE UI
- Import and analyze files in APP_TWO UI
- Ask questions in APP_TWO; answers are sent back to APP_ONE and displayed automatically

## Notes
- Make sure Ollama is running and the desired model (e.g., llama3) is pulled.
- The results section in APP_ONE auto-refreshes to show new results from APP_TWO.
- All communication is local and privacy-respecting.
