# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Mlflow PythonModel wrapper helper scripts."""

import logging
import os
import platform
import tempfile
import torch
import mlflow
import pandas as pd
import base64
import io
import re
import requests

from PIL import Image
from typing import Any, Dict, Optional
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, Schema
from common_constants import (
    Tasks,
    MLFlowSchemaLiterals,
    MMDetLiterals
)

logger = logging.getLogger(__name__)

# Uncomment the following line for mlflow debug mode
# logging.getLogger("mlflow").setLevel(logging.DEBUG)


def create_temp_file(request_body: bytes, parent_dir: str) -> str:
    """Create temporory file, save image and return path to the file.

    :param request_body: Image
    :type request_body: bytes
    :param parent_dir: directory name
    :type parent_dir: str
    :return: Path to the file
    :rtype: str
    """
    with tempfile.NamedTemporaryFile(dir=parent_dir, mode="wb", delete=False) as image_file_fp:
        # image_file_fp.write(request_body)
        img_path = image_file_fp.name + ".png"
        img = Image.open(io.BytesIO(request_body))
        img.save(img_path)
        return img_path


def get_mlflow_signature(task_type: str) -> ModelSignature:
    """
    Return mlflow model signature with input and output schema given the input task type.

    :param task_type: Task type used in training.
    :type task_type: str
    :return: mlflow model signature.
    :rtype: mlflow.models.signature.ModelSignature
    """

    input_schema = Schema(
        [
            ColSpec(
                MLFlowSchemaLiterals.INPUT_COLUMN_IMAGE_DATA_TYPE,
                MLFlowSchemaLiterals.INPUT_COLUMN_IMAGE,
            )
        ]
    )

    # For classification
    if task_type in [
        Tasks.HF_MULTI_CLASS_IMAGE_CLASSIFICATION,
        Tasks.HF_MULTI_LABEL_IMAGE_CLASSIFICATION,
    ]:

        output_schema = Schema(
            [
                ColSpec(
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_DATA_TYPE,
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_PROBS,
                ),
                ColSpec(
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_DATA_TYPE,
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_LABELS,
                ),
            ]
        )

    # for object detection and instance segmentation mlflow signature remains same
    elif task_type in [
        Tasks.MM_OBJECT_DETECTION,
        Tasks.MM_INSTANCE_SEGMENTATION
    ]:
        output_schema = Schema(
            [
                ColSpec(
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_DATA_TYPE,
                    MLFlowSchemaLiterals.OUTPUT_COLUMN_BOXES,
                ),
            ]
        )
    else:
        raise ValueError(f"invalid task type {task_type}")

    return ModelSignature(inputs=input_schema, outputs=output_schema)


def save_mlflow_model(
    model_output_dir: str,
    mlflow_output_dir: str,
    options: Dict[str, Any],
    model_name: str,
    pip_requirements: Optional[os.PathLike] = None,
) -> None:
    """
    Save the mlflow model.

    :param model_output_dir: Output directory where the HF trainer model files are stored.
    :type model_output_dir: str
    :param mlflow_output_dir: Output directory where mlflow model will be stored.
    :type mlflow_output_dir: str
    :param options: Dictionary of MLflow settings/wrappers for model saving process.
    :type options: Dict
    """

    config_path = os.path.join(model_output_dir, model_name + ".py")
    model_weights_path = os.path.join(model_output_dir, model_name + ".pth")
    artifacts_dict = {
        MMDetLiterals.CONFIG_PATH : config_path,
        MMDetLiterals.WEIGHTS_PATH : model_weights_path
    }

    logger.info(f"Saving mlflow pyfunc model to {mlflow_output_dir}.")

    try:
        logging.getLogger("mlflow").setLevel(logging.DEBUG)
        dir = os.path.dirname(__file__)
        code_path = [os.path.join(dir, x) for x in os.listdir(dir)]
        mlflow.pyfunc.save_model(
            path=mlflow_output_dir,
            python_model=options[MLFlowSchemaLiterals.WRAPPER],
            artifacts=artifacts_dict,
            pip_requirements=pip_requirements,
            signature=options[MLFlowSchemaLiterals.SCHEMA_SIGNATURE],
            code_path=code_path
        )
        logger.info("Saved mlflow model successfully.")
    except Exception as e:
        raise Exception(f"failed to save the mlflow model {str(e)}")


def process_image(img: pd.Series) -> pd.Series:
    """If input image is in base64 string format, decode it to bytes. If input image is in url format,
    download it and return bytes.
    https://github.com/mlflow/mlflow/blob/master/examples/flower_classifier/image_pyfunc.py

    :param img: pandas series with image in base64 string format or url.
    :type img: pd.Series
    :return: decoded image in pandas series format.
    :rtype: Pandas Series
    """
    image = img[0]
    if _is_valid_url(image):
        image = requests.get(image).content
        return pd.Series(image)
    try:
        return pd.Series(base64.b64decode(image))
    except Exception:
        raise ValueError("Invalid image format")


def _is_valid_url(text: str) -> bool:
    """check if text is url or base64 string
    :param text: text to validate
    :type text: str
    :return: True if url else false
    :rtype: bool
    """
    regex = (
        "((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )
    p = re.compile(regex)

    # If the string is empty
    # return false
    if str is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, text):
        return True
    else:
        return False
