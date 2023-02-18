import logging
import os
import sys

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, Updater, MessageHandler,
                          Filters)

from getapi import get_token, check_train, finde_mai
from utils import check_user
from consts import TRAIN_ENDPOINT, MAI_ENDPOINT, USER_ENDPOINT, USERS

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

#  получаем доступ к api
#  добавь обработку ошибок!
API_TOKEN = get_token(USER_ENDPOINT, USER, PASSWORD)
logger = logging.getLogger()


def wake_up(update, context):
    """Приветствие при запуске."""

    chat_id = update.effective_chat.id
    name = update.message.chat.first_name
    username = update.effective_chat.username

    access = check_user(update, context, USERS)
    if not access:
        return

    context.bot.send_message(
        chat_id=chat_id,
        text=f'{name} привет! Введи номер поезда. '
             f'Только цифры - дальше я разберусь сам.',
    )
    logging.info(f'User {username}, {chat_id} is starting bot')


def have_massege(update, context):
    """Обработка первичного сообщения о расходе."""

    access = check_user(update, context, USERS)
    if not access:
        return

    chat_id = update.effective_chat.id
    text = update.message.text

    if " " in text:
        result = finde_mai(MAI_ENDPOINT, API_TOKEN, text)
        context.bot.send_message(
            chat_id=chat_id,
            text=result)
        return

    trains = check_train(TRAIN_ENDPOINT, API_TOKEN, text)
    if len(trains) < 1:
        context.bot.send_message(
            chat_id=chat_id,
            text='Поезд не найден.')
        return
    if len(trains) > 1:
        return
    if len(trains) == 1:
        serial = trains[0].get('serial').get('slug')
        text = f'{serial} {text}'
        result = finde_mai(MAI_ENDPOINT, API_TOKEN, text)
        context.bot.send_message(
            chat_id=chat_id,
            text=result)


def check_tokens() -> bool:
    """Проверка наличия переменных в окружении."""

    return all([TELEGRAM_BOT_TOKEN, USER, PASSWORD])


def main():
    """Основная логика работы бота."""

    if not check_tokens():
        logging.critical('There is no data in the environment. '
                         'The function is stopped.')
        raise sys.exit()
    logging.info('Main function is strating.')

    updater = Updater(token=TELEGRAM_BOT_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, have_massege))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.log',
        format=(
            '%(asctime)s, %(levelname)s, %(message)s,'
            '%(name)s, %(funcName)s, %(lineno)d'),
        filemode='a',
    )
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(message)s,'
        '%(name)s, %(funcName)s, %(lineno)d')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    main()
