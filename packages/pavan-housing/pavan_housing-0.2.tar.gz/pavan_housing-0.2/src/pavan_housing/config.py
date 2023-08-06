""" All configuration settings are available here"""

import os

DATA_DOWNLOAD_ROOT = "https://github.com/ageron/handson-ml/master/"
DEFAULT_HOUSING_PATH = "datasets"
HOUSING_URL = DATA_DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

DEFAULT_HOUSING_TRAIN_PATH = os.path.join("datasets", "train.csv")
DEFAULT_HOUSING_TEST_PATH = os.path.join("datasets", "test.csv")

LOGS_PATH = "logs/logs.txt"
