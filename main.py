from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.helpers import *
from math import floor
import re


def get_driver(data):
    options = Options()

    if "headless" in data:
        options.headless = data["headless"]
    else:
        options.headless = True

    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--blink-settings=imagesEnabled=false")

    prefs = {
        # desativa imagens
        "profile.managed_default_content_settings.images": 2,

        # desativa javascript
        'profile.managed_default_content_settings.javascript': 2,
    }

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe", options=options)
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 3)

    return driver, wait


def login(driver, data):
    print("Logando no moodle...\n")
    driver.get("https://lms.infnet.edu.br/moodle/login/index.php")
    driver.find_element_by_id("username").send_keys(data["username"])
    driver.find_element_by_id("password").send_keys(data["password"], Keys.ENTER)


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


def get_faltas(driver, wait, materia_datas):
    template = "{:<33} {:>8} {:>12} {:>8} {:>9} {:>14} {:>14} {:>14}"

    print("\nPegando dados de frequência...")
    print(template.format("Materia",
                          "Dias",
                          "Freq Atual",
                          "Faltas",
                          "Atrasos",
                          "Não Lançados",
                          "Faltas Disp",
                          "Atrasos Disp"))
    for data in materia_datas:
        get_falta(driver, wait, data, template)


def get_falta(driver, wait, materia_data, template):
    driver.get(materia_data["link"])
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.attendance  a")))
    pauta_url = driver.find_element_by_css_selector("li.attendance  a").get_attribute("href")

    driver.get(f"{pauta_url}&view=5")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "table.attlist tbody tr:last-child td:last-child")))

    dias_web_el = driver.find_elements_by_css_selector("table.generaltable tbody tr")
    atrasos = 0
    faltas = 0
    nao_lancados = 0
    dia_max_pontos = 0
    dias_semana = []

    for idx, dia_row in enumerate(dias_web_el):
        try:
            if idx < 5:
                # pegando dia da semana
                first_col_html = dia_row.find_element_by_css_selector(":first-child").get_attribute("innerHTML")
                dia_semana = first_col_html[first_col_html.find("(")+1:first_col_html.find(")")]\
                    .replace(" ", "")\
                    .lower()
                dias_semana.append(dia_semana)

            # pegando os pontos max do dia
            pontos_list = dia_row.find_element_by_class_name("pointscol").get_attribute("innerHTML") \
                .replace(" ", "") \
                .split("/")

            pontos_max = int(pontos_list[1])

            if pontos_list[0] != '?':
                pontos = int(pontos_list[0])
            else:
                # se os pontos do dias forem '?' o prof ainda nao lançou...
                pontos = pontos_max
                nao_lancados += 1

            if pontos == 0:
                faltas += 1
            elif pontos < pontos_max:
                atrasos += 1

            # definindo o ponto maximo de um dia
            if dia_max_pontos == 0:
                dia_max_pontos = pontos_max
            elif dia_max_pontos != pontos_max:
                print(f"A materia {materia_data['nome']} tem dias com frequencias diferentes, nõa é possivel calcular...")
                return

        except Exception:
            pass

    # Pontuação da frequência:	{pontos_freq} / {pontos_freq_max}
    list_freq_pontos = driver.find_element_by_css_selector("table.attlist tr:nth-last-child(2) td:last-child") \
        .get_attribute("innerHTML") \
        .replace(" ", "") \
        .split("/")

    # Porcentagem de frequência:	{freq_perc}%
    freq_perc = float(driver.find_element_by_css_selector("table.attlist tr:last-child td:last-child")
                      .get_attribute("innerHTML")
                      .replace("%", "")
                      .replace(",", "."))

    pontos_freq, pontos_freq_max = list(map(int, list_freq_pontos))

    # calculando as faltas e atrasos disponiveis
    ponto_por_freq = 100 / pontos_freq_max
    freq_disponivel = freq_perc - 75.0
    pontos_disponiveis = freq_disponivel / ponto_por_freq
    faltas_disponiveis = floor(pontos_disponiveis / dia_max_pontos)
    atrasos_disponiveis = floor(pontos_disponiveis / (dia_max_pontos/2))

    dias_semana = "-".join(set(dias_semana))

    print(template.format(materia_data['nome'],
                          dias_semana,
                          str(freq_perc) + "%",
                          faltas,
                          atrasos,
                          nao_lancados,
                          faltas_disponiveis,
                          atrasos_disponiveis))


def run():
    data = get_data()
    print("Abrindo browser virtual...")
    driver, wait = get_driver(data)

    try:
        login(driver, data)

        escola = get_escola(driver)
        curso = get_curso(driver, escola)
        classe = get_classe(driver, curso)
        bloco = get_bloco(driver, classe)
        materia = get_materia(driver, bloco)
        materia_datas = get_materia_data(materia)

        get_faltas(driver, wait, materia_datas)

    except Exception:
        driver.close()
        raise Exception

    driver.close()


if __name__ == "__main__":
    run()
