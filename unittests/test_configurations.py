import os
import yaml

from models.configs.AnnConfig import AnnConfig
from models.configs.ApiConfig import ApiConfig
from models.configs.DatabaseConfig import DatabaseConfig
from models.configs.FeatureConfig import FeatureConfig
from models.configs.OtherConfig import OtherConfig

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_application_conf.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


class TestConfigurations:
    def __init__(self):
        ################################################################################################################
        # Api Information
        api_name = os.getenv('API_NAME', cfg['API']['NAME'])
        is_debug = os.getenv('API_IS_DEBUG', cfg['API']['IS_DEBUG'])
        api_port = os.getenv('API_PORT', cfg['API']['PORT'])
        self.api_config = ApiConfig(name=api_name, is_debug=is_debug, port=api_port)

        ################################################################################################################
        # Database Information
        dbms_host = os.getenv('DBMS_HOST', cfg['DBMS']['HOST'])
        dbms_user = os.getenv('DBMS_USER', cfg['DBMS']['USER'])
        dbms_password = os.getenv('DBMS_PASSWORD', cfg['DBMS']['PASSWORD'])
        dbms_name = os.getenv('DBMS_NAME', cfg['DBMS']['NAME'])
        self.database_config = DatabaseConfig(host=dbms_host, user=dbms_user, password=dbms_password, name=dbms_name)

        ################################################################################################################
        # Data Features
        features_input_format = os.getenv('FEATURES_INPUT', cfg['FEATURES']['INPUT_FORMAT'])
        features_output_format = os.getenv('FEATURES_OUTPUT', cfg['FEATURES']['OUTPUT_FORMAT'])
        self.feature_config = FeatureConfig(input_format=features_input_format, output_format=features_output_format)

        ################################################################################################################
        # Neural Network Parameters
        ann_model_file = os.getenv('ANN_MODEL_FILE', cfg['ANN']['MODEL_FILE'])
        ann_one_hot_model_file = os.getenv('ANN_ONE_HOT_MODEL_FILE', cfg['ANN']['ONE_HOT_MODEL_FILE'])
        ann_epochs = os.getenv('ANN_EPOCHS', cfg['ANN']['EPOCHS'])
        ann_batch_size = os.getenv('ANN_BATCH_SIZE', cfg['ANN']['BATCH_SIZE'])
        ann_test_size = os.getenv('ANN_TEST_SIZE', cfg['ANN']['TEST_SIZE'])
        ann_validation_split = os.getenv('ANN_VALIDATION_SPLIT', cfg['ANN']['VALIDATION_SPLIT'])
        ann_minimum_accuracy = os.getenv('ANN_MINIMUM_ACCURACY', cfg['ANN']['MINIMUM_ACCURACY'])
        self.ann_config = AnnConfig(model_file=ann_model_file, one_hot_model_file=ann_one_hot_model_file,
                                    epochs=ann_epochs, batch_size=ann_batch_size, test_size=ann_test_size,
                                    validation_split=ann_validation_split, minimum_accuracy=ann_minimum_accuracy)

        ################################################################################################################
        # Other Parameters
        other_model_path = os.getenv('OTHER_MODEL_PATH', cfg['OTHER']['MODEL_PATH'])
        other_backup_path = os.getenv('OTHER_BACKUP_PATH', cfg['OTHER']['BACKUP_PATH'])
        other_file_name = os.getenv('OTHER_FILE_NAME', cfg['OTHER']['FILE_NAME'])
        root_directory = os.path.dirname(os.path.abspath(__file__))
        other_log_path = os.getenv('OTHER_LOG_PATH', cfg['OTHER']['LOG_PATH'])

        self.other_config = OtherConfig(model_path=other_model_path, backup_path=other_backup_path,
                                        file_name=other_file_name, root_directory=root_directory,
                                        log_path=other_log_path)
