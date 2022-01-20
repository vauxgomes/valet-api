#!/usr/bin/env python3

# Author: Vaux Gomes
# Contact: vauxgomes@gmail.com
# Version: 1.0

# Modules
import os
import subprocess
import uuid
import pickle
import logging

from utils import load_data
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Constants
API_VERSION = 'Beta'
API_NAME = 'Valet'

UPLOAD_FOLDER = '.tmp'
LOGGING_FOLDER = 'logs'

JARFILE = 'jar/cicflowmeter.jar'
CLFFILE = 'clf/clf.sav'
LOGFILE = 'logs/flask.log'

COLUMNS = ['Flow IAT Max', 'Fwd IAT Std',
           'Fwd IAT Max', 'Idle Mean', 'Idle Max']

CLASSES = ['BENIGN', 'DoS Hulk', 'DoS slowloris', 
'DoS GoldenEye', 'DoS Slowhttptest', 'Heartbleed']

# Safety
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
if not os.path.isdir(LOGGING_FOLDER):
    os.mkdir(LOGGING_FOLDER)

# -----------------------------------------------------------
# Main objects
# -----------------------------------------------------------

# APP
app = Flask(API_NAME)

# Classifier
clf = pickle.load(open(CLFFILE, 'rb'))

# Logger
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)

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


@app.route('/sys', methods=['GET'])
def sys():
    return jsonify({'version': API_VERSION, 'name': API_NAME})


@app.route('/run', methods=['POST'])
def run():
    logging.info(f'Classification requested on {datetime.now()}')

    if 'file' not in request.files:
        return {'success': False, 'msg': 'File not found'}

    file = request.files['file']
    if not file.filename.endswith('.pcap'):
        return {'success': False, 'msg': 'Wrong extension'}

    _ = secure_filename(file.filename)

    pcap_filename = f'{uuid.uuid1()}-{file.filename}'
    pcap_path = os.path.join(UPLOAD_FOLDER, pcap_filename)
    pcap_flow = f'{pcap_path}_Flow.csv'

    file.save(pcap_path)

    logging.debug(f'Pcap created: {pcap_filename}')

    try:
        # CICFlowMeter Command
        cmd = ['java', '-jar', JARFILE, pcap_path, UPLOAD_FOLDER]

        # Execution
        rel = subprocess.run(cmd, stdout=subprocess.PIPE)

        # Decoding
        rel = rel.stdout.decode('utf-8')

        if not rel.find('is done'):
            return {'success': False, 'msg': 'File not processed'}

        logging.debug(f'Pcap processed: {pcap_filename}')
    except:
        logging.error(f'Error while converting Pcap')

        try:
            os.remove(pcap_path)
            os.remove(pcap_flow)
        except:
            pass

        return {'success': False, 'msg': 'Error while processing your file'}

    # Loading CICFlowMeter's output
    X = load_data(data_path=pcap_flow, columns=COLUMNS)
    logging.debug(f'Flow read: {pcap_filename}')

    # Gettting predictions
    predictions = clf.predict(X)

    # Removing temporary files
    os.remove(pcap_path)
    os.remove(pcap_flow)

    # Return
    return jsonify({
        'success': True,
        'predictions': [CLASSES[i] for i in predictions.tolist()]
    })

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

if __name__ == '__main__':
    app.run()

# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
