import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from commands.command_processor import CommandProcessor
from typing import List

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")



async def router(update: Update, context: ContextTypes.DEFAULT_TYPE, processors: List[CommandProcessor]):
    text = update.message.text.strip()

    for processor in processors:
        if processor.supports(text, context):
            if not processor.can_access(update.message.from_user):
                return await update.message.reply_text("❌ Нет прав")
            return await processor.process(update, context)
    
    return await update.message.reply_text("❗ Неизвестная команда")


# ======================================
#      MAIN
# ======================================

def main():
    processors = [cls() for cls in CommandProcessor.__subclasses__()]
    print("Найдены процессоры:")
    for p in processors:
        print(" •", p.__class__.__name__)

    app = Application.builder().token(BOT_TOKEN).build()
    
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await router(update, context, processors)

    # ✅ 4. Один универсальный обработчик
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wrapper))

    print("✅ Бот запущен")
    app.run_polling()
    
if __name__ == "__main__":
    main()