from math import floor
from datetime import datetime
from modules.options import *
import requests


def get_faltas(session: requests.Session, materia_datas, cache):
    template = "{:<33} {:>8} {:>8} {:>12} {:>8} {:>9} {:>14} {:>14} {:>14}"

    print("\nPegando dados de frequência...\n")
    print(template.format("Materia",
                          "Dias",
                          "Aulas",
                          "Freq Atual",
                          "Faltas",
                          "Atrasos",
                          "Faltas Disp",
                          "Atrasos Disp",
                          "Não Lançados"))

    erros = {}

    for data in materia_datas:
        erros_materia = get_falta(session, data, template, cache)

        if len(erros_materia) > 0:
            erros[data["nome"]] = erros_materia
            continue

    if len(erros.keys()) > 0:
        print("\nErros de execução...")
        for materia in erros.keys():
            print(materia)

            for erro in erros[materia]:
                print(" - " + erro)


def get_falta(session: requests.Session, materia_data, template, cache):
    pauta_url = get_materia_pauta_url(session, cache, materia_data["link"])

    materia_falta_page = parse_html(session, f"{pauta_url}&view=5")

    dias_web_el = materia_falta_page.select("table.generaltable tbody tr")
    aulas_total = len(dias_web_el)
    aulas_dadas = 0
    atrasos = 0
    faltas = 0
    nao_lancados = 0
    dia_max_pontos = 0
    dias_semana = []

    erros = []

    for idx, dia_row in enumerate(dias_web_el):
        first_col_html = dia_row.select_one("td:nth-of-type(1)").text

        # pegando dia da semana
        if idx < 5:
            dias_semana.append(get_dia_semana(first_col_html))

        # checando se a data esta no passado
        dia, mes, ano = first_col_html.split("\xa0")[0].split("/")
        data_passado = datetime(int('20' + ano), int(mes), int(dia)) < datetime.now()

        if data_passado:
            aulas_dadas += 1

        # pegando os pontos max do dia
        try:
            pontos_list = dia_row.find(attrs={"class": "pointscol"}).text \
                .replace(" ", "") \
                .split("/")

            pontos_max = int(pontos_list[1])
        except Exception:
            erros.append(f"O dia {dia}/{mes}/{ano} não tem a presença disponível! Pulando para o próximo!")
            continue

        if pontos_list[0] == '?':
            # se os pontos do dias forem '?' é calculado como presença
            pontos = pontos_max

            # checando se a data esta no passado, se tiver
            # contabilizar nos dias nao lancados
            if data_passado:
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

    # Pontuação da frequência:	{pontos_freq} / {pontos_freq_max}
    list_freq_pontos = materia_falta_page.select_one("table.attlist tr:nth-of-type(7) td:nth-of-type(2)")\
        .text.replace(" ", "")\
        .split("/")

    # Porcentagem de frequência:	{freq_perc}%
    freq_perc = float(materia_falta_page.select_one("table.attlist tr:nth-of-type(8) td:nth-of-type(2)")
                      .text
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
                          f"{aulas_dadas}/{aulas_total}",
                          str(freq_perc) + "%",
                          faltas,
                          atrasos,
                          faltas_disponiveis,
                          atrasos_disponiveis,
                          nao_lancados))

    return erros


def get_dia_semana(first_col_html):
    return first_col_html[first_col_html.find("(") + 1:first_col_html.find(")")] \
        .replace(" ", "") \
        .lower()
