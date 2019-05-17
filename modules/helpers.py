from PyInquirer import prompt
import json


def select(msg, navs):
    choices = []

    for nav in navs:
        if isinstance(nav, dict):
            choices.append(nav)
        else:
            choices.append({"name": get_nav_text(nav), "value": nav})

    return prompt([
        {
            'type': 'list',
            'name': 'select',
            'message': msg,
            'choices': choices
        }
    ])["select"]


def get_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        print("Erro ao ler o arquivo data.json! Você renomeou o data.json-example")
        exit(-1)


def get_nav_text(nav):
    return nav.find_element_by_tag_name("a").get_attribute("innerHTML")


def get_nav_label_id(nav):
    return nav.get_attribute("aria-labelledby")
