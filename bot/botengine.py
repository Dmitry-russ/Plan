from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from consts import CERTIFICATES_ENDPOINT
from getapi import check_train, get_report, get_certificates, get_metrolog

DAYS_LIMIT_METROLOG = 10


def measurement(measurement, API_TOKEN):
    """Обработка одной системы измерения."""
    messege: str = ''
    description = measurement.get('description')
    seral_number = measurement.get('seral_number')
    location = measurement.get('location')
    id = measurement.get('id')
    file = measurement.get('file')
    days = measurement.get('days')
    place = measurement.get('place')
    messege += (f"\n /{id} {location}: {description} (SN: {seral_number}), "
                f"расположение: {place}, осталось дней: {days}.")
    keyboard: list = []
    if file:
        keyboard.append([InlineKeyboardButton(
            "Посмотреть фото",
            callback_data=file)])
    if get_certificates(id, CERTIFICATES_ENDPOINT, API_TOKEN):
        keyboard.append([InlineKeyboardButton(
            "Посмотреть сертификат",
            callback_data=f'поиск сертификата {id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(keyboard) == 0:
        reply_markup = None
    return messege, reply_markup


def metrolog(measurement):
    """Обработка списка по метрлогии перед выводом."""
    if len(measurement) == 0:
        return 'СИ не найдено.'
    messege: str = ''
    location_pre: str = ''
    for measur in measurement:
        description = measur.get('description')
        seral_number = measur.get('seral_number')
        location = measur.get('location')
        id = measur.get('id')
        days = measur.get('days')
        if location_pre != location and location_pre != "":
            messege += '\n--------------------'
        if int(days) < DAYS_LIMIT_METROLOG:
            messege += (f"\n /{id} <code><b>{location}: {description} "
                        f"(SN: {seral_number}), дней: {days}</b></code>")
        else:
            messege += (f"\n /{id} {location}: {description} "
                        f"(SN: {seral_number}), дней: {days}")
        location_pre = location
    return messege


def summerwinter(update, context, text,
                 TRAIN_ALL_ENDPOINT, MAI_ENDPOINT, API_TOKEN):
    chat_id = update.effective_chat.id
    info_mai = get_report(MAI_ENDPOINT, API_TOKEN, text)
    trains = check_train(TRAIN_ALL_ENDPOINT, API_TOKEN, None)
    choose_report: dict = {'winter': 'переводам в зиму',
                           'summer': 'переводам в лето',
                           '30days': '30 суточным постановкам', }
    messege: str = (f'Отчет по {choose_report.get(text)}:'
                    '\nСерия-номер вид дата комментарий')
    for train in trains:
        serial = train.get('serial').get('serial')
        number = train.get('number')
        for mai in info_mai:
            if train.get('id') == mai.get('train').get('id'):
                maintenance_date = datetime.strptime(
                    mai.get('maintenance_date'), '%Y-%m-%d')
                maintenance_date = maintenance_date.strftime("%d.%m.%Y")
                comment = mai.get('comment')
                mai_type = mai.get('maintenance').get('type')
                if comment is None:
                    comment = '-'
                if text == '30days':
                    maintenance_date_calk = datetime.strptime(
                        str(maintenance_date), "%d.%m.%Y")
                    current_date = datetime.strptime(
                        str(datetime.now().date()), '%Y-%m-%d')
                    counter = current_date - maintenance_date_calk
                    counter = 30 - counter.days
                    counter = 0 if counter < 0 else counter
                    messege += (f'\n{serial}-{number} '
                                # f'{mai_type} {maintenance_date} '
                                f'осталось дней {counter}')
                    break
                messege += (f'\n{serial}-{number} '
                            f'{mai_type} {maintenance_date} '
                            f'({comment})')
                break
        else:
            messege += f'\n{serial}-{number} - - -'

    context.bot.send_message(
        chat_id=chat_id,
        text=messege)


def metrolog_list(context, chat_id, METROLOG_ENDPOINT, API_TOKEN, data):
    """Поиск и вывод в бот списка сертификатов."""
    result = get_metrolog(METROLOG_ENDPOINT, API_TOKEN, data)
    result_text = metrolog(result)
    context.bot.send_message(
        chat_id=chat_id,
        text=result_text,
        parse_mode=ParseMode.HTML, )
