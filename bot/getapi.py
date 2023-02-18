import requests


def get_token(USER_ENDPOINT, USER, PASSWORD) -> str:
    """Функция получения токена для доступа к api."""

    response = requests.post(
        url=USER_ENDPOINT,
        data={'username': USER, 'password': PASSWORD}
    ).json()
    return f'Bearer {response.get("access")}'


def check_train(TRAIN_ENDPOINT, API_TOKEN, text) -> list:
    """Проверка наличия запрошенного номера поезда."""

    response = requests.get(
        url=TRAIN_ENDPOINT + f'{text}/',
        headers={'Authorization': API_TOKEN},
    )
    return response.json()


def finde_mai(MAI_ENDPOINT, API_TOKEN, text) -> requests:
    """Запрос данных о всех сохраненных расходах пользователя."""
    textchange = text.split()
    response = requests.get(
        url=MAI_ENDPOINT+f'{textchange[0]}/{textchange[1]}/',
        headers={'Authorization': API_TOKEN},
        )
    # добавить обратботку 404 и 500 ошибок сервера
    return response.json()
