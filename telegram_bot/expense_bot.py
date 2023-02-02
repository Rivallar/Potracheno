import telebot
from telebot import types

import bot_settings
import bot_api_calls

bot = telebot.TeleBot(bot_settings.TELEGRAM_TOKEN)


class Expense:

    """Saves expense records temporarily to process data on several steps"""

    def __init__(self, price, comment=None, category=None):
        self.price = price
        self.comment = comment

    def __str__(self):
        return f'{self.price} - {self.comment}'


# dict to store expense records
expenses = {}


def make_buttons(*args, if_inline=False):

    """Makes both Reply and Inline menu buttons"""

    if not if_inline:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.add(*args)
    else:
        markup = types.InlineKeyboardMarkup()
        categories_list = args[0]
        button_list = [types.InlineKeyboardButton(item['title'], callback_data=item['id']) for item in categories_list]
        markup.add(*button_list)
    return markup


def check_for_correct_input(message):

    """Processes expense record message from a user.
    Throw errors if format is incorrect. Returns formatted price and comment otherwise."""

    expense_details = message.text.split(' ', 1)
    price = float("%0.2f" % float(expense_details[0]))
    expense_comment = ''
    if price <= 0:
        raise ValueError
    if len(expense_details) > 1:
        expense_comment = expense_details[1]
    return price, expense_comment


@bot.message_handler(commands=['start'])
def to_start(message, hint='Возвращаюсь в начальное меню'):

    """Returns chat to start point"""

    markup = make_buttons('Внести расходы', 'Добавить категорию', 'Удалить категорию')
    bot.send_message(message.chat.id, hint, reply_markup=markup)


@bot.message_handler(commands=['register'])
def request_phone_number(message):

    """Requests user`s phone to sync him with site"""

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона",
                                        request_contact=True)
    markup.add(button_phone)
    bot.send_message(message.chat.id, 'Для работы бота нужен номер телефона, который ты указал на сайте',
                     reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def site_registration(message):

    """Updates user profile on server with chat_id (for further queries).
    Return text result of operation."""

    phone_number = message.contact.phone_number
    chat_id = message.chat.id
    result = bot_api_calls.update_chat_id(phone_number, chat_id)
    bot.send_message(chat_id, result)


# first step to send expense
def process_expense_record(message):

    """Takes string of expense record, checks the input (must be: 'price optional_comment'),
    creates expense object in expenses dictionary. Then gets expense categories from server and goes to step 2."""

    if message.text == 'Отмена':
        to_start(message)
    else:
        try:
            price, expense_comment = check_for_correct_input(message)
            exp_item = Expense(price=price, comment=expense_comment)
            expenses[message.chat.id] = exp_item
            try:
                categories_dict = bot_api_calls.get_user_categories(message.chat.id)
                if not categories_dict:
                    to_start(message, hint='Не смог получить список категорий расходов. Убедись, '
                                           'что номер телефона зарегистрирован на сайте, и у тебя есть хотя бы одна '
                                           'категория расходов. Для регистрации напиши "/register".')
                else:
                    markup = make_buttons(categories_dict, if_inline=True)
                    markup.add(types.InlineKeyboardButton('Обратно в меню', callback_data='Обратно в меню'))
                    bot.send_message(message.chat.id, 'К какой категории относится эта трата?', reply_markup=markup)
                    bot.register_next_step_handler(message, callback_send_expense_to_server)
            except:
                to_start(message, hint='Ошибка! Не смог получить список категорий расходов. Попробуй позже.')

        except ValueError:
            error_message = 'Неверный формат! Сначала число больше нуля, потом один пробел,' \
                            'потом комментарий, если нужно'
            markup = make_buttons('Отмена')
            bot.send_message(message.chat.id, error_message, reply_markup=markup)
            bot.register_next_step_handler(message, process_expense_record)


# second step to send expense
@bot.callback_query_handler(func=lambda call: True)
def callback_send_expense_to_server(call):

    """Gets info about expense category from a pushed button. Gets expense info from expense dict. Sends data to
    a server."""

    chat = call.message.chat.id

    if expenses.get(chat):
        category = call.data
        if category != 'Обратно в меню':
            bot.answer_callback_query(callback_query_id=call.id, text='Отправка записи на сервер')
            result = bot_api_calls.send_expense_to_server(expenses[chat], category)
            bot.send_message(chat, result)
        del expenses[chat]
        to_start(call.message)
    else:
        to_start(call.message, hint='Эти кнопки уже не работают. Начни сначала')

    bot.answer_callback_query(callback_query_id=call.id, text='Возврат в меню')
    bot.clear_step_handler_by_chat_id(chat_id=chat)


@bot.message_handler(content_types=['text'])
def process_user_text(message):

    """Handles text requests of users."""

    text = message.text.lower()
    if text == 'внести расходы':
        hint = 'Напиши сколько потратил (просто число) и ' \
               'через пробел комментарий (опционально). Например: "5.25 поел в kfc"'
        markup = make_buttons('Отмена')
        bot.send_message(message.chat.id, hint, reply_markup=markup)
        bot.register_next_step_handler(message, process_expense_record)
    elif text == 'добавить категорию':
        bot.send_message(message.chat.id, 'Тут пока ничего нет')
    elif text == 'удалить категорию':
        bot.send_message(message.chat.id, 'Тут пока ничего нет')
    elif text == 'категории':
        categories_dict = bot_api_calls.get_user_categories(message.chat.id)
        markup = make_buttons(categories_dict, if_inline=True)
        bot.send_message(message.chat.id, 'Тут будет список категорий', reply_markup=markup)
    else:
        to_start(message, hint='Не понимаю, нет такой команды. Начни сначала.')


bot.polling(none_stop=True)

