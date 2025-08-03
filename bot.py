from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "ваш_токен_сюда"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь описание товара, я всё проверю.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "¥" in text:
        try:
            price = float(text.split("¥")[1].split()[0])
            kzt = round(price * 60, 2)
            await update.message.reply_text(f"💴 ¥{price} ≈ {kzt} ₸")
        except:
            await update.message.reply_text("Не удалось распознать цену.")
    else:
        await update.message.reply_text("Описание получено, но цена не найдена.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()