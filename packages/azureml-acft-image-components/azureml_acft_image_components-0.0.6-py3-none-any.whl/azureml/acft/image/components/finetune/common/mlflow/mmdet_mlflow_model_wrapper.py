# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Mlflow PythonModel wrapper class that loads the Mlflow model, preprocess inputs and performs inference."""

import logging
import mlflow
import pandas as pd
import sys
import subprocess
import tempfile


from common_utils import process_image, create_temp_file
from transformers import TrainingArguments

from common_constants import (
    HFMiscellaneousLiterals,
    MMDetLiterals,
    MLFlowSchemaLiterals,
    Tasks,
)

logger = logging.getLogger(__name__)


class ImagesMLFlowModelWrapper(mlflow.pyfunc.PythonModel):
    """MLFlow model wrapper for AutoML for Images models."""

    def __init__(
        self,
        task_type: str,
    ) -> None:
        """This method is called when the python model wrapper is initialized.

        :param task_type: Task type used in training.
        :type task_type: str
        """
        super().__init__()
        self._task_type = task_type

    def load_context(self, context: mlflow.pyfunc.PythonModelContext) -> None:
        """This method is called when loading a Mlflow model with pyfunc.load_model().

        :param context: Mlflow context containing artifacts that the model can use for inference.
        :type context: mlflow.pyfunc.PythonModelContext
        """
        logger.info("Inside load_context()")

        if self._task_type == Tasks.MM_OBJECT_DETECTION:
            # Install mmcv and mmdet using mim, with pip installation is not working
            subprocess.check_call([sys.executable, "-m", "mim", "install", "mmcv-full"])
            subprocess.check_call([sys.executable, "-m", "mim", "install", "mmdet"])

            # importing mmdet/mmcv afte installing using mim
            from mmdet.models import build_detector
            from mmcv import Config
            from mmcv.runner import load_checkpoint
            from mmdet_modules import ObjectDetectionModelWrapper

            try:
                if self._task_type == Tasks.MM_OBJECT_DETECTION:
                    model_config_path = context.artifacts[MMDetLiterals.CONFIG_PATH]
                    model_weights_path = context.artifacts[MMDetLiterals.WEIGHTS_PATH]

                    self._config = Config.fromfile(model_config_path)
                    self._model = build_detector(self._config.model)
                    load_checkpoint(self._model, model_weights_path)
                    self._model = ObjectDetectionModelWrapper(self._model, self._config, model_weights_path)
                    logger.info("Model loaded successfully")
                else:
                    raise ValueError(f"invalid task type {self._task_type}")
            except Exception:
                logger.warning("Failed to load the the model.")
                raise

    def predict(
        self, context: mlflow.pyfunc.PythonModelContext, input_data: pd.DataFrame
    ) -> pd.DataFrame:
        """This method performs inference on the input data.

        :param context: Mlflow context containing artifacts that the model can use for inference.
        :type context: mlflow.pyfunc.PythonModelContext
        :param input_data: Input images for prediction.
        :type input_data: Pandas DataFrame with a first column name ["image"] of images where each
        image is in base64 String format.
        :return: Output of inferencing
        :rtype: Pandas DataFrame with columns ["probs", "labels"] for classification and
        ["boxes"] for object detection, instance segmentation
        """
        task = self._task_type

        # process the images in image column
        processed_images = input_data.loc[
            :, [MLFlowSchemaLiterals.INPUT_COLUMN_IMAGE]
        ].apply(axis=1, func=process_image)

        # arguments for Trainer
        test_args = TrainingArguments(
            output_dir=".",
            do_train=False,
            do_predict=True,
            per_device_eval_batch_size=1,
            dataloader_drop_last=False,
            remove_unused_columns=False,
        )

        # To Do: change image height and width based on kwargs.

        with tempfile.TemporaryDirectory() as tmp_output_dir:
            image_path_list = (
                processed_images.iloc[:, 0]
                .map(lambda row: create_temp_file(row, tmp_output_dir))
                .tolist()
            )
            if task in [
                Tasks.MM_OBJECT_DETECTION,
                Tasks.MM_INSTANCE_SEGMENTATION
            ]:
                from mmdet_utils import mmdet_run_inference_batch
                result = mmdet_run_inference_batch(
                    test_args,
                    model=self._model,
                    id2label=self._config[HFMiscellaneousLiterals.ID2LABEL],
                    image_path_list=image_path_list,
                    task_type=task
                )

        return pd.DataFrame(result)
