import threading
import time
import urllib.request
import os

def keep_alive():
    """Пингует сам себя каждые 5 минут чтобы не засыпать."""
    url = os.environ.get("WEBAPP_URL", "").replace("/app", "/health")
    if not url:
        return
    while True:
        time.sleep(300)  # каждые 5 минут
        try:
            urllib.request.urlopen(url, timeout=10)
            print(f"[keep-alive] ping OK -> {url}")
        except Exception as e:
            print(f"[keep-alive] ping failed: {e}")

def start_keep_alive():
    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()
