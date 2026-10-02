import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import google.generativeai as genai

# লোগিং সেটআপ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# আপনার Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6ItMMvm5EdmJuXPHjyDM0jNAsFjJIjAFHs8H-rp4cwGTg"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "হ্যালো! আমি আপনার নিজস্ব এআই অ্যাসিস্ট্যান্ট বট। 🤖\n\n"
        "আমাকে যেকোনো প্রশ্ন করুন, আমি একদম ঠিকঠাক উত্তর দেবো!"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = model.generate_content(user_question)
        answer = response.text
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("দুঃখিত! এই মুহূর্তে উত্তর দিতে একটু সমস্যা হচ্ছে, আবার চেষ্টা করুন।")

def main():
    TELEGRAM_TOKEN = "8753444727:AAHZfCFMQYpL_0yx49MZDEhBVNq5Urzq1eQ"
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("AI Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
