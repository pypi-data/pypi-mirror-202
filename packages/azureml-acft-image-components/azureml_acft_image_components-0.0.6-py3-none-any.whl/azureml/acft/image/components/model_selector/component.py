# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""AzureML ACFT Image Components - model selector component code."""
import glob
import json
import os

from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore

from azureml.acft.accelerator.utils.error_handling.error_definitions import LLMInternalError
from azureml.acft.accelerator.utils.error_handling.exceptions import LLMException

from azureml.acft.common_components import get_logger_app
from azureml.acft.common_components.model_selector.component import ModelSelector
from azureml.acft.common_components.model_selector.constants import ModelSelectorDefaults, ModelSelectorConstants

from azureml.acft.image.components.finetune.factory.mappings import MODEL_FAMILY_CLS
from azureml.acft.image.components.model_selector.constants import ImageModelSelectorConstants


logger = get_logger_app(__name__)


class ImageModelSelector(ModelSelector):
    """Implementation for image model selector."""
    def __init__(
        self,
        pytorch_model: str = None,
        mlflow_model: str = None,
        model_family: str = None,
        model_name: str = None,
        output_dir: str = None,
        **kwargs,
    ) -> None:
        """Implementation for image model selector.

        :param pytorch_model: asset path of pytorch model, defaults to None
        :type pytorch_model: str, optional
        :param mlflow_model: asset path of mlflow model, defaults to None
        :type mlflow_model: str, optional
        :param model_family: model family (like HuggingFace, MMDetection), defaults to None
        :type model_family: str, optional
        :param model_name: model name from the framework (i.e., HF), defaults to None
        :type model_name: str, optional
        :param output_dir: path to store arguments and model, defaults to None
        :type output_dir: str, optional
        """
        # Todo - Remove when we start supporting all the models from MMDetection model zoo.
        if model_family == MODEL_FAMILY_CLS.MMDETECTION_IMAGE:
            if pytorch_model is None and mlflow_model is None:
                raise NotImplementedError(
                    f"For {model_family}, we are only supporting models, which are registered. "
                    f"We don't provide support for all models from MMDetection Model Zoo yet."
                )

        super().__init__(
            pytorch_model=pytorch_model,
            mlflow_model=mlflow_model,
            model_name=model_name,
            output_dir=output_dir,
            **kwargs,
        )
        self.model_family = model_family

    def _prepare_mmlab_arguments_from_input_model(self) -> dict:
        """Prepare arguments for MMLAB/MMDetection models.

        :return: A dictinary conatining argument name to value mapping to update.
        :rtype: dictionary
        """
        input_model_path = None
        if self.pytorch_model is not None:
            input_model_path = self.pytorch_model
        elif self.mlflow_model is not None:
            input_model_path = self.mlflow_model

        abs_input_model_path = os.path.join(self.output_dir, input_model_path)

        model_metafile_json_path = os.path.join(
            abs_input_model_path,
            ImageModelSelectorConstants.MMLAB_MODEL_METAFILE_NAME
        )
        if os.path.exists(model_metafile_json_path):
            with open(model_metafile_json_path, "r") as jsonFile:
                model_metadata = json.load(jsonFile)
            if self.model_name is not None and self.model_name != model_metadata[ModelSelectorConstants.MODEL_NAME]:
                error_string = (
                    f"Ensure provided model_name ({self.model_name}) matches with what's in "
                    f"{ImageModelSelectorConstants.MMLAB_MODEL_METAFILE_NAME} - "
                    f"{model_metadata[ModelSelectorConstants.MODEL_NAME]}."
                )
                raise LLMException._with_error(
                    AzureMLError.create(LLMInternalError, error=error_string)
                )
            else:
                self.model_name = model_metadata[ModelSelectorConstants.MODEL_NAME]

        self.model_name = self.model_name if not self.model_name.endswith(".py") else self.model_name[:-3]

        if self.model_name is None:
            error_string = (
                f"We could not indentify {ModelSelectorConstants.MODEL_NAME}'s value {self.model_name}. "
                f"Ensure to either pass model name in {ModelSelectorConstants.MODEL_NAME}, or in "
                f"{ImageModelSelectorConstants.MMLAB_MODEL_METAFILE_NAME} as "
                f"{{{ModelSelectorConstants.MODEL_NAME}: <NAME_OF_MODEL>}}"
            )
            raise LLMException._with_error(
                AzureMLError.create(LLMInternalError, error=error_string)
            )

        abs_mmlab_config_path = os.path.join(abs_input_model_path, f"{self.model_name}.py")
        # Assume that model config is in the parent folder
        mmlab_config_path = abs_mmlab_config_path.replace(abs_input_model_path, input_model_path)
        # Check existance of mmlab config python file
        if not os.path.exists(abs_mmlab_config_path):
            error_string = (
                f"Ensure that {self.model_name}.py exists in your registered input model folder. "
                f"Found list of files: {os.listdir(abs_input_model_path)}"
            )
            raise LLMException._with_error(
                AzureMLError.create(LLMInternalError, error=error_string)
            )

        # Get the model weight file path
        checkpoint_files = glob.glob(os.path.join(abs_input_model_path, "*.pth"), recursive=True)
        if len(checkpoint_files) != 1:
            error_string = (
                f"Ensure that you have only one .pth checkpoint file in your registered model. "
                f"Found {len(checkpoint_files)}"
            )
            raise LLMException._with_error(
                AzureMLError.create(LLMInternalError, error=error_string)
            )
        # Assume checkpoint is in the parent folder
        checkpoint_file_name = checkpoint_files[0].replace(abs_input_model_path, input_model_path)

        if self.pytorch_model is not None:
            self.pytorch_model = mmlab_config_path
        elif self.mlflow_model is not None:
            self.mlflow_model = mmlab_config_path

        return {
            ModelSelectorConstants.MODEL_NAME: self.model_name,
            ModelSelectorConstants.MLFLOW_MODEL_PATH: self.mlflow_model,
            ModelSelectorConstants.PYTORCH_MODEL_PATH: self.pytorch_model,
            ImageModelSelectorConstants.MMLAB_MODEL_WEIGHTS_PATH_OR_URL: checkpoint_file_name
        }

    def _prepare_mmlab_arguments_from_model_zoo_config(self) -> dict:
        """Prepared arguments for MMLAB/MMDetection models using the model name as in MMDetection model zoo.

        :return: A dictinary conatining argument name to value mapping to update.
        :rtype: dictionary
        """
        # Todo - add the functionality to prepare from model zoo config
        raise NotImplementedError(
            "Supporting from MMDetection model zoo is not implemented yet."
        )
        # # Uncomment the below when enabling the support
        # if self.pytorch_model is None and self.mlflow_model is None and self.model_name is None:
        #     error_string = (
        #             f"All, model_name:{self.model_name}, mlflow_model: {self.mlflow_model},"
        #             f" pytorch_model: {self.pytorch_model} can not be None together."
        #             f"Please provide either a model via pytorch_model or mlflow_model port; Or, "
        #             f"provide name of the model from MMDetcetion model zoo, as specified in respective model"
        #             " model family's metafile.yaml."
        #         )
        #     raise LLMException._with_error(
        #         AzureMLError.create(LLMInternalError, error=error_string)
        #     )

    def _prepare_mmlab_arguments(self) -> dict:
        """Prepare an update for the keyword arguments (if present) with required key-val items for MMLab/MMDetection
        models.

        :return: A dictinary conatining argument name to value mapping to update.
        :rtype: dictionary
        """

        if self.pytorch_model is not None or self.mlflow_model is not None:
            return self._prepare_mmlab_arguments_from_input_model()
        else:
            # Todo - add the support for reading from model zoo config.
            return self._prepare_mmlab_arguments_from_model_zoo_config()

    def _prepare_and_logs_arguments(self) -> None:
        """Update the keyword arguments (if present) with required key-val items and
        Store the model selector arguments to json file.
        """
        arguments = {
            ModelSelectorConstants.MLFLOW_MODEL_PATH: self.mlflow_model,
            ModelSelectorConstants.PYTORCH_MODEL_PATH: self.pytorch_model,
            ModelSelectorConstants.MODEL_NAME: self.model_name,
            ImageModelSelectorConstants.MODEL_FAMILY: self.model_family
        }

        if self.model_family == MODEL_FAMILY_CLS.MMDETECTION_IMAGE:
            arguments.update(self._prepare_mmlab_arguments())

        if self.keyword_arguments:
            self.keyword_arguments.update(arguments)
        else:
            self.keyword_arguments = arguments

        os.makedirs(self.output_dir, exist_ok=True)
        model_selector_args_save_path = os.path.join(
            self.output_dir, ModelSelectorDefaults.MODEL_SELECTOR_ARGS_SAVE_PATH
        )
        logger.info(
            f"Saving the model selector args to {model_selector_args_save_path}"
        )
        with open(model_selector_args_save_path, "w") as output_file:
            json.dump(self.keyword_arguments, output_file, indent=2)
