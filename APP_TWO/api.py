from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataRequest(BaseModel):
    filename: str

@app.post("/request_file/")
def request_file(data: DataRequest):
    # Example: request file from APP_ONE
    url = "http://localhost:8001/file/" + data.filename
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch file from APP_ONE"}
