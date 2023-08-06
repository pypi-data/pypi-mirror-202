import logging

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pathlib import Path

from mlflow import tracking

def set_tracking_uri(uri: Union[str, Path]) -> None:
    """
    Set the tracking server URI. This does not affect the
    currently active run (if one exists), but takes effect for successive runs.

    :param uri:

                - An empty string, or a local file path, prefixed with ``file:/``. Data is stored
                  locally at the provided file (or ``./mlruns`` if empty).
                - An HTTP URI like ``https://my-tracking-server:5000``.
                - A Databricks workspace, provided as the string "databricks" or, to use a
                  Databricks CLI
                  `profile <https://github.com/databricks/databricks-cli#installation>`_,
                  "databricks://<profileName>".
                - A :py:class:`pathlib.Path` instance

    .. test-code-block:: python
        :caption: Example

        import mlflow

        mlflow.set_tracking_uri("file:///tmp/my_tracking")
        tracking_uri = mlflow.get_tracking_uri()
        print("Current tracking uri: {}".format(tracking_uri))

    .. code-block:: text
        :caption: Output

        Current tracking uri: file:///tmp/my_tracking
    """
    tracking.set_tracking_uri(uri)

def get_tracking_uri() -> str:
    return tracking.get_tracking_uri()
