# pylint: disable=wrong-import-position
__version__ = '0.0.1'

_model_flavors_supported = []
try:
    # pylint: disable=unused-import
    from mlflow import catboost
    from mlflow import fastai
    from mlflow import gluon
    from mlflow import h2o
    from mlflow import lightgbm
    from mlflow import mleap
    from mlflow import onnx
    from mlflow import recipes
    from mlflow import pyfunc
    from mlflow import pytorch
    from mlflow import sklearn
    from mlflow import spacy
    from mlflow import spark
    from mlflow import statsmodels
    from mlflow import tensorflow
    from mlflow import xgboost
    from mlflow import shap
    from mlflow import pyspark
    from mlflow import paddle
    from mlflow import prophet
    from mlflow import pmdarima
    from mlflow import diviner
    from mlflow import transformers

    _model_flavors_supported = [
        "catboost",
        "fastai",
        "gluon",
        "h2o",
        "lightgbm",
        "mleap",
        "onnx",
        "pyfunc",
        "pytorch",
        "sklearn",
        "spacy",
        "spark",
        "statsmodels",
        "tensorflow",
        "keras",
        "xgboost",
        "shap",
        "paddle",
        "prophet",
        "pmdarima",
        "diviner",
        "transformers",
    ]
except ImportError as e:
    # We are conditional loading these commands since the skinny client does
    # not support them due to the pandas and numpy dependencies of MLflow Models
    pass

from haiqvML.client import (
    set_tracking_uri,
    get_tracking_uri,
    # is_tracking_uri_set,
    # _get_store,
    # _TRACKING_URI_ENV_VAR,
)

from haiqvML.track import (    
    set_experiment,
    start_run,
    end_run,    
    log_param,
    log_params,
    log_metric,
    log_metrics,
)

__all__ = [
    "get_tracking_uri",
    "set_tracking_uri",    
    "set_experiment",
    "start_run",
    "end_run",
    "log_param",
    "log_params",
    "log_metric",
    "log_metrics",
] + _model_flavors_supported
