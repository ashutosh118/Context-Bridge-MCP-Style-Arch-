from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import os
import shutil
from PyPDF2 import PdfReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@app.get("/files/")
def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}


@app.get("/file/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        # If PDF, extract text
        if filename.lower().endswith(".pdf"):
            try:
                reader = PdfReader(file_path)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                return {"filename": filename, "content": text}
            except Exception as e:
                return {"filename": filename, "content": f"[PDF extraction error: {e}]"}
        # Otherwise, return as text
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    return {"error": "File not found"}
