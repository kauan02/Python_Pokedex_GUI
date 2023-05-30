import requests
import PySimpleGUI as sg
import tempfile
import os
from PIL import Image, ImageTk

meu_tema = {'BACKGROUND': '#383838',
            'TEXT': '#def5fc',
            'INPUT': '#89e3f0',
            'TEXT_INPUT': '#000000',
            'SCROLL': '#0f0f0f',
            'BUTTON': ('#ffffff', '#474747'),
            'PROGRESS': ('#000000', '#FFFFFF'),
            'BORDER': 1,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0}

# Configure o tema personalizado
sg.theme_add_new('MeuTema', meu_tema)

# Aplique o tema personalizado
sg.theme('MeuTema')


def obter_informacoes_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_pokemon = resposta.json()
        nome_pokemon = dados_pokemon['species']['name']
        imagem_url = dados_pokemon['sprites']['front_default']
        habilidades = [habilidade['ability']['name'] for habilidade in dados_pokemon['abilities']]
        estatisticas = []
        for estatistica in dados_pokemon['stats']:
            nome_estatistica = estatistica['stat']['name']
            valor_estatistica = estatistica['base_stat']
            estatisticas.append((nome_estatistica, valor_estatistica))
        return nome_pokemon, imagem_url, habilidades, estatisticas
    else:
        return None


def exibir_informacoes(nome_pokemon, imagem_path, habilidades, estatisticas):
    layout = [
        [sg.Text(f"Name: {nome_pokemon}", font='Helvetica 12 bold')],
        [sg.Image(filename=imagem_path, size=(230, 100))],
        [sg.Text("Skills:", font='Helvetica 12 bold')],
        [sg.Listbox(habilidades, size=(30, len(habilidades)),
                    key='-HABILIDADES-', enable_events=True)],
        [sg.Text("Statistics:", font='Helvetica 12 bold')],
        [sg.Table(values=estatisticas, headings=['Estatística', 'Valor'], auto_size_columns=True, justification='left')]
    ]

    window = sg.Window("Pokémon Information", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()


nome_pokemon = sg.popup_get_text("Enter the name or number of the Pokémon:")

informacoes = obter_informacoes_pokemon(nome_pokemon)

if informacoes:
    nome, imagem_url, habilidades, estatisticas = informacoes
    imagem_temp_file = tempfile.NamedTemporaryFile(delete=False)
    imagem_response = requests.get(imagem_url)
    imagem_temp_file.write(imagem_response.content)
    imagem_temp_file.close()
    exibir_informacoes(nome, imagem_temp_file.name, habilidades, estatisticas)
    os.unlink(imagem_temp_file.name)
else:
    sg.popup("Pokémon not found.")
