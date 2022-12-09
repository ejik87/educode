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
    btn4 = types.InlineKeyboardButton("Поддержка", callback_data='support', url=config.support_url)
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def services_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Примерка", callback_data='serv_1')
    btn2 = types.InlineKeyboardButton("Закупки", callback_data='serv_2')
    btn3 = types.InlineKeyboardButton("Всякое разное", callback_data='serv_3')
    btn4 = types.InlineKeyboardButton("И многое другое", callback_data='serv_4')
    btn5 = types.InlineKeyboardButton("Назад в главное меню", callback_data='main')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def service_menu():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Условия", callback_data='terms')
    btn2 = types.InlineKeyboardButton("Оформление заказа", callback_data='order')
    btn3 = types.InlineKeyboardButton("Назад в главное меню", callback_data='main')
    markup.add(btn1, btn2, btn3)
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
    if message.chat.type == 'private':
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'Вот тебе ответ!')
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
                case 'serv_1':
                    bot.send_message(call.message.chat.id, text='Примерка', reply_markup=service_menu())
                    # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка1 работает...")
                case 'serv_2':
                    bot.send_message(call.message.chat.id, text='Закупки', reply_markup=service_menu())
                    # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка2 работает...")
                case 'serv_3':
                    bot.send_message(call.message.chat.id, text='Всякое разное', reply_markup=service_menu())
                    # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кнопка3 работает...")
                case 'serv_4':
                    bot.send_message(call.message.chat.id, text='И многое другое', reply_markup=service_menu())
                case 'terms':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='Инфо из списка ' + call.data, reply_markup=service_menu())
                case 'order':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='Инфо из списка ' + call.data, reply_markup=service_menu())
                case 'main':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='Главное меню', reply_markup=main_menu())
                case _:
                    pass

            #     bot.delete_message(chat_id=call.message.chat.id,
            #                        message_id=call.message.message_id)  # Удаляем сообщюху с меню
            #  Удаляем inline клавиатуру меню
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="Выбери какую функцию мне выполнить",
            #                       reply_markup=None)
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
