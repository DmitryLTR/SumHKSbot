from commands.command_processor import CommandProcessor
from telegram import Update

class HelpCommandProcessor(CommandProcessor):
    
    def supports(self, command: str, context) -> bool:
        return command == '/help'
    
    async def process(self, message: Update, context):
        await message.message.reply_text(
            "Доступные команды:\n"
            "/start - запуск бота\n"
            "/salary - подсчет зп кальян мастера за смену\n"
            "/tbc_calculator - калькулятор табака"
        )
    
    def can_access(self, user) -> bool:
        return True