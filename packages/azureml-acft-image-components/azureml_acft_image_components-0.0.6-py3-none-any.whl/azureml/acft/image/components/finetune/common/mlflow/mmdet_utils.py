# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Mlflow PythonModel wrapper helper scripts."""

import logging
import mlflow
import numpy as np
import os
import torch


from datasets import load_dataset
from dataclasses import asdict
from torchvision.transforms import functional as F
from transformers import Trainer, TrainingArguments
from typing import Dict, List, Optional, Tuple, Any


from common_constants import (HFMiscellaneousLiterals, Tasks,
                              MMDetLiterals,
                              MLFlowSchemaLiterals,
                              MmDetectionDatasetLiterals,
                              ODLiterals)
from common_utils import get_mlflow_signature
from mmdet_mlflow_model_wrapper import ImagesMLFlowModelWrapper
from mmdet_modules import ImageMetadata

logger = logging.getLogger(__name__)


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
    :param model_name: Name of the model.
    :type model_name: str
    :param pip_requirements: Path to the pip requirements file.
    :type pip_requirements: Optional[os.PathLike]
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
        files_to_include = ['common_constants.py', 'common_utils.py', 'mmdet_mlflow_model_wrapper.py',
                            'mmdet_modules.py', 'mmdet_utils.py']
        code_path = [os.path.join(dir, x) for x in files_to_include]
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


def save_mmdet_mlflow_pyfunc_model(
    task_type: str,
    model_output_dir: str,
    mlflow_output_dir: str,
    model_name: str,
    pip_requirements: Optional[List[str]] = None,
) -> None:
    """
    Save the mlflow model.

    :param task_type: Task type used in training.
    :type task_type: str
    :param model_output_dir: Output directory where the HF trainer model files are stored.
    :type model_output_dir: str
    :param mlflow_output_dir: Output directory where mlflow model will be stored.
    :type mlflow_output_dir: str
    :param model_name: Name of the model.
    :type model_name: str
    :param pip_requirements: Path to the pip requirements file.
    :type pip_requirements: Optional[os.PathLike]
    """

    mlflow_model_wrapper = None
    logger.info("Saving the model in MLFlow format.")
    mlflow_model_wrapper = ImagesMLFlowModelWrapper(task_type=task_type)

    # Upload files to artifact store
    mlflow_options = {
        MLFlowSchemaLiterals.WRAPPER: mlflow_model_wrapper,
        MLFlowSchemaLiterals.SCHEMA_SIGNATURE: get_mlflow_signature(task_type),
    }
    save_mlflow_model(
        model_output_dir=model_output_dir,
        mlflow_output_dir=mlflow_output_dir,
        options=mlflow_options or {},
        model_name=model_name,
        pip_requirements=pip_requirements,
    )


def mmdet_run_inference_batch(
    test_args: TrainingArguments,
    model: torch.nn.Module,
    id2label: Dict[int, str],
    image_path_list: List,
    task_type: Tasks,
) -> List:
    """This method performs inference on batch of input images.

    :param test_args: Training arguments path.
    :type test_args: transformers.TrainingArguments
    :param image_processor: Preprocessing configuration loader.
    :type image_processor: transformers.AutoImageProcessor
    :param model: Pytorch model weights.
    :type model: transformers.AutoModelForImageClassification
    :param image_path_list: list of image paths for inferencing.
    :type image_path_list: List
    :param task_type: Task type of the model.
    :type task_type: constants.Tasks
    :return: list of dict.
    :rtype: list
    """

    def collate_fn(examples: List[Dict[str, Dict]]) -> Dict[str, Dict]:
        # Filter out invalid examples
        valid_examples = [example for example in examples if example is not None]
        if len(valid_examples) != len(examples):
            if len(valid_examples) == 0:
                raise Exception("All images in the current batch are invalid.")
            else:
                num_invalid_examples = len(examples) - len(valid_examples)
                logger.info(f"{num_invalid_examples} invalid images found.")
                logger.info("Replacing invalid images with randomly selected valid images from the current batch")
                new_example_indices = np.random.choice(np.arange(len(valid_examples)), num_invalid_examples)
                for ind in new_example_indices:
                    # Padding the batch with valid examples
                    valid_examples.append(valid_examples[ind])

        # Pre processing code should come here once the PR for mmdet aug
        # is merged
        pixel_values = torch.stack(
            [
                F.to_tensor(example[HFMiscellaneousLiterals.DEFAULT_IMAGE_KEY]).to(dtype=torch.float)
                for example in valid_examples
            ]
        )

        img_metas = []
        for i, example in enumerate(valid_examples):
            image = example[HFMiscellaneousLiterals.DEFAULT_IMAGE_KEY]
            width, height = image.size
            no_ch = len(image.getbands())
            img_metas.append(
                asdict(ImageMetadata(ori_shape=(width, height, no_ch), filename=f"test_{i}.jpg"))
            )

        # input to mmdet model should contain image and image meta data
        output = {
            MmDetectionDatasetLiterals.IMG: pixel_values,
            MmDetectionDatasetLiterals.IMG_METAS: img_metas
        }

        return output

    inference_dataset = load_dataset(
        HFMiscellaneousLiterals.IMAGE_FOLDER,
        data_files={HFMiscellaneousLiterals.VAL: image_path_list}
    )
    inference_dataset = inference_dataset[HFMiscellaneousLiterals.VAL]

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=test_args,
        data_collator=collate_fn,
    )
    results = trainer.predict(inference_dataset)
    output = results.predictions[1]

    proc_op = []
    for bboxes, labels in zip(output[MmDetectionDatasetLiterals.BBOXES], output[MmDetectionDatasetLiterals.LABELS]):
        curimage_preds = {ODLiterals.BOXES : []}
        for bbox, label in zip(bboxes, labels):
            curimage_preds[ODLiterals.BOXES].append({
                ODLiterals.BOX : {
                    ODLiterals.TOP_X : bbox[0],
                    ODLiterals.TOP_Y : bbox[1],
                    ODLiterals.BOTTOM_X : bbox[2],
                    ODLiterals.BOTTOM_Y : bbox[3],
                },
                ODLiterals.LABEL : id2label[label],
                ODLiterals.SCORE : bbox[4],
            })
        proc_op.append(curimage_preds)
    return proc_op
