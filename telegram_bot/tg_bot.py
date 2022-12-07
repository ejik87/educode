import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TG_TOKEN)  # Создадим экземпляр бота


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Меню", callback_data='menu1')
    btn2 = types.InlineKeyboardButton("Ещё меню", callback_data='menu2')
    btn3 = types.InlineKeyboardButton("И тут меню", callback_data='menu3')
    btn4 = types.InlineKeyboardButton("закрыть всё это", callback_data='menu4')
    markup.add(btn1, btn2, btn3, btn4)

    # sticker01 = open('static/welcome.webp', 'rb')  # Открываем изображение для стикера режим чтения байтовый
    # bot.send_sticker(message.chat.id, sticker01)  # Функция отправки стикера отправителю команды
    bot.send_message(message.chat.id,
                     f"Добро пожаловать, {message.from_user.first_name}!\nЯ - <b>{bot.get_me().first_name}</b>, бот созданный чтобы быть подопытным кроликом.",
                     parse_mode='html')
    bot.send_message(message.chat.id, 'Выбери какую функцию мне выполнить', reply_markup=markup)


@bot.message_handler(content_types=['text'])  # Ответы на текстовые сообщения
def respond_foo(message):
    if message.chat.type == 'ptivate':
        if message.text == 'Ответ1':
            bot.send_message(message.chat.id, str(1))
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline_menu(call):
    try:
        if call.message:
            match call.data:
                case 'menu1':
                    bot.send_message(call.message.chat.id, 'ТЫ выбрал меню №1 😊')
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Воу! Ты нажал меню 1!")
                case 'menu2':
                    bot.send_message(call.message.chat.id, 'ТЫ выбрал меню №2 😊')
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Воу! Ты нажал меню 2!")  # show_alert=True Даёт окно с сообщением
                case 'menu3':
                    bot.send_message(call.message.chat.id, 'ТЫ выбрал меню №3 😊')
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Воу! Ты нажал меню 3!")
                case 'menu4':
                    # bot.send_message(call.message.chat.id, 'ТЫ выбрал меню №4 😊')
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  # Удаляем сообщюху с меню
                    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                    #                       text="Выбери какую функцию мне выполнить",
                    #                       reply_markup=None)
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Воу! Ты нажал Закрыть это")
                case _:
                    pass
            #  Удаляем inline клавиатуру меню
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="Выбери какую функцию мне выполнить",
            #                       reply_markup=None)
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
