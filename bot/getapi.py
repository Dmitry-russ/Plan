import datetime

import requests

from http import HTTPStatus


def get_token(USER_ENDPOINT, USER, PASSWORD) -> str:
    """Функция получения токена для доступа к api."""
    response = requests.post(
        url=USER_ENDPOINT,
        data={'username': USER, 'password': PASSWORD}
    ).json()
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError('Сервер недоступен.')
    return f'Bearer {response.get("access")}'


def check_train(TRAIN_ENDPOINT, API_TOKEN, text) -> list:
    """Проверка наличия запрошенного номера поезда."""
    response = requests.get(
        url=TRAIN_ENDPOINT + f'{text}/',
        headers={'Authorization': API_TOKEN},
    )
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError('Сервер недоступен.')
    return response.json()


def finde_mai(MAI_ENDPOINT, API_TOKEN, text) -> requests:
    """Запрос данных о инспекциях."""
    textchange = text.split()
    response = requests.get(
        url=MAI_ENDPOINT + f'{textchange[0]}/{textchange[1]}/',
        headers={'Authorization': API_TOKEN},
    )
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError('Сервер недоступен.')
    result = response.json()
    if len(result) == 0:
        return 'Инспекций еще не проводилось.'
    result_messege: str = ''
    for res in result:
        train_serial = res.get('train').get('serial').get('serial')
        train_number = res.get('train').get('number')
        mai_data = datetime.datetime.strptime(
            res.get('maintenance_date'), '%Y-%m-%d')
        mai_data = mai_data.strftime("%d.%m.%Y")
        mileage = res.get('mileage')
        mileage = '{0:,}'.format(mileage).replace(',', ' ')
        mai_type = res.get('maintenance').get('type')
        place = res.get('place')
        result_messege += (f'{train_serial}-{train_number} '
                           f'вид: {mai_type} дата: {mai_data} пробег: '
                           f'{mileage} место: {place} \n\n')
    return result_messege
