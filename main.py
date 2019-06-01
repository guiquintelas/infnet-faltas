from modules.faltas import *
from modules.templates import *
import requests


def get_session_and_index(data):
    print("\nLogando no moodle...")

    session = requests.Session()

    # pegando logintoken
    soup = parse_html(session, "https://lms.infnet.edu.br/moodle/login/index.php")
    token = soup.find("input", {"name": "logintoken"}).attrs["value"]

    payload = {
        "username": data["username"],
        "password": data["password"],
        "logintoken": token
    }

    res = get_res(session.post("https://lms.infnet.edu.br/moodle/login/index.php", payload))

    return session, res


def run():
    data = get_data()
    cache = get_cache()
    template = get_template(data)

    if template:
        print("\nDados do template:")
        print(f"Escola: {template['escola']}")
        print(f"Curso:  {template['curso']}")
        print(f"Classe: {template['classe']}")
        print(f"Bloco:  {template['bloco']}")

    # logando...
    session, index_page = get_session_and_index(data)

    if not template:
        escola = get_escola(index_page)
        curso = get_curso(index_page, escola)
        classe = get_classe(index_page, curso)
        bloco = get_bloco(index_page, classe)
        materia = get_materia(index_page, bloco)
        materia_datas = get_materia_data(materia)
        ask_save_template(escola, curso, classe, bloco, materia_datas, data)

    else:
        materia_datas = template["materias"]

    get_faltas(session, materia_datas, cache)
    save_data(data)

    session.close()


if __name__ == "__main__":
    run()
