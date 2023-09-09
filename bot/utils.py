from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def check_user(update, context, USERS):
    username = update.effective_chat.username
    name = update.message.chat.first_name
    if username not in USERS:
        raise ConnectionError(f'{name} привет! Пользователь не найден. '
                              f'Доступ запрещен.')


def case_buttons(serial_serial, train_number, serial_slug, ):
    keyboard: list = []
    keyboard.append([InlineKeyboardButton(
        f"{serial_serial}-{train_number}",
        callback_data=f'{serial_slug} {train_number} case')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def send_me_messege(context, MY_CHAT_ID, messege):
    """Отправка сообщения в мой чат."""
    context.bot.send_message(
        chat_id=MY_CHAT_ID,
        text=messege,
    )


def check_token_time(previos_date):
    pass
