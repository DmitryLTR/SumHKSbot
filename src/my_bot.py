import importlib
import os
import pkgutil
import commands
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from commands.command_processor import CommandProcessor
from typing import List

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_all_processors():
    for _, module_name, _ in pkgutil.iter_modules(commands.__path__):
        importlib.import_module(f"{commands.__name__}.{module_name}")

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
    load_all_processors()
    processors = [cls() for cls in CommandProcessor.__subclasses__()]
    print("Найдены процессоры:")
    for p in processors:
        print(" •", p.__class__.__name__)

    app = Application.builder().token(BOT_TOKEN).build()
    
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await router(update, context, processors)

    app.add_handler(MessageHandler(filters.COMMAND, wrapper))
    app.add_handler(MessageHandler(filters.TEXT, wrapper))

    print("✅ Бот запущен")
    app.run_polling()
    
if __name__ == "__main__":
    main()