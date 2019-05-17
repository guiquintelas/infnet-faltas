from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from modules.helpers import *
from selenium.webdriver.chrome.options import Options


def login():
    driver.get("https://lms.infnet.edu.br/moodle/login/index.php")
    driver.find_element_by_id("username").send_keys(data["username"])
    driver.find_element_by_id("password").send_keys(data["password"], Keys.ENTER)


def get_escola():
    escolas = driver.find_elements_by_css_selector("li[aria-labelledby='label_2_8'] > ul > li")

    escolas_sem_institucional = [i for i in escolas if get_nav_text(i) != "Institucional"]

    return select("Escolha uma escola: ", escolas_sem_institucional)


def get_curso():
    cursos = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(escola)}'] > ul > li")

    return select("Escolha um curso: ", cursos)


def get_classe():
    classes = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(curso)}'] > ul > li")

    return select("Escolha uma classe: ", classes)


def get_materia():
    materias = driver.find_elements_by_css_selector(f"li[aria-labelledby='{get_nav_label_id(classe)}'] > ul > li")

    materias = [{"name": "Todas", "value": materias}] + materias

    return select("Escolha uma materia: ", materias)


def get_faltas():
    if isinstance(materia, list):
        materias = materia
    else:
        materias = [materia]

    for mat in materias:
        print(get_nav_text(mat))


if __name__ == "__main__":
    data = get_data()

    options = Options()
    options.headless = True
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe", options=options)

    login()
    escola = get_escola()
    curso = get_curso()
    classe = get_classe()
    materia = get_materia()

    get_faltas()

    driver.close()




