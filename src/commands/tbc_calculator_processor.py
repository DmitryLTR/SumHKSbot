from commands.command_processor import CommandProcessor
from telegram import Update

class TbcCalculatorCommandProcessor(CommandProcessor):
    
    def supports(self, command: str, context) -> bool:
        return command == '/tbc_calculator' or context.user_data.get('state_tbc') == 'WAITING_TBC_REPORT'
    
    async def process(self, message: Update, context):
        if context.user_data.get('state_tbc') == 'WAITING_TBC_REPORT':
            context.user_data['state_tbc'] = None
            return await self.handle_report(message)
        
        await message.message.reply_text('Скинь мне отчет взвешиваний контейнеров в формате: \n'
                                         '123\n'
                                         '234')
        context.user_data['state_tbc'] = 'WAITING_TBC_REPORT'
        
    async def handle_report(self, update: Update):
        user_text = update.message.text
        numbers = []
        response = "Обработанные данные:\n"
        for line in user_text.split('\n'):
            line = line.strip()  # Убираем пробелы и переносы
            if line:  # Если строка не пустая
                try:
                    numbers.append(int(line))
                except ValueError:
                    print(f"Пропущено нечисловое значение: {line}")

        total = sum(numbers)
        response += f"\n💰 Взвешивания: {numbers}"
        response += f"\n💰 Результат взвешивания: {total}"
        await update.message.reply_text(response)
                
    
    def can_access(self, user) -> bool:
        return True