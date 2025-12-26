import requests
from llm_utils import ask_llama3
import time

API_ONE_URL = "http://localhost:8001"

# Agent loop: poll for new files, analyze, and print results
def agent_loop(poll_interval=10):
    seen_files = set()
    while True:
        try:
            file_list = requests.get(f"{API_ONE_URL}/files/").json().get("files", [])
            new_files = [f for f in file_list if f not in seen_files]
            for filename in new_files:
                file_resp = requests.get(f"{API_ONE_URL}/file/{filename}")
                if file_resp.status_code == 200:
                    content = file_resp.json().get("content", "")
                    prompt = f"Summarize the following file content:\n{content}"
                    answer = ask_llama3(prompt)
                    print(f"\n[Agent] File: {filename}\nSummary: {answer}\n")
                    seen_files.add(filename)
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("Agent stopped.")
            break
        except Exception as e:
            print(f"Agent error: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    agent_loop()
