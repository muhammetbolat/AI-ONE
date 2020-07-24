from dependency_injector import providers, containers

from domain.ai.services.NeuralNetworkModelService import NeuralNetworkModelService
from domain.ai.services.NeuralNetworkService import NeuralNetworkService
from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from controllers.AiController import AiController
from infrastructor.api.ErrorHandler import ErrorHandlers
from configurations import Configurations
from infrastructor.logging.logger import Logger


class IocContainer(containers.DeclarativeContainer):
    configurations = Configurations()

    errorHandlers = providers.Singleton(ErrorHandlers)

    logger = providers.Factory(Logger,
                               other_config=configurations.other_config)

    neural_network_service = providers.Factory(NeuralNetworkService,
                                               feature_config=configurations.feature_config,
                                               ann_config=configurations.ann_config,
                                               other_config=configurations.other_config,
                                               logger=logger)

    neural_network_model_service = providers.Factory(NeuralNetworkModelService,
                                                     feature_config=configurations.feature_config,
                                                     ann_config=configurations.ann_config,
                                                     other_config=configurations.other_config,
                                                     logger=logger)

    aiController = providers.Factory(AiController,
                                     neural_network_model_service=neural_network_model_service)

    applicationWrapper = providers.Factory(FlaskAppWrapper,
                                           api_config=configurations.api_config,
                                           handlers=errorHandlers,
                                           controllers=[aiController])

# class IocContainer(containers.DeclarativeContainer):
#     def __init__(self):
#         self.configurations = Configurations()
#
#         self.errorHandlers = providers.Singleton(ErrorHandlers)
#
#         self.neural_network_model_service = providers.Factory(NeuralNetworkModelService,
#                                                               feature_config=self.configurations.feature_config,
#                                                               ann_config=self.configurations.ann_config,
#                                                               other_config=self.configurations.other_config)
#
#         self.aiController = providers.Factory(AiController,
#                                               feature_config=self.configurations.feature_config,
#                                               ann_config=self.configurations.ann_config,
#                                               other_config=self.configurations.other_config,
#                                               neural_network_model_service=self.neural_network_model_service)
#         self.app = providers.Factory(FlaskAppWrapper,
#                                      apiConfig=self.configurations.apiConfig,
#                                      handlers=self.errorHandlers,
#                                      controllers=[self.aiController])
