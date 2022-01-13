# Modules
import os
import subprocess
import uuid
import json

from flask import Flask, request, jsonify

# Constants
API_VERSION = 'Beta'
API_NAME = 'Valet'
API_OUTPUT_DIR = '.tmp/'
JARFILE = 'jar/dummy.jar'

# APP
app = Flask(API_NAME)

# Segurança
if not os.path.isdir(API_OUTPUT_DIR):
    os.mkdir(API_OUTPUT_DIR)

# -----------------------------------------------------------
# Routes
# -----------------------------------------------------------


@app.route('/help', methods=['GET'])
def help():
    return jsonify({
        'lang': 'pt-BR',
        'endpoints': {
            '/help': {
                'args': None,
                'desc': 'Exibe esta mensagem de ajuda'
            },

            '/sys': {
                'args': None,
                'desc': 'Nome e versão da API'
            },

            '/run': {
                'args': {
                    'data': {
                        'type': 'array',
                        'desc': 'Instância para classificação'
                    }
                },
                'desc': 'Classifica uma intância retornando uma das classes: A B C D'
            },
        }
    })


@app.route('/', methods=['GET'])
def sys():
    return jsonify({'version': API_VERSION, 'name': API_NAME})


@app.route('/run', methods=['POST'])
def run():
    # Arquivo temporário
    temp = f'{API_OUTPUT_DIR}{uuid.uuid1()}.tmp'

    # Carregando array de argumentos do CICFlowMeter
    instance = json.loads(request.data.decode('utf-8'))

    # Salvando instância em arquivo
    with open(temp, 'w') as handler:
        handler.write(','.join(instance))

    # Log
    print(f'[LOG]: Instância: {instance}')
    print(f'[LOG]: Arquivo: {temp}')

    # Montando o comando que chama o CICFlowMeter
    cmd = ['java', '-jar', JARFILE]
    cmd.extend(instance)  # Argumentos do CICFlowMeter

    # Executando o comando
    rel = subprocess.run(cmd, stdout=subprocess.PIPE)

    # Tratamento da saída
    rel = rel.stdout.decode('utf-8')
    rel = rel.strip().split('\n')  # TODO

    # Chamando o classificador
    CLS = None

    # Removendo arquivos temporários
    os.remove(temp)

    # Retorno para o usuário
    return jsonify({'res': rel})

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------


if __name__ == '__main__':
    app.run()
