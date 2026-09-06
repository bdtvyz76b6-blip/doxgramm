import telebot
import time
import threading
from engine import get_full_info, BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id,
                     "🔍 Введите номер телефона (только цифры, 10+ символов).\n"
                     "Бот выдаст: оператор, имя (из соцсетей), утечки, банки и др.")

@bot.message_handler(func=lambda m: True)
def handle_phone(message):
    phone = message.text.strip()
    if not phone.isdigit() or len(phone) < 10:
        bot.send_message(message.chat.id, "❌ Только цифры, минимум 10.")
        return

    status = bot.send_message(message.chat.id, "⏳ Сбор данных... (может занять до 30 сек)")
    
    def worker():
        try:
            result = get_full_info(phone)
            bot.edit_message_text(result, chat_id=message.chat.id, message_id=status.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Ошибка: {str(e)}", chat_id=message.chat.id, message_id=status.message_id)
    
    threading.Thread(target=worker).start()

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)