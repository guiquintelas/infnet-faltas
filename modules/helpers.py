from bs4 import BeautifulSoup
from PyInquirer import prompt
import json
import os

dia_semana_order = [
    "seg",
    "ter",
    "qua",
    "qui",
    "sex",
    "sab",
    "dom",
]


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

    return prompt([
        {
            'type': 'list',
            'name': 'select',
            'message': msg,
            'choices': choices
        }
    ])["select"]


def ask_username():
    question = {
        'type': 'input',
        'name': 'username',
        'message': 'Qual seu username no moodle?',
    }

    return prompt(question)["username"]


def ask_password():
    question = {
        'type': 'password',
        'name': 'pass',
        'message': 'Qual sua senha no moodle?',
    }

    return prompt(question)["pass"]


def get_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        print("Seu username e senha serão salvas no arquivo data.json para "
              "\nfacilitar a autenticação na proxima execução.")
        print("Seus dados não são coletados!")

    data = {
        "username": ask_username(),
        "password": ask_password(),
        "templates": []
    }

    return data


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
