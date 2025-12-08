from telebot import TeleBot
from controllers import Controller
from constants import TOKEN

# Главный файл, запустить для начала работы бота

bot = TeleBot(TOKEN)
controller = Controller(bot)

controller.register_handlers()

if __name__ == "__main__":
    try:
        print("Bot is running...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Ошибка:{e}')