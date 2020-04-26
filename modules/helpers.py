from bs4 import BeautifulSoup
from PyInquirer import prompt
import json
import os

from prompt_toolkit.terminal.win32_output import NoConsoleScreenBufferError

dia_semana_order = [
    "seg",
    "ter",
    "qua",
    "qui",
    "sex",
    "sab",
    "dom",
]


def ask(ask_type, message,  choices=None, default=None):
    opts = {
        'type': ask_type,
        'name': "response",
        'message': message
    }

    if default is not None:
        opts["default"] = default

    if choices:
        opts["choices"] = choices

    try:
        response = prompt([opts], keyboard_interrupt_msg="Tchau Tchau!")
    except NoConsoleScreenBufferError:
        print("Esse console não é suportado! :( \nSe estiver no windows use o cmd ou cmder")
        exit(-1)

    if not response:
        exit()

    return response["response"]


def ask_list(message, choices):
    return ask("list", message, choices)


def select(msg, navs):
    choices = []

    for nav in navs:
        if isinstance(nav, dict):
            choices.append(nav)
        else:
            choices.append({
                "name": get_nav_text(nav),
                "value": nav
            })

    while len(msg) < 21:
        msg += " "

    return ask_list(msg, choices)


def ask_username():
    return ask("input", 'Qual seu username no moodle?')


def ask_password():
    return ask("password", 'Qual sua senha no moodle?')


def get_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)

        # if data.json file exists and is valid
        # but username or password are not set
        if "username" not in data or "password" not in data:
            return {
                **ask_credentials(),
                "templates": data["templates"]
            }

        # data.json exists and is valid
        return data
    except Exception:
        pass

    # data.json file doesn't exist or is invalid
    return {
        **ask_credentials(),
        "templates": []
    }


def ask_credentials():
    print("Seu username e senha serão salvos no arquivo data.json para "
          "\nfacilitar a autenticação na proxima execução.")
    print("Seus dados não são coletados!")

    return {
        "username": ask_username(),
        "password": ask_password()
    }


def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_cache():
    try:
        with open('cache.json', 'r') as f:
            return json.load(f)
    except:
        pass

    return {}


def save_cache(cache):
    try:
        with open('cache.json', 'w') as f:
            json.dump(cache, f, indent=4)
    except:
        print("Erro ao salvar cache...")


def get_nav_text(nav: BeautifulSoup):
    return nav.select_one("a").text


def get_nav_label_id(nav):
    return nav.attrs["aria-labelledby"]


def get_nav_link(nav: BeautifulSoup):
    return nav.find("a").attrs["href"]


def get_res(res):
    return BeautifulSoup(res.text, 'html.parser')


def parse_html(session, url):
    res = session.get(url)
    return BeautifulSoup(res.text, 'html.parser')
