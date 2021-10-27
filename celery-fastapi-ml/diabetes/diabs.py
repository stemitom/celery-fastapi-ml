import pandas
import numpy
from sklearn import datasets, ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from celery.utils.log import get_logger

celery_log = get_logger(__name__)

def dataloader(partition_size:str = 0.2, random_state:int = 42):
    diabetes = datasets.load_diabetes()
    X, y = diabetes.data, diabetes.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=partition_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test

def train(X_train, y_train, params:dict = {
    "n_estimators": 500, 
    "max_depth": 4, 
    "min_samples_split": 5, 
    "learning_rate": 0.01, 
    "loss": "squared_error",
}):
    regressor = ensemble.GradientBoostingRegressor(**params)
    regressor.fit(X_train, y_train)
    return regressor

def metric_test(X_test, y_test, model):
    mse = mean_squared_error(y_test, model.predict(X_test))
    return mse

def main():
    X_train, X_test, y_train, y_test = dataloader()
    celery_log.info("Dataset loaded")
    celery_log.info("Starting Training")
    model = train(X_train, y_train)
    celery_log.info("Ending Training")
    mse = metric_test(X_test, y_test, model)
    celery_log.info(f"MSELoss: {mse}")