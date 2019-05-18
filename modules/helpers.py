from PyInquirer import prompt
import json


def select(msg, navs):
    choices = []

    for nav in navs:
        if isinstance(nav, dict):
            choices.append(nav)
        else:
            choices.append({"name": get_nav_text(nav), "value": nav})

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
        'message': 'Qual seu username moodle?',
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
        print("Não foi encontrado o arquivo data.json. Criando um padrão...")
        print("Seu username e passwprd serão salvas no arquivo data.json.")
        print("Seus dados não são coletados!")

    data = {
        "username": ask_username(),
        "password": ask_password(),
        "headless": True,
        "escola": False,
        "curso": False,
        "classe": False,
        "bloco": False,
        "materia": False,
    }

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    return data


def get_nav_text(nav):
    return nav.find_element_by_tag_name("a").get_attribute("innerHTML")


def get_nav_label_id(nav):
    return nav.get_attribute("aria-labelledby")


def get_nav_link(nav):
    return nav.find_element_by_tag_name("a").get_attribute("href")
