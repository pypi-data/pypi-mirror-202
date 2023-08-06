from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from mlflow import tracking
from mlflow.entities import Experiment, Run, RunStatus

def set_experiment(experiment_name: str = None, experiment_id: str = None) -> Experiment:
    """
    Set the given experiment as the active experiment. The experiment must either be specified by
    name via `experiment_name` or by ID via `experiment_id`. The experiment name and ID cannot
    both be specified.

    :param experiment_name: Case sensitive name of the experiment to be activated. If an experiment
                            with this name does not exist, a new experiment wth this name is
                            created.
    :param experiment_id: ID of the experiment to be activated. If an experiment with this ID
                          does not exist, an exception is thrown.
    :return: An instance of :py:class:`mlflow.entities.Experiment` representing the new active
             experiment.

    .. test-code-block:: python
        :caption: Example

        import mlflow

        # Set an experiment name, which must be unique and case-sensitive.
        experiment = mlflow.set_experiment("Social NLP Experiments")

        # Get Experiment Details
        print("Experiment_id: {}".format(experiment.experiment_id))
        print("Artifact Location: {}".format(experiment.artifact_location))
        print("Tags: {}".format(experiment.tags))
        print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    .. code-block:: text
        :caption: Output

        Experiment_id: 1
        Artifact Location: file:///.../mlruns/1
        Tags: {}
        Lifecycle_stage: active
    """
    return tracking.fluent.set_experiment(experiment_name, experiment_id)

class ActiveRun(Run):  # pylint: disable=W0223
    """Wrapper around :py:class:`mlflow.entities.Run` to enable using Python ``with`` syntax."""

    def __init__(self, run):
        Run.__init__(self, run.info, run.data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
        end_run(RunStatus.to_string(status))
        return exc_type is None

def start_run(
    run_id: str = None,
    experiment_id: Optional[str] = None,
    run_name: Optional[str] = None,
    nested: bool = False,
    tags: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
) -> ActiveRun:
    return tracking.fluent.start_run(
        run_id,
        experiment_id,
        run_name,
        nested,
        tags,
        description)

def end_run(status: str = RunStatus.to_string(RunStatus.FINISHED)) -> None:
    tracking.fluent.end_run(status)

def log_param(key: str, value: Any) -> Any:
    """
    Log a parameter (e.g. model hyperparameter) under the current run. If no run is active,
    this method will create a new active run.

    :param key: Parameter name (string). This string may only contain alphanumerics,
                underscores (_), dashes (-), periods (.), spaces ( ), and slashes (/).
                All backend stores support keys up to length 250, but some may
                support larger keys.
    :param value: Parameter value (string, but will be string-ified if not).
                  All backend stores support values up to length 500, but some
                  may support larger values.

    :return: the parameter value that is logged.

    .. test-code-block:: python
        :caption: Example

        import mlflow

        with mlflow.start_run():
            value = mlflow.log_param("learning_rate", 0.01)
            assert value == 0.01
    """
    tracking.fluent.log_param(key, value)

def log_params(params: Dict[str, Any]) -> None:
    tracking.fluent.log_params(params)

def log_metric(key: str, value: float, step: Optional[int] = None) -> None:
    tracking.fluent.log_metric(key, value, step)

def log_metrics(metrics: Dict[str, float], step: Optional[int] = None) -> None:
    """
    Log multiple metrics for the current run. If no run is active, this method will create a new
    active run.

    :param metrics: Dictionary of metric_name: String -> value: Float. Note that some special
                    values such as +/- Infinity may be replaced by other values depending on
                    the store. For example, sql based store may replace +/- Infinity with
                    max / min float values.
    :param step: A single integer step at which to log the specified
                 Metrics. If unspecified, each metric is logged at step zero.

    :returns: None

    .. test-code-block:: python
        :caption: Example

        import mlflow

        metrics = {"mse": 2500.00, "rmse": 50.00}

        # Log a batch of metrics
        with mlflow.start_run():
            mlflow.log_metrics(metrics)
    """
    tracking.fluent.log_metrics(metrics, step)
