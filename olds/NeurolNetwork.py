import pickle
import warnings
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime as dt
import shutil
import sys
import matplotlib.pyplot as plt
import os
import logging as log
import yaml

warnings.filterwarnings("ignore")

with open("application_conf.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

########################################################################################################################
# Database Information
DB_HOST = cfg['DBMS']['host']
DB_USER = cfg['DBMS']['user']
DB_PASSWD = cfg['DBMS']['passwd']
DB_NAME = cfg['DBMS']['db']

FILE_NAME = "LAST_ANTENNA_DATA.csv"
########################################################################################################################
# Data Features
INPUT_FEATURES = cfg['FEATURES']['INPUT']
OUTPUT_FEATURE = cfg['FEATURES']['OUTPUT']

########################################################################################################################
# Models
modelsPath = cfg['OTHER']['modelsPath']
backupPath = cfg['OTHER']['backupPath']

BACKUP_FOLDER = '{}_Models'.format(dt.now().strftime("%m_%d_%Y"))
########################################################################################################################
# Neural Network Parameters
epochs = cfg['ANN']['epochs']
batch_size = cfg['ANN']['batch_size']
test_size = cfg['ANN']['test_size']
val_split = cfg['ANN']['val_split']
minimum_accuracy = cfg['ANN']['minimum_accuracy']
ANN_MODEL_FILE = cfg['ANN']['ANN_model_file']
ONE_HOT_MODEL_FILE = cfg['ANN']['One_Hot_model_file']


def backupModels():
    """
    If accuracy is enough to continue, system backup existing models to new file which is named by date.
    """
    try:
        shutil.copytree(modelsPath, backupPath + BACKUP_FOLDER)
    except IOError as e:
        log.error("(backupModels) Unable to copy file: {0}".format(str(e)))
    except:
        log.error("(backupModels) Unexpected error: {0}".format(sys.exc_info()))


def log_init(log_file):
    """
    initiliazation of log file.
    """
    log.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file),
                    filemode='a',
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=log.DEBUG)

def visualization(history):
    """
    Visualization of training model.
    """
    plt.title('Epoch Accuracy')
    plt.xlabel = 'Epochs'
    plt.ylabel = 'Mean Accuracy Error'
    plt.plot(range(1, len(history.epoch) + 1), history.history['accuracy'])
    plt.plot(range(1, len(history.epoch) + 1), history.history['val_accuracy'])
    plt.legend(['Accuracy', 'Validation Accuracy'])
    plt.savefig(modelsPath + 'epochAccuracy.png')


if __name__ == '__main__':
    try:
        #Log file init
        log_init("ann.log")

        log.info("Starting Neural Network algorithm...")
        log.info("Reading DB to get all data...")
        dataset = pd.read_csv(FILE_NAME)  # Veri tabanından okunacak şekilde değiştirilecek.
        log.info("Datas are fetched.")

        ################################################################################################################
        # Pre-Processing
        log.info("Pre-processing is started.")
        dataset = dataset.dropna()

        X = dataset[INPUT_FEATURES.split(',')]
        Y = dataset[OUTPUT_FEATURE]

        hot_encoder = OneHotEncoder(handle_unknown='ignore')
        X = hot_encoder.fit_transform(X).toarray()

        Y = to_categorical(Y)
        log.info("Pre-processing is done.")

        ################################################################################################################
        # Training DataSet
        log.info("ANN Model is training....")

        training_set_x, test_set_x, training_set_y, test_set_y = train_test_split(X, Y, test_size=test_size,
                                                                                  random_state=42)
        model = Sequential()

        training_feauture = training_set_x.shape[1]
        model.add(Dense(256, input_dim=training_feauture, activation='relu', name='Hidden-1'))
        model.add(Dense(256, activation='relu', name='Hidden-2'))
        model.add(Dense(training_set_y.shape[1], activation='softmax', name='Output'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        history = model.fit(training_set_x, training_set_y, epochs=epochs, batch_size=batch_size,
                            validation_split=val_split)

        log.info("ANN Model is finished....")

        ####################################################################################################################
        # Test DataSet
        loss, accuracy = model.evaluate(test_set_x, test_set_y)
        log.info("!!!TEST RESULTS!!! loss:{0}, accuracy:{1}".format(loss, accuracy))

        ####################################################################################################################
        # Backup legacy models to specified file.
        backupModels()
        log.info("Model is backuped.")

        # Model check and finiliaze.
        if accuracy > minimum_accuracy:
            visualization(history)

            log.info("Accuracy is enough to replace the model. :)")
            output = open(modelsPath + ANN_MODEL_FILE, 'wb')
            pickle.dump(model, output)

            log.info("Model is saved...")

            output = open(modelsPath + ONE_HOT_MODEL_FILE, 'wb')
            pickle.dump(hot_encoder, output)

            log.info("One-Hot-Encoding is saved...")

        else:
            log.info("Accuracy is not enough to replace the model. :(")

    except Exception as e:
        log.error("neurol network main error: {}".format(str(e)))

    ####################################################################################################################
