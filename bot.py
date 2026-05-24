from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
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
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Нажми кнопку ниже, чтобы открыть калькулятор прямо здесь в Telegram.",
        reply_markup=reply_markup
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 *Crypto Calculator* — калькулятор кредитного плеча и маржи.\n\n"
        "• *Leverage Calc* — Entry Price, Stop Loss, Margin, Max Leverage → нужное плечо\n"
        "• *Margin Calc* — Entry Price, Stop Loss, Leverage, Desired Loss → нужная маржа\n\n"
        "Нажми /start чтобы открыть калькулятор.",
        parse_mode="Markdown"
    )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан в переменных окружения!")
    if not WEBAPP_URL:
        raise ValueError("WEBAPP_URL не задан в переменных окружения!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    print(f"Bot started. WebApp URL: {WEBAPP_URL}")
    app.run_polling()

if __name__ == "__main__":
    main()
