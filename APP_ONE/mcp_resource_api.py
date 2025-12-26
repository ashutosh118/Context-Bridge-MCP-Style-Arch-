from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import json
from PyPDF2 import PdfReader
import base64

UPLOAD_DIR = "uploaded_files"
RESULTS_FILE = "results_from_app_two.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_file")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@app.get("/list_files")
def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}


@app.get("/get_file_content")
def get_file_content(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        ext = filename.lower().split('.')[-1]
        # Binary files: PDF, DOCX, XLSX, XLS
        if ext in ["pdf", "docx", "xlsx", "xls"]:
            with open(file_path, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf-8")
            return {"filename": filename, "content": content}
        # CSV and TXT files: send as raw text
        if ext in ["csv", "txt"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {"filename": filename, "content": content}
        # Fallback: try text
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    return {"error": "File not found"}

@app.post("/write_summary")
async def write_summary(request: Request):
    data = await request.json()
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
    results.append(data)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return {"status": "received"}

@app.delete("/delete_file")
def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "success", "message": f"File '{filename}' deleted successfully."}
    return {"status": "error", "message": f"File '{filename}' not found."}
