def check_user(update, context, USERS):
    username = update.effective_chat.username
    name = update.message.chat.first_name
    chat_id = update.effective_chat.id
    if username not in USERS:
        context.bot.send_message(
            chat_id=chat_id,
            text=f'{name} привет! Пользователь не найден. '
                 f'Доступ запрещен.', )
        return False
    return True


def send_me_messege():
    pass


def check_token_time(previos_date):
    pass
