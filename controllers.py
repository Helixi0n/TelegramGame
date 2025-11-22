from telebot import types, TeleBot
from models import Model

user_states = {}
user_question = {}
photos, names = Model.get_photo_list_shuffled()
PHOTOS_DIR = 'photos/'
admin_id = 0

class Controller:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            msg = 'Привет! Это игра "Угадай коллегу". Тебе нужно будет угадать своего коллегу по фото из его детства. Для начала напиши своё имя:'

            self.bot.send_message(
                message.chat.id,
                msg
            )
        
        @self.bot.message_handler()
        def name(message):
            Model.add_user(message.chat.id, message.text)

            msg = 'Отлично! Теперь мы можем начать! Как только будете готовы - нажмите на кнопку под сообщением'

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton('Начать!', callback_data='start'))

            self.bot.send_message(
                message.chat.id,
                msg,
                reply_markup=keyboard
            )

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'start')
        def game(callback):
            Model.start_time(callback.message.chat.id)
            user_states[callback.message.chat.id] = iter(photos)

            send_question(callback)

        @self.bot.callback_query_handler(func=lambda callback: callback.data != 'start')
        def handle_answer(callback):
            answer = callback.data
            right_answer = user_question[callback.message.chat.id]

            Model.add_score(callback.message.chat.id, answer, right_answer)
            del user_question[callback.message.chat.id]
            send_question(callback)
    
        def send_question(callback):
            try:
                photo = next(user_states[callback.message.chat.id])
                keyboard = types.InlineKeyboardMarkup(row_width=1)

                for name in names:
                    keyboard.add(types.InlineKeyboardButton(text=name, callback_data=name))

                user_question[callback.message.chat.id] = photo.split('.')[0]

                with open(PHOTOS_DIR + photo, "rb") as photo:
                    self.bot.send_photo(
                        callback.message.chat.id,
                        photo=photo,
                        reply_markup=keyboard
                    )
    
            except StopIteration:
                    Model.end_time(callback.message.chat.id)
                    compl = Model.delta_time(callback.message.chat.id)
                    score = Model.get_score(callback.message.chat.id)
                    user = Model.get_user(callback.message.chat.id)
                    self.bot.send_message(
                        callback.message.chat.id, 
                        f"Тест завершен! Результат {score}/{len(names)}. Время прохождения {compl}"
                        )
                    
                    self.bot.send_message(
                        admin_id,
                        f'{user} прошел (-а) тест за {compl}. Результат: {score}/{len(names)}'
                    )