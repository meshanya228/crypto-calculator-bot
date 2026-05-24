# Crypto Calculator — Telegram Mini App

Telegram-бот с встроенным калькулятором кредитного плеча и маржи для крипто-трейдинга.

## Структура
- `bot.py` — Telegram бот
- `server.py` — Flask сервер для раздачи Mini App
- `static/index.html` — веб-интерфейс калькулятора
- `requirements.txt` — зависимости
- `Procfile` — конфиг для Railway

## Переменные окружения (задаются в Railway)
- `BOT_TOKEN` — токен от @BotFather
- `WEBAPP_URL` — URL задеплоенного приложения + `/app`
- `PORT` — задаётся Railway автоматически
