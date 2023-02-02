import requests

import bot_settings

SITE_URL = bot_settings.SITE_URL


def get_user_categories(chat_id):

    """Takes user expense categories from a server. Lookup performed by chat_id."""

    endpoint = f'{SITE_URL}/api/user_categories/{chat_id}'
    response = requests.get(endpoint)
    return response.json()


def send_expense_to_server(expense, category_id):

    """Adds expense record on server based on expense category.
    Returns text result of operation."""

    endpoint = f'{SITE_URL}/api/add_expense/'
    data = {'category': category_id, 'price': expense.price, 'comment': expense.comment}
    response = requests.post(endpoint, data=data)
    if response.status_code == 201:
        return 'Запись успешно добавлена'
    return 'Ошибка! Запись не внесена. Попробуй позже.'


def update_chat_id(phone, chat_id):

    """Adds/updates chat_id in user profile on server.
    Returns text result of operation."""

    endpoint = f'{SITE_URL}/api/update_chat_id/{phone}'
    data = {'telegram_chat_id': chat_id}
    try:
        response = requests.put(endpoint, data=data)
        if response.status_code == 200:
            return 'Номер телефона успешно привязан к аккаунту.'
        elif response.status_code == 404:
            return 'Ошибка! Нет аккаунта с таким телефонным номером.'
    except requests.exceptions.ConnectionError:
        return 'Ошибка! Что-то сломалось. Попробуй позже.'
