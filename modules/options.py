from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from modules.helpers import *
import re

def get_escola(driver):
    escolas = driver.find_elements_by_css_selector("li[aria-labelledby='label_2_8'] > ul > li")

    escolas_sem_institucional = [i for i in escolas if get_nav_text(i) != "Institucional"]

    return select("Escolha uma escola: ", escolas_sem_institucional)


def get_curso(driver, escola):
    cursos = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(escola)}'] > ul > li")

    return select("Escolha um curso: ", cursos)


def get_classe(driver, curso):
    classes = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(curso)}'] > ul > li")

    return select("Escolha uma classe: ", classes)


def get_bloco(driver, classe):
    blocos = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(classe)}'] > ul > li")

    return select("Escolha um bloco: ", blocos)


def get_materia(driver, bloco):
    materias = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(bloco)}'] > ul > li")

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
            .replace("] ", "")

        materia_data.append({
            "nome": nome,
            "link": get_nav_link(materia),
        })

    return materia_data


def get_materia_pauta_url(driver, wait, cache, materia_link):
    """
    Tenta resgatar a link da pauta associado ao link da materia no cache
    Caso nao encontre segue para o driver.get no link da materia
    salvando o link da pauta no cache fornecido
    """

    if materia_link in cache:
        return cache[materia_link]

    driver.get(materia_link)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.attendance  a")))
    cache[materia_link] = driver.find_element_by_css_selector("li.attendance  a").get_attribute("href")
    return cache[materia_link]
