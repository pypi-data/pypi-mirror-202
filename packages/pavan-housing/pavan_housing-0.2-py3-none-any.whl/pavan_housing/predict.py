import argparse

import mlflow.sklearn
import pandas as pd
from sklearn.metrics import r2_score

from pavan_housing.config import DEFAULT_HOUSING_TEST_PATH
from pavan_housing.methods import preprocess

# Load the model artifact
best_run_id = "ede37f64711845258936830791646d75"
model_path = f"runs:/{best_run_id}/model"
model = mlflow.sklearn.load_model(model_path)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--test_path",
    help="Path to testing data",
    default=DEFAULT_HOUSING_TEST_PATH,
)

args = parser.parse_args()

HOUSING_TEST_PATH = args.test_path

# read test data
test_data = pd.read_csv(HOUSING_TEST_PATH)

# preprocess the data
test_x, test_y = preprocess(test_data)
y_predict_test = model.predict(test_x)

score = r2_score(test_y,y_predict_test)
print('R2 score :',score)