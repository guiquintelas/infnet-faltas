from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from modules.options import *
from modules.helpers import *
from math import floor
from datetime import date


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


def get_faltas(driver, wait, materia_datas, cache):
    template = "{:<33} {:>8} {:>12} {:>8} {:>9} {:>14} {:>14} {:>14}"

    print("\nPegando dados de frequência...")
    print(template.format("Materia",
                          "Dias",
                          "Freq Atual",
                          "Faltas",
                          "Atrasos",
                          "Faltas Disp",
                          "Atrasos Disp",
                          "Não Lançados"))
    for data in materia_datas:
        get_falta(driver, wait, data, template, cache)


def get_falta(driver, wait, materia_data, template, cache):
    pauta_url = get_materia_pauta_url(driver, wait, cache, materia_data["link"])

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
            first_col_html = dia_row.find_element_by_css_selector(":first-child").get_attribute("innerHTML")

            # pegando dia da semana
            if idx < 5:
                dia_semana = first_col_html[first_col_html.find("(") + 1:first_col_html.find(")")] \
                    .replace(" ", "") \
                    .lower()
                dias_semana.append(dia_semana)

            # pegando os pontos max do dia
            pontos_list = dia_row.find_element_by_class_name("pointscol").get_attribute("innerHTML") \
                .replace(" ", "") \
                .split("/")

            pontos_max = int(pontos_list[1])

            if pontos_list[0] == '?':
                # se os pontos do dias forem '?' é calculado como presença
                pontos = pontos_max

                # checando se a data esta no passado, se tiver
                # contabilizar nos dias nao lancados
                dia, mes, ano = first_col_html.split("&nbsp;")[0].split("/")
                if date(int('20' + ano), int(mes), int(dia)) < date.today():
                    nao_lancados += 1
            else:
                pontos = int(pontos_list[0])

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

    # removendo duplicatas
    dias_semana = list(set(dias_semana))

    # ordenando os dias da semana
    dias_semana.sort(key=lambda dia: dia_semana_order.index(dia))

    # convertendo em str delimitador por '-'
    dias_semana = "-".join(dias_semana)

    print(template.format(materia_data['nome'],
                          dias_semana,
                          str(freq_perc) + "%",
                          faltas,
                          atrasos,
                          faltas_disponiveis,
                          atrasos_disponiveis,
                          nao_lancados))


def run():
    data = get_data()
    cache = get_cache()

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

        get_faltas(driver, wait, materia_datas, cache)

    except Exception:
        save_cache(cache)
        driver.close()
        raise Exception

    save_cache(cache)
    driver.close()


if __name__ == "__main__":
    run()
