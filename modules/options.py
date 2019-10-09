from modules.helpers import *
import requests
import re
from bs4 import BeautifulSoup


def get_escola(index_page: BeautifulSoup):
    escolas = index_page.select("li[aria-labelledby='label_2_8'] > ul > li")

    escolas_sem_institucional = [i for i in escolas if get_nav_text(i) != "Institucional"]

    return select("Escolha uma escola: ", escolas_sem_institucional)


def get_curso(index_page: BeautifulSoup, escola):
    cursos = index_page.select(f"li[aria-labelledby='{get_nav_label_id(escola)}'] > ul > li")

    return select("Escolha um curso: ", cursos)


def get_classe(index_page: BeautifulSoup, curso):
    classes = index_page.select(f"li[aria-labelledby='{get_nav_label_id(curso)}'] > ul > li")

    return select("Escolha uma classe: ", classes)


def get_bloco(index_page: BeautifulSoup, classe):
    blocos = index_page.select(f"li[aria-labelledby='{get_nav_label_id(classe)}'] > ul > li")

    return select("Escolha um bloco: ", blocos)


def get_materia(index_page: BeautifulSoup, bloco):
    materias = index_page.select(f"li[aria-labelledby='{get_nav_label_id(bloco)}'] > ul > li")

    materias = [{"name": "Todas", "value": materias}] + materias

    materia = select("Escolha uma materia: ", materias)

    if isinstance(materia, list):
        materias = materia
    else:
        materias = [materia]

    return materias


def get_materia_data(materias):
    materia_data = []

    for materia in materias:

        # limpando o nome da metria
        nome = get_nav_text(materia).replace("...", "")

        # remove o código prefixo da materia [CDB1782DB] Nome materia
        nome = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", nome)\
            .replace("[", "")\
            .replace("]", "")

        materia_data.append({
            "nome": nome,
            "link": get_nav_link(materia),
        })

    return materia_data


def get_materia_pauta_url(session: requests.Session, cache, materia_link):
    """
    Tenta resgatar a link da pauta associado ao link da materia no cache
    Caso nao encontre segue para o driver.get no link da materia
    salvando o link da pauta no cache fornecido
    """

    if materia_link in cache:
        return cache[materia_link]

    materia_page = parse_html(session, materia_link)
    cache[materia_link] = materia_page.select_one("li.attendance  a").attrs["href"]
    return cache[materia_link]
