import json
import pickle
import pandas as pd
import os
import numpy as np

from infrastructor.logging.logger import Logger
from models.configs.AnnConfig import AnnConfig
from models.configs.FeatureConfig import FeatureConfig
from models.configs.OtherConfig import OtherConfig


class NeuralNetworkModelService:
    def __init__(self,
                 feature_config: FeatureConfig,
                 ann_config: AnnConfig,
                 other_config: OtherConfig,
                 logger: Logger
                 ):
        self.logger = logger
        self.other_config = other_config
        self.feature_config = feature_config
        self.ann_config = ann_config

        path = os.path.join(self.other_config.root_directory,
                            self.other_config.model_path + self.ann_config.model_file)
        if os.path.isfile(path):
            model_file = open(path, 'rb')
            self.model = pickle.load(model_file)
            model_file.close()

    def do_the_one_hot_encode(self, data):
        """
        This global function calculate to one-hot encode correspoing to the one-hote model.
        """
        path = os.path.join(self.other_config.root_directory,
                            self.other_config.model_path + self.ann_config.one_hot_model_file)
        model_file = open(path, 'rb')
        one_hot_encode_model = pickle.load(model_file)
        model_file.close()
        features = self.feature_config.input_format.split(',')

        x = np.array(data[features])
        val = one_hot_encode_model.transform(x).toarray()
        return val

    def make_calculation(self, request_json):
        """
        Function run at each API call
        """
        data = pd.read_json(json.dumps(request_json), orient='index')
        ypred = self.model.predict(self.do_the_one_hot_encode(data))
        self.logger.log.info("New request -> {}, Prediction -> {}".format(data, ypred))

        result = []
        for i in range(len(ypred)):
            prediction_order = []
            first3 = list(np.argsort(ypred[i])[-3:][::-1])
            for j in range(len(first3)):
                prediction_order.append(int(first3[j]))
            result.append(prediction_order)

        return result
