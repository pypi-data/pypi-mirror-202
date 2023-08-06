""" This module is for traing the data"""
import argparse
import os
import sys
import warnings
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split

from pavan_housing import logger
from pavan_housing.config import DEFAULT_HOUSING_TRAIN_PATH
from pavan_housing.methods import *

warnings.filterwarnings("ignore")

# import the data
# import ingest_data

# define the logger
LOGGER = logger.get_logger(__name__)

# Parsing the command line inputs


parser = argparse.ArgumentParser()
parser.add_argument(
    "--train_path",
    help="Path to training data",
    default=DEFAULT_HOUSING_TRAIN_PATH,
)

args = parser.parse_args()

HOUSING_TRAIN_PATH = args.train_path

# *********Model building and training

# Load the trainig data
train_data = pd.read_csv(HOUSING_TRAIN_PATH)

train, val = train_test_split(train_data, test_size=0.2, random_state=42)
# Load preprocessed X and y
train_x, train_y = preprocess(train)
val_x, val_y = preprocess(val)


experiment_name_lr = "linear_regression"
experiment_lr = mlflow.get_experiment_by_name(experiment_name_lr)

if experiment_lr is None:
    experiment_id_lr = mlflow.create_experiment(experiment_name_lr)
    print(f"Created new experiment with ID: {experiment_id_lr}")
else:
    experiment_id_lr = experiment_lr.experiment_id
    print(f"Using existing experiment with ID: {experiment_id_lr}")

with mlflow.start_run(experiment_id = experiment_id_lr) as run:
    LOGGER.info(f'''Elastic Net Training Started with 
    Exp ID : {experiment_id_lr} | Exp name : {experiment_name_lr}''')
    #  Model1 -- Elastic Net
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(val_x)

    (rmse, mae, r2) = eval_metrics(val_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)


    mlflow.sklearn.log_model(lr, "model")



experiment_name_rf = "random_forest_regression"
experiment_rf = mlflow.get_experiment_by_name(experiment_name_rf)

if experiment_rf is None:
    experiment_id_rf = mlflow.create_experiment(experiment_name_rf)
    print(f"Created new experiment with ID: {experiment_id_rf}")
else:
    experiment_id_rf = experiment_rf.experiment_id
    print(f"Using existing experiment with ID: {experiment_id_rf}")

with mlflow.start_run(experiment_id =experiment_id_rf ) as run:
    LOGGER.info(f'''Random Forest Training Started with 
    Exp ID : {experiment_id_rf} | Exp name : {experiment_name_rf}''')
    LOGGER.info("Random Forest Training Started")
    #  Model1 -- Elastic Net
    n_estimators = 100
    max_depth = 3
    rf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
    rf.fit(train_x, train_y)

    predicted_qualities = rf.predict(val_x)

    (rmse, mae, r2) = eval_metrics(val_y, predicted_qualities)

    print(
        "Random Forest model (n_estimators=%f, max_depth=%f):"
        % (n_estimators, max_depth)
    )
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    mlflow.log_param("alpha", n_estimators)
    mlflow.log_param("l1_ratio", max_depth)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)

    mlflow.sklearn.log_model(rf, "model")
