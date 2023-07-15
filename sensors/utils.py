import httpx
import json

# Set the headers
headers = {
    "Content-Type": "application/json",
}


def send_event(url: str, message: str) -> None:
    """Send an event to the http server
    and retry if it fails"""
    while True:
        try:
            httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
            break
        except Exception as e:
            print(f"Failed to send event: {message} with exception: {e}")
            print("Waiting for the http server to start up...")