from telebot import TeleBot
from controllers import Controller

# Главный файл, запустить для начала работы бота

bot = TeleBot('8276363231:AAGvbsP7IiV08lPBza7aAV_rjKlE8C8OXTI')
controller = Controller(bot)

controller.register_handlers()

if __name__ == "__main__":
    print("Bot is running...")

    bot.polling(none_stop=True)