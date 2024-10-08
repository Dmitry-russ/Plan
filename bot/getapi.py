import datetime
from http import HTTPStatus
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests

from utils import case_buttons


def check_server(response):
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError('Ошибка обработки запроса на сервере.'
                              'Попробуйте повторить запрос.')


def get_token(USER_ENDPOINT, USER, PASSWORD) -> str:
    """Функция получения токена для доступа к api."""
    response = requests.post(
        url=USER_ENDPOINT,
        data={'username': USER, 'password': PASSWORD}
    )
    check_server(response)
    return f'Bearer {response.json().get("access")}'


def user_telegram(MAI_USERDATA_ENDPOINT, API_TOKEN, user) -> list:
    """Запрос наличия пользователя."""
    response = requests.get(
        url=MAI_USERDATA_ENDPOINT + f'{user}/',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def get_report(MAI_ENDPOINT, API_TOKEN, text) -> str:
    """Запрос выполненных переводов в лето или зиму."""
    response = requests.get(
        url=MAI_ENDPOINT + f'{text}/',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def get_photo(url, API_TOKEN) -> str:
    """Запрос фото системы измерения."""
    photo_endpoint = f'http://194.187.122.3{url[15:]}'
    response = requests.get(
        url=photo_endpoint,
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.content


def get_file(url, API_TOKEN) -> str:
    """Запрос файла сертификата системы измерения."""
    url_parsed = urlparse(url)
    file_path = Path(
        "/metrolog/") / unquote(Path(url_parsed.path).name)
    document = open(file_path, 'rb', )
    return document


def get_certificates(id, CERTIFICATES_ENDPOINT, API_TOKEN) -> str:
    """Запрос списка сертификатов."""
    url = f'{CERTIFICATES_ENDPOINT}{id}/'
    response = requests.get(
        url=url,
        headers={'Authorization': API_TOKEN},
        stream=True,
    )
    check_server(response)
    return response.json()


def get_measurement(METROLOG_ENDPOINT, API_TOKEN, data) -> str:
    """Запрос данных об одной системе измерения."""
    response = requests.get(
        url=METROLOG_ENDPOINT + f'/{data}',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def get_metrolog(METROLOG_ENDPOINT, API_TOKEN, data) -> str:
    """Запрос данных о системах измерения."""
    response = requests.get(
        url=METROLOG_ENDPOINT + f'?search={data}',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def check_train(TRAIN_ENDPOINT, API_TOKEN, text) -> list:
    """Проверка наличия запрошенного номера поезда."""
    if text:
        response = requests.get(
            url=TRAIN_ENDPOINT + f'{text}/',
            headers={'Authorization': API_TOKEN},
        )
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        check_server(response)
        return response.json()
    response = requests.get(
        url=TRAIN_ENDPOINT,
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def next_mai_num(MAI_NEXT_ENDPOINT, API_TOKEN, number) -> list:
    """Поиск следующего ТО."""
    response = requests.get(
        url=MAI_NEXT_ENDPOINT + f'{number}/',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    return response.json()


def finde_mai(MAI_ENDPOINT, MAI_NEXT_ENDPOINT, API_TOKEN, text) -> requests:
    """Запрос данных о инспекциях."""
    textchange = text.split()
    response = requests.get(
        url=MAI_ENDPOINT + f'{textchange[0]}/{textchange[1]}/',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    result = response.json()
    # проверка на отсутвие инспекций
    if len(result) == 0:
        result_messege = 'Инспекций еще не проводилось.'
        reply_markup = case_buttons(textchange[0],
                                    textchange[1],
                                    textchange[0], )
        return result_messege, reply_markup

    result_messege: str = ''

    # смотрю следующую инспекцию
    next_mai = None
    for res in result:
        number_mai = res.get('maintenance').get('number')
        if number_mai is not None:
            number_mai = int(number_mai) + 1
            next_mai = next_mai_num(MAI_NEXT_ENDPOINT, API_TOKEN, number_mai)
            break

    first_run_check = True
    for res in result:
        if first_run_check:
            if next_mai:
                next_mai = next_mai[0].get('type')
            train_serial_slug = res.get('train').get('serial').get('slug')
            train_serial = res.get('train').get('serial').get('serial')
            train_number = res.get('train').get('number')
            train_mileage = res.get('train').get('mileage')
            if train_mileage:
                train_mileage = '{0:,}'.format(train_mileage).replace(',', ' ')
            train_mileage_date = res.get('train').get('mileage_date')
            if train_mileage_date:
                train_mileage_date = datetime.datetime.strptime(
                    res.get('train').get('mileage_date'), '%Y-%m-%d')
                train_mileage_date = train_mileage_date.strftime("%d.%m.%Y")
            train_renter = res.get('train').get('renter')
            result_messege += f'{train_serial}-{train_number} \n'
            result_messege += f'Арендатор: {train_renter} \n'
            result_messege += (f'Пробег: {train_mileage} на дату: '
                               f'{train_mileage_date} \n')
            result_messege += f'Следующее ТО: {next_mai} \n\n'

        first_run_check = False
        mai_data = datetime.datetime.strptime(
            res.get('maintenance_date'), '%Y-%m-%d')
        mai_data = mai_data.strftime("%d.%m.%Y")
        mileage = res.get('mileage')
        mileage = '{0:,}'.format(mileage).replace(',', ' ')
        mai_type = res.get('maintenance').get('type')
        place = res.get('place')
        result_messege += f'Вид ТО: {mai_type}\n'
        if train_mileage:
            mileage_diff = (int(res.get('train').get('mileage')) -
                            int(res.get('mileage')))
            mileage_diff = '{0:,}'.format(mileage_diff).replace(',', ' ')
            result_messege += f' пробег от ТО: {mileage_diff}\n'
        result_messege += (f' дата: {mai_data}\n пробег:'
                           f' {mileage}\n место: {place}\n\n')
        reply_markup = case_buttons(train_serial,
                                    train_number,
                                    train_serial_slug, )
    return result_messege, reply_markup


def finde_case(CASE_ENDPOINT, API_TOKEN, text):
    textchange = text.split()
    textchange.pop()
    response = requests.get(
        url=CASE_ENDPOINT + f'{textchange[0]}/{textchange[1]}/',
        headers={'Authorization': API_TOKEN},
    )
    check_server(response)
    result = response.json()
    result_messege: str = ''
    if len(result) == 0:
        return 'Нет замечаний'
    for res in result:
        name = res.get('name')
        result_messege += f'{name}\n'
    return result_messege
