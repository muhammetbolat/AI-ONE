from flask import Flask, request, jsonify
import json
import pandas as pd
import numpy as np
import pickle
import os
import logging as log
import yaml

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "application_conf.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

########################################################################################################################
API_PORT = cfg['API']['PORT']
API_ROUTE = cfg['API']['NAME']

########################################################################################################################
ANN_MODEL_FILE = cfg['ANN']['MODEL_FILE']
ONE_HOT_MODEL_FILE = cfg['ANN']['ONE_HOT_MODEL_FILE']

########################################################################################################################
modelsPath = cfg['OTHER']['MODEL_PATH']

########################################################################################################################
# Data Features
INPUT_FEATURES = cfg['FEATURES']['INPUT_FORMAT']

app = Flask(__name__)


def log_init(log_file):
    """
    initiliazation of log file.
    """
    log.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file),
                    filemode='a',
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log.DEBUG)


def doTheOneHotEncode(data):
    """
    This global function calculate to one-hot encode correspoing to the one-hote model.
    """
    model = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          modelsPath + ONE_HOT_MODEL_FILE), 'rb'))

    features = INPUT_FEATURES.split(',')

    X = np.array(data[features])
    val = model.transform(X).toarray()

    return val

@app.route(API_ROUTE, methods=['POST'])
def makecalc():
    """
    Function run at each API call
    """
    try:
        jsonfile = request.get_json()
        data = pd.read_json(json.dumps(jsonfile), orient='index')
        ypred = model.predict(doTheOneHotEncode(data))
        log.info("New request -> {}, Prediction -> {}".format(data, ypred))

        res = dict()
        for i in range(len(ypred)):
            predOrder = dict()
            first3 = list(np.argsort(ypred[i])[-3:][::-1])
            for j in range(len(first3)):
                predOrder[j + 1] = int(first3[j])

            res[i] = predOrder

        return jsonify(res)

    except Exception as e:
        log.error("makelcalc method -> {}".format(str(e)))


if __name__ == '__main__':
    log_init(log_file='rest_api.log')

    model = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), modelsPath + ANN_MODEL_FILE), 'rb'))
    log.info("REST-API Model is loaded.")

    app.run(debug=True, port=API_PORT)
