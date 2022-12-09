import telebot
import logging
import config
from telebot import types

bot = telebot.TeleBot(config.TG_TOKEN)  # Создадим экземпляр бота


def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("О нас", callback_data='about')
    btn2 = types.InlineKeyboardButton("Список услуг", callback_data='services')
    btn3 = types.InlineKeyboardButton("Мои заказы", callback_data='orders')
    btn4 = types.InlineKeyboardButton("Поддержка", callback_data='support')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def services_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Примерка", callback_data='serv_1')
    btn2 = types.InlineKeyboardButton("Закупки", callback_data='serv2')
    btn3 = types.InlineKeyboardButton("Всякое разное", callback_data='serv3')
    btn4 = types.InlineKeyboardButton("И многое другое", callback_data='serv4')
    btn5 = types.InlineKeyboardButton("Назад в главное меню", callback_data='main')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def orders_info():
    ...


def back_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Назад в главное меню", callback_data='main')
    markup.add(btn1)
    return markup


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    # sticker01 = open('static/welcome.webp', 'rb')  # Открываем изображение для стикера режим чтения байтовый
    # bot.send_sticker(message.chat.id, sticker01)  # Функция отправки стикера отправителю команды
    bot.send_message(message.chat.id,
                     f"Добро пожаловать, {message.from_user.first_name}!\nЯ - <b>{bot.get_me().first_name}</b>, бот созданный чтобы быть подопытным кроликом.",
                     parse_mode='html')
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=main_menu())


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
                case 'about':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Раздел О нас!\nМы хорошие и красивые и воообще очень классные\nСвязь с нами по телеграмму тут!",
                                          reply_markup=main_menu())
                case 'services':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Вот список наших услуг: Тратататата", reply_markup=services_menu())
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Ознакомьтесь с услугами и выберите подходящую")  # show_alert=True Даёт окно с сообщением
                case 'orders':
                    # show alert
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ваши данные загружаются...")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Вот история ваших заказов", reply_markup=main_menu())
                case 'support':
                    # bot.send_message(call.message.chat.id, 'ТЫ выбрал меню №4 😊')
                    bot.delete_message(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id)  # Удаляем сообщюху с меню
                    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                    #                       text="Выбери какую функцию мне выполнить",
                    #                       reply_markup=None)
                    bot.get_chat(config.chat_id)
                case 'serv_1':
                    print(call.message.chat.id)
                    print(call.message.message_id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="1", reply_markup=back_menu())
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка1 работает...")
                case 'serv_2':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="2", reply_markup=back_menu())
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка2 работает...")
                case 'serv_3':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="3", reply_markup=back_menu())
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка3 работает...")
                case 'serv_4':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="4", reply_markup=back_menu())
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка4 работает...")
                case 'main':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='Главное меню', reply_markup=main_menu())
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
