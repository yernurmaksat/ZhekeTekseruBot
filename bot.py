from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
import re

TOKEN = "8291369010:AAGJEVaOp3ovV88Ol2bpCRDAMbQdVCfiaFU"

def yuan_to_kzt(yuan: str) -> float:
    try:
        return round(float(yuan) * 60, 2)
    except ValueError:
        return 0.0

def analyze_text(text: str) -> list:
    suspicious = ["replica", "copy", "fake", "non-original", "подделка", "реплика", "копия"]
    return [w for w in suspicious if w.lower() in text.lower()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send a product description and I will analyze it.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    price_match = re.search(r"¥(\d+(?:\.\d+)?)", text)
    yuan = price_match.group(1) if price_match else None
    kzt = yuan_to_kzt(yuan) if yuan else None
    flags = analyze_text(text)

    reply = "📦 Product received.\n"
    if yuan:
        reply += f"💴 Price: ¥{yuan} ≈ {kzt} ₸\n"
    reply += f"⚠️ Suspicious words: {', '.join(flags)}" if flags else "✅ No suspicious words found."

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
