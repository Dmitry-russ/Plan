import datetime

from getapi import check_train, get_summerwinter


def summerwinter(update, context, text,
                 TRAIN_ALL_ENDPOINT, MAI_ENDPOINT, API_TOKEN):
    chat_id = update.effective_chat.id
    text = 'summer'
    summer_mai = get_summerwinter(MAI_ENDPOINT, API_TOKEN, text)
    text = None
    trains = check_train(TRAIN_ALL_ENDPOINT, API_TOKEN, text)

    messege: str = ('Отчет по переводам в лето:'
                    '\nСерия-номер вид дата комментарий')
    for train in trains:
        serial = train.get('serial').get('serial')
        number = train.get('number')
        for mai in summer_mai:
            if train.get('id') == mai.get('train').get('id'):
                maintenance_date = datetime.datetime.strptime(
                    mai.get('maintenance_date'), '%Y-%m-%d')
                maintenance_date = maintenance_date.strftime("%d.%m.%Y")
                comment = mai.get('comment')
                if comment is None:
                    comment = 'нет комментария'
                messege += (f'\n{serial}-{number} '
                            f'Лето {maintenance_date} ({comment})')
                break
        else:
            messege += f'\n{serial}-{number} - - -'

    context.bot.send_message(
        chat_id=chat_id,
        text=messege)
