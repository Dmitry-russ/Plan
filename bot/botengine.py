from datetime import datetime

from getapi import check_train, get_report


def measurement(measurement):
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
                f"расположение: {place}, осталось дней: {days}")

# def get_measurement(METROLOG_ENDPOINT, API_TOKEN, data) -> str:
#     """Запрос данных об одной системе измерения."""
#     response = requests.get(
#         url=METROLOG_ENDPOINT + f'/{data}',
#         headers={'Authorization': API_TOKEN},
#     )
#     check_server(response)
    return messege



def metrolog(measurement):
    """Обработка списка по метрлогии перед выводом."""
    if len(measurement) == 0:
        return 'не найдено'
    messege: str = ''
    for measur in measurement:
        description = measur.get('description')
        seral_number = measur.get('seral_number')
        location = measur.get('location')
        id = measur.get('id')
        messege += f"\n /{id} {location}: {description} (SN: {seral_number})"
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
