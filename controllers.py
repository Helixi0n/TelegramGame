from telebot import types, TeleBot
from models import Model
from constants import ADMIN_ID

user_states = {}
user_question = {}
photos, names = Model.get_photo_list_shuffled()
PHOTOS_DIR = 'photos/'

class Controller:
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            if Model.get_user(message.chat.id):
                Model.zero_score(message.chat.id)
                msg = 'Как только будете готовы - нажмите на кнопку под сообщением'

                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(types.InlineKeyboardButton('Начать!', callback_data='start'))

                self.bot.send_message(
                    message.chat.id,
                    msg,
                    reply_markup=keyboard
                )

            else:
                msg = 'Приближается Новый год - волшебный и всеми любимый праздник. И в это время мы мысленно возвращаемся в детство, вспоминая, как мы украшали елку и ждали деда Мороза с подарками.\nС помощь ИИ мы вернули наших коллег в детство. Предлагаем Вам их угадать!\nДля начала напиши своё имя:'

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

        @self.bot.callback_query_handler(func=lambda callback: callback.data.startswith('ans_'))
        def handle_answer(callback):
            key = callback.data.strip('ans_')
            answer = names.get(key)
            right_answer = user_question[callback.message.chat.id]

            Model.add_score(callback.message.chat.id, answer, right_answer)
            del user_question[callback.message.chat.id]
            send_question(callback)
    
        def send_question(callback):
            try:
                photo = next(user_states[callback.message.chat.id])
                keyboard = types.InlineKeyboardMarkup(row_width=1)

                correct_answer = photo.split('.')[0]
                user_question[callback.message.chat.id] = correct_answer

                answer_options = Model.get_five_shuffled(correct_answer, names)
                buttons = []
                
                for key in answer_options:
                    buttons.append(types.InlineKeyboardButton(
                        text=names[key], 
                        callback_data=f'ans_{key}'
                    ))
                
                keyboard.add(*buttons)

                with open(PHOTOS_DIR + photo, "rb") as photo_file:
                    self.bot.send_photo(
                        callback.message.chat.id,
                        photo=photo_file,
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
                        ADMIN_ID,
                        f'{user} прошел (-а) тест за {compl}. Результат: {score}/{len(names)}'
                    )