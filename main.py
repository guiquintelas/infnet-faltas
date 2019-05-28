from modules.faltas import *
import requests


def get_session_and_index(data):
    print("Logando no moodle...")

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

    session, index_page = get_session_and_index(data)

    escola = get_escola(index_page)
    curso = get_curso(index_page, escola)
    classe = get_classe(index_page, curso)
    bloco = get_bloco(index_page, classe)
    materia = get_materia(index_page, bloco)
    materia_datas = get_materia_data(materia)
    get_faltas(session, materia_datas, cache)

    session.close()


if __name__ == "__main__":
    run()
