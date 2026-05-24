from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import start_keep_alive
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="📊 Открыть Crypto Calculator",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    await update.message.reply_text(
        "👋 Привет! Нажми кнопку ниже чтобы открыть калькулятор прямо здесь в Telegram.\n\n"
        "Работает и на телефоне, и на ПК.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="📊 Crypto Calculator",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    await update.message.reply_text(
        "Открываю калькулятор 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Crypto Calculator*\n\n"
        "• *Leverage Calc* — вводишь Entry Price, Stop Loss, Margin и Max Leverage → получаешь нужное плечо и скорректированную маржу\n\n"
        "• *Margin Calc* — вводишь Entry Price, Stop Loss, Leverage и Desired Loss → получаешь нужную маржу и размер позиции\n\n"
        "Команды:\n"
        "/start — главное меню\n"
        "/calc — открыть калькулятор\n"
        "/help — эта справка",
        parse_mode="Markdown"
    )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан!")
    if not WEBAPP_URL:
        raise ValueError("WEBAPP_URL не задан!")

    # Запускаем пингер чтобы сервер не засыпал
    start_keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("help", help_cmd))

    print(f"Bot started | WebApp: {WEBAPP_URL}")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
