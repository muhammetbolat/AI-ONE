from flask import jsonify, request
from flask_cors import cross_origin
from domain.ai.services.NeuralNetworkModelService import NeuralNetworkModelService
from infrastructor.api.ControllerBase import ControllerBase
from models.configs.FeatureConfig import FeatureConfig
from models.configs.AnnConfig import AnnConfig
from models.configs.OtherConfig import OtherConfig


class AiController(ControllerBase):
    def __init__(self,
                 neural_network_model_service: NeuralNetworkModelService,
                 ):
        self.neural_network_model_service = neural_network_model_service

    def endpoints(self) -> []:
        return [
            {
                'endpoint': f'get',
                'endpoint_name': 'GET',
                'handler': self.get,
                'methods': ['GET']
            },
            {
                'endpoint': f'antenna',
                'endpoint_name': 'MakeAntennaCalculation',
                'handler': self.make_calculation,
                'methods': ['POST']
            },
        ]

    @cross_origin()
    def get(self):
        return jsonify({'sum': 1 + 2})

    def make_calculation(self):
        """
        Function run at each API call
        """
        request_json = request.get_json()
        result = self.neural_network_model_service.make_calculation(request_json)
        return jsonify(result)
