import requests

MCP_API_URL = "http://localhost:8004"  # Change port as needed

def list_files():
    return requests.get(f"{MCP_API_URL}/list_files").json().get("files", [])

def get_file_content(filename):
    response = requests.get(f"{MCP_API_URL}/get_file_content", params={"filename": filename})
    response.raise_for_status()  # Raise an error for bad responses
    return response.content  # Return raw binary content

def write_summary(filename, result):
    data = {"filename": filename, "result": result}
    resp = requests.post(f"{MCP_API_URL}/write_summary", json=data)
    return resp.status_code == 200
