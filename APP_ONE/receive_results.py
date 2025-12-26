from fastapi import FastAPI, Request
import os
import json

RESULTS_FILE = "results_from_app_two.json"

app = FastAPI()

@app.post("/receive_result/")
async def receive_result(request: Request):
    data = await request.json()
    # Append result to file
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
    results.append(data)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return {"status": "received"}
