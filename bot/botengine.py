from datetime import datetime

from getapi import check_train, get_report


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
