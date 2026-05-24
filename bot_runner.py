"""
bot_runner.py — запускается из server.py в отдельном потоке.
Отдельный файл нужен чтобы asyncio.run() не конфликтовал с Flask.
"""
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import start_keep_alive
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(
        text="📊 Открыть Crypto Calculator",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    await update.message.reply_text(
        "👋 Привет! Нажми кнопку ниже чтобы открыть калькулятор прямо здесь в Telegram.\n\n"
        "Работает и на телефоне, и на ПК.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(
        text="📊 Crypto Calculator",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    await update.message.reply_text(
        "Открываю калькулятор 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Crypto Calculator*\n\n"
        "• *Leverage Calc* — Entry Price, Stop Loss, Margin, Max Leverage → нужное плечо\n\n"
        "• *Margin Calc* — Entry Price, Stop Loss, Leverage, Desired Loss → нужная маржа\n\n"
        "Команды: /start /calc /help",
        parse_mode="Markdown"
    )

async def start_bot():
    if not BOT_TOKEN or not WEBAPP_URL:
        print("[bot] BOT_TOKEN или WEBAPP_URL не заданы, бот не запущен")
        return

    start_keep_alive()

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calc", calc))
    application.add_handler(CommandHandler("help", help_cmd))

    print(f"[bot] started | WebApp: {WEBAPP_URL}")
    await application.run_polling(drop_pending_updates=True)
