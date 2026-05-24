from flask import Flask, send_from_directory, jsonify
import os
import threading

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/app")
def webapp():
    return send_from_directory("static", "index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

def run_bot():
    """Запускает Telegram бота в отдельном потоке."""
    try:
        import asyncio
        from bot_runner import start_bot
        asyncio.run(start_bot())
    except Exception as e:
        print(f"[bot] error: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    app.run(host="0.0.0.0", port=port)
