from flask import Flask, send_from_directory, jsonify
import os
import threading
import time
import urllib.request

app = Flask(__name__, static_folder="static")

# ─── Keep-alive: пингуем себя каждые 13 минут ───────────────────────────────
# Render Free засыпает ровно через 15 мин без внешних запросов.
# 13 минут — минимально достаточный интервал, тратит меньше всего ресурсов.
def _self_ping():
    # Ждём 30 сек после старта чтобы сервер успел подняться
    time.sleep(30)
    base = os.environ.get("WEBAPP_URL", "").replace("/app", "")
    if not base:
        base = "https://crypto-calculator-bot.onrender.com"
    health_url = base.rstrip("/") + "/health"
    print(f"[keep-alive] Starting self-ping every 13 min -> {health_url}")
    while True:
        try:
            req = urllib.request.Request(health_url, headers={"User-Agent": "keep-alive/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f"[keep-alive] ping OK {r.status}")
        except Exception as e:
            print(f"[keep-alive] ping failed: {e}")
        time.sleep(780)  # 13 минут

# Запускаем поток один раз при импорте модуля (gunicorn импортирует server.py)
_ping_thread = threading.Thread(target=_self_ping, daemon=True, name="keep-alive")
_ping_thread.start()

# ─── Запускаем Telegram бота в отдельном потоке ──────────────────────────────
def _run_bot():
    try:
        import asyncio
        from bot_runner import start_bot
        asyncio.run(start_bot())
    except Exception as e:
        print(f"[bot] crashed: {e}")

_bot_thread = threading.Thread(target=_run_bot, daemon=True, name="telegram-bot")
_bot_thread.start()

# ─── Flask routes ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/app")
def webapp():
    return send_from_directory("static", "index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
