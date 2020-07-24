import os
import pickle
import warnings
import pandas as pd
import shutil
import matplotlib.pyplot as plt
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime as dt

from infrastructor.logging.logger import Logger
from models.configs.AnnConfig import AnnConfig
from models.configs.FeatureConfig import FeatureConfig
from models.configs.OtherConfig import OtherConfig
from keras.callbacks import EarlyStopping

warnings.filterwarnings("ignore")


class NeuralNetworkService:
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
        self.backup_folder = '{}_Models'.format(dt.now().strftime("%m_%d_%Y"))

    def backup_models(self):
        """
        If accuracy is enough to continue, system backup existing models to new file which is named by date.
        """
        try:

            shutil.copytree(self.other_config.model_path, self.other_config.backup_path + self.backup_folder)
        except IOError as e:
            self.logger.log.error("(backupModels) Unable to copy file: {0}".format(str(e)))
        except Exception as ex:
            self.logger.log.error("(backupModels) Unexpected error: {0}".format(sys.exc_info()))

    def visualization(self, history):
        """
        Visualization of training model.
        """
        plt.title('Epoch Accuracy')
        plt.xlabel = 'Epochs'
        plt.ylabel = 'Mean Accuracy Error'
        plt.plot(range(1, len(history.epoch) + 1), history.history['accuracy'])
        plt.plot(range(1, len(history.epoch) + 1),
                 history.history['val_accuracy'])
        plt.legend(['Accuracy', 'Validation Accuracy'])

        path = os.path.join(self.other_config.root_directory, self.other_config.model_path, 'epochAccuracy.png')
        plt.savefig(path)

    def run_training_operation(self):
        try:
            self.logger.log.info("Starting Neural Network algorithm...")
            self.logger.log.info("Reading DB to get all data...")
            # Veri tabanından okunacak şekilde değiştirilecek.

            path = os.path.join(self.other_config.root_directory, self.other_config.file_name)
            data_set = pd.read_csv(path)
            self.logger.log.info("Datas are fetched.")

            ###########################################################################################################
            # Pre-Processing
            self.logger.log.info("Pre-processing is started.")
            data_set = data_set.dropna()

            x = data_set[self.feature_config.input_format.split(',')]
            y = data_set[self.feature_config.output_format]

            hot_encoder = OneHotEncoder(handle_unknown='ignore')
            x = hot_encoder.fit_transform(x).toarray()

            y = to_categorical(y)
            self.logger.log.info("Pre-processing is done.")

            ###########################################################################################################
            # Training DataSet
            self.logger.log.info("ANN Model is training....")

            training_set_x, test_set_x, training_set_y, test_set_y = train_test_split(x,
                                                                                      y,
                                                                                      test_size=self.ann_config.test_size,
                                                                                      random_state=42)
            model = Sequential()

            training_feature = training_set_x.shape[1]
            model.add(Dense(256, input_dim=training_feature, activation='relu', name='Hidden-1'))
            model.add(Dense(256, activation='relu', name='Hidden-2'))
            model.add(Dense(training_set_y.shape[1], activation='softmax', name='Output'))

            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            esc = EarlyStopping(monitor='val_accuracy', patience=5, verbose=1, restore_best_weights=True)
            history = model.fit(training_set_x,
                                training_set_y,
                                epochs=self.ann_config.epochs,
                                batch_size=self.ann_config.batch_size,
                                validation_split=self.ann_config.validation_split,
                                callbacks=[esc])

            self.logger.log.info("ANN Model is finished....")

            ###########################################################################################################
            # Test DataSet
            loss, accuracy = model.evaluate(test_set_x, test_set_y)
            self.logger.log.info("!!!TEST RESULTS!!! loss:{0}, accuracy:{1}".format(loss, accuracy))

            ###########################################################################################################
            # Backup legacy models to specified file.
            self.backup_models()
            self.logger.log.info("Model is backuped.")

            # Model check and finiliaze.
            if accuracy > self.ann_config.minimum_accuracy:
                self.visualization(history)

                self.logger.log.info("Accuracy is enough to replace the model. :)")
                path = os.path.join(self.other_config.root_directory, self.other_config.model_path,
                                    self.ann_config.model_file)
                output = open(path, 'wb')
                pickle.dump(model, output)
                output.close()
                self.logger.log.info("Model is saved...")

                path = os.path.join(self.other_config.root_directory, self.other_config.model_path,
                                    self.ann_config.one_hot_model_file)
                output = open(path, 'wb')
                pickle.dump(hot_encoder, output)
                output.close()
                self.logger.log.info("One-Hot-Encoding is saved...")

            else:
                self.logger.log.info("Accuracy is not enough to replace the model. :(")

        except Exception as e:
            self.logger.log.error("neurol network main error: {}".format(str(e)))
