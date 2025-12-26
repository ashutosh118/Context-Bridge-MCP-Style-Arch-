import requests

def send_result_to_app_one(filename, query, result, api_url="http://localhost:8003/receive_result/"):
    data = {"filename": filename, "query": query, "result": result}
    try:
        resp = requests.post(api_url, json=data)
        return resp.status_code == 200
    except Exception as e:
        print(f"Failed to send result: {e}")
        return False
