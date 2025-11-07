from commands.command_processor import CommandProcessor
from telegram import Update

class SalaryCommandProcessor(CommandProcessor):
    
    def supports(self, command: str, context) -> bool:
        return command == '/salary' or context.user_data['state'] == 'WAITING_REPORT'
    
    async def process(self, message: Update, context):
        if context.user_data['state'] == 'WAITING_REPORT':
            context.user_data['state'] = None
            return await self.handle_report(message)
            
        await message.message.reply_text('Скинь мне отчет в формате: *название кальяна* x *количество* (*процент скидки*). \n'
                                        'Пример: 1x5(20), 2x4(30)')
        context.user_data['state'] = 'WAITING_REPORT'
        
    async def handle_report(update: Update):
        user_text = update.message.text
        items = user_text.split(",")
        salary_18 = 0
        salary_14_without_discount = 0
        salary_18_without_discount = 0
        
        response = "Обработанные данные:\n"
        for item in items:
            item = item.strip()
            try:
                # Проверяем есть ли скобки с процентом
                if '(' in item and ')' in item:
                    # Формат "1х5(10%)"
                    name_hookah = item.split('x')[0]
                    rest = item.split('x')[1]
                    count = rest.split('(')[0]
                    percent = rest.split('(')[1].replace('%)', '').replace('%', '')
                    percent_decimal = float(percent) / 100
                else:
                    # Формат "1x3" - без процента
                    name_hookah = item.split('x')[0]
                    count = item.split('x')[1]
                    percent_decimal = 0  # третья ячейка заменяется на 0
                    
                match name_hookah:
                    case '1':
                        first_cell = 40
                    case '2':
                        first_cell = 52
                    case 'Cel':
                        first_cell = 65
                    case 'Rub':
                        first_cell = 78
                    case 'Pum':
                        first_cell = 45
                    case 'Ex':
                        first_cell = 48
                    case 'Of':
                        first_cell = 2.8
                    case _:
                        first_cell = float(name_hookah)
                
                count_num = float(count)
                
                response += f"• {item} → [{first_cell}, {count_num}, {percent_decimal}]\n"
                salary_14_without_discount += first_cell * count_num * 0.14
                salary_18_without_discount += first_cell * count_num * 0.18
                salary_18 += first_cell * (1 - percent_decimal) * count_num * 0.18
                
                
            except:
                response += f"• {item} → Ошибка формата\n"
        
        response += f"\n💰 Итоговая зарплата при 18%: {salary_18:.2f} руб."
        response += f"\n💰 Итоговая зарплата при 14%(без учета скидок): {salary_14_without_discount:.2f} руб."
        response += f"\n💰 Итоговая зарплата при 18%(без учета скидок): {salary_18_without_discount:.2f} руб."
        await update.message.reply_text(response)
        return ConversationHandler.END
    
    def can_access(self, user) -> bool:
        return True