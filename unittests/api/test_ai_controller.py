import json
import os
from unittest import TestCase

import jsonpickle

from domain.ai.services.NeuralNetworkService import NeuralNetworkService
import json
from unittest import TestCase

from unittests.test_container import TestIocContainer


class TestAiController(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestAiController, self).__init__(methodName)
        self.applicationWrapper = TestIocContainer.applicationWrapper()
        self.client = self.applicationWrapper.app.test_client()

        pass

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_epoch_accuracy_path(self):
        path = os.path.join(TestIocContainer.configurations.other_config.root_directory,
                            TestIocContainer.configurations.other_config.model_path, 'epochAccuracy.png')
        print(path)

    def test_execute_run_training_operation(self):
        TestIocContainer.neural_network_service().run_training_operation()
        print("Test finish")

    def test_post_api_antenna(self):
        data = json.dumps(
            {
                "0": {
                    'ONAIR_SITE_TABLE_ID': 20249035.0,
                    'SITE_IS_OIS': 0.0,
                    'SITE_ENVIRONMENT_TYPE_ID': 1.0,
                    'SITE_SITE_TYPE_ID': 113.0,
                    'SITE_MONTAGE_TYPE_ID': 12.0,
                    'SITE_RN_SUBREGION_ID': 53.0,
                    'SITE_RN_REGION_ID': 16.0,
                    'SITE_RN_MAIN_REGION_ID': 1.0,
                    'SITE_COUNTY_ID': 788.0,
                    'SITE_CITY_ID': 77.0,
                    'ONAIR_CABINET_TYPE_ID': 12.0,
                    'ONAIR_ANTENNA_TYPE_ID': 1392.0,
                    'ONAIR_BBU_TYPE_ID': 241.0,
                    'ONAIR_RFU_TYPE_ID': 345.0,
                    'SIR_CREATED_BY_USER_ID': 20680.0,
                    'SIR_MONTH_ID': 11.0,
                    'SIR_YEAR_ID': 2019.0,
                    'SIR_REASON_ID': 45.0,
                    'IR_TYPE_ID': 93
                },
                "1": {
                    'ONAIR_SITE_TABLE_ID': 20249035.0,
                    'SITE_IS_OIS': 0.0,
                    'SITE_ENVIRONMENT_TYPE_ID': 1.0,
                    'SITE_SITE_TYPE_ID': 113.0,
                    'SITE_MONTAGE_TYPE_ID': 12.0,
                    'SITE_RN_SUBREGION_ID': 53.0,
                    'SITE_RN_REGION_ID': 16.0,
                    'SITE_RN_MAIN_REGION_ID': 1.0,
                    'SITE_COUNTY_ID': 788.0,
                    'SITE_CITY_ID': 77.0,
                    'ONAIR_CABINET_TYPE_ID': 12.0,
                    'ONAIR_ANTENNA_TYPE_ID': 1392.0,
                    'ONAIR_BBU_TYPE_ID': 241.0,
                    'ONAIR_RFU_TYPE_ID': 345.0,
                    'SIR_CREATED_BY_USER_ID': 20680.0,
                    'SIR_MONTH_ID': 11.0,
                    'SIR_YEAR_ID': 2019.0,
                    'SIR_REASON_ID': 45.0,
                    'IR_TYPE_ID': 93
                }
            }
        )

        response = self.client.post(
            '/api/ai/antenna',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'

        response = self.client.post(
            '/api/ai/antenna',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'
        print("Test finish")
