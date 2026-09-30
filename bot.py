import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# লগিং সেটআপ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ১. স্টার্ট কমান্ড হ্যান্ডলার (ভিডিওর প্রথম ধাপের মতো)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Create a bot", callback_data="create_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "Telegram hands the subscriber list only to a bot "
        "the owner made. That is why you need your own bot.\n\n"
        "Send /cancel to abort."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ২. বাটন ক্লিক হ্যান্ডলার (Create a bot এ ক্লিক করলে যা হবে)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "create_bot":
        context.user_data["state"] = "WAITING_FOR_NAME"
        await query.message.reply_text(
            "Create Bot\n\nTap to edit bot name.\n\nSend your bot name now:"
        )

# ৩. ইউজারের পাঠানো নাম ও ইউজারনেম রিসিভ করা
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    
    if state == "WAITING_FOR_NAME":
        bot_name = update.message.text
        context.user_data["bot_name"] = bot_name
        context.user_data["state"] = "WAITING_FOR_USERNAME"
        
        await update.message.reply_text(
            f"Bot Name: {bot_name}\n\nNow send the username for your bot (must end with _bot):"
        )
        
    elif state == "WAITING_FOR_USERNAME":
        bot_username = update.message.text
        bot_name = context.user_data.get("bot_name")
        context.user_data["state"] = None
        
        # এখানে আপনি ব্যবহারকারীর দেওয়া তথ্য ডাটাবেসে সেভ করবেন 
        # অথবা টেলিগ্রামের ব্যাকএন্ড লজিক প্রসেস করবেন।
        
        await update.message.reply_text(
            f"✅ Success!\n\nBot Name: {bot_name}\nUsername: {bot_username}\n\n"
            "Now please send a bot token from @BotFather to continue:"
        )

def main():
    # এখানে আপনার মাস্টার বটের টোকেন বসাবেন (যা BotFather থেকে পেয়েছেন)
    TOKEN = "8834179265:AAGSNxJJmgUV3Sa_tp3K8PxCv8WGtnK1UPw"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
