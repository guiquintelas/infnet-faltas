from modules.helpers import *


def get_template(data):
    try:
        if len(data["templates"]) <= 0:
            return False

    except Exception:
        os.remove("data.json")
        print("Erro ao ler o arquivo data.json.")
        print("O arquivo sera deletado e gerado na próxima execução.")
        exit(-1)

    choices = [
        *data["templates"],

        {
            "name": "Criar um novo",
            "value": False
        },
        {
            "name": "Deletar um template",
            "value": "deletar"
        }
    ]

    response = ask_list("Qual template você quer usar?", choices)

    if response == "deletar":
        delete_template(data)
        return get_template(data)

    return response


def delete_template(data):
    # nome de todos os templetes mais o 'Cancelar'
    choices = [
        *[t["name"] for t in data["templates"]],

        {
            "name": "Cancelar",
            "value": False
        }
    ]

    template = ask_list("Qual template você quer deletar?", choices)

    if template:
        # filtra para fora o template escolhido
        data["templates"] = [t for t in data["templates"] if t['name'] != template]
        save_data(data)


def ask_save_template(escola, curso, classe, bloco, materias, data):
    escola = get_nav_text(escola)
    curso = get_nav_text(curso)
    classe = get_nav_text(classe)
    bloco = get_nav_text(bloco)

    save_tmplate = ask("confirm", "Deseja salvar as escolhas para utilizar no futuro?", default=True)

    if save_tmplate:

        while True:
            template_name = ask("input", 'De um nome para o template.')

            # checando se o nome ja existe
            if len([t for t in data["templates"] if t["name"] == template_name]) <= 0:
                break

            print("Esse nome já existe! Por favor escolha outro!")

        novo_template = {
            "name": template_name,
            "value": {
                "escola": escola,
                "curso": curso,
                "classe": classe,
                "bloco": bloco,
                "materias": materias,
            }
        }

        data["templates"].append(novo_template)
