# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""MMDetection modules."""

import torch
import numpy as np

from dataclasses import dataclass
from mmcv import Config
from pathlib import Path
from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence
from typing import Dict, List, Union, Any, Tuple

from common_constants import MmDetectionDatasetLiterals


@dataclass
class ImageMetadata:
    """Dataclass for maintaining the metadata dictionary as required for MM detection models.
    The keys of metadata dictionary is same as the property name."""

    ori_shape: Tuple[int, int, int]
    img_shape: Tuple[int, int, int] = None
    pad_shape: Tuple[int, int, int] = None
    scale_factor: Tensor = torch.as_tensor([1, 1, 1, 1])
    flip: bool = False
    flip_direction: str = None
    filename: str = None
    ori_filename: str = None

    def __post_init__(self):
        """If image shape after resizing and padding is not provided then assign it with original shape"""
        self.img_shape = self.ori_shape or self.img_shape
        self.pad_shape = self.ori_shape or self.pad_shape


class ObjectDetectionModelWrapper(nn.Module):
    """Wrapper class over object detection model of MMDetection."""
    def __init__(
        self,
        mm_object_detection_model: nn.Module,
        config: Config,
        model_name_or_path: str = None,
    ):
        """Wrapper class over object detection model of MMDetection.

        :param mm_object_detection_model: MM object detection model
        :type mm_object_detection_model: nn.Module
        :param config: MM Detection model configuration
        :type config: MMCV Config
        :param model_name_or_path: model name or path
        :type model_name_or_path: str
        """

        super().__init__()
        self.model = mm_object_detection_model
        self.config = config
        self.model_name = Path(model_name_or_path).stem

    @classmethod
    def _get_bboxes_and_labels(
        cls, predicted_bbox: List[List[np.ndarray]]
    ) -> Tuple[Tensor, Tensor]:
        """
        Map the MM detection model"s predicted label to the bbox and labels
        :param predicted_bbox: bbox of shape [Number of labels, Number of boxes, 5 [tl_x, tl_y, br_x, br_y,
        box_score]] format.
        :type predicted_bbox: List[List[np.ndarray]]
        :return: bounding boxes of shape [Number of boxes, 5 [tl_x, tl_y, br_x, br_y, box_score]] and labels of
        shape [Number of boxes, label id]
        :rtype: Tuple[Tensor, Tensor]
        """
        bboxes = torch.as_tensor(np.vstack(predicted_bbox))
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(predicted_bbox)
        ]
        labels = torch.as_tensor(np.concatenate(labels))
        return bboxes, labels

    @classmethod
    def _pad_sequence(cls, sequences: Tensor, padding_value: float = -1, batch_first: bool = True) -> Tensor:
        """
        It stacks a list of Tensors sequences, and pads them to equal length.
        :param sequences: list of variable length sequences.
        :type sequences: Tensor
        :param padding_value: value for padded elements
        :type padding_value: float
        :param batch_first: output will be in B x T x * if True, or in T x B x * otherwise
        :type batch_first: bool
        :return: Tensor of size ``B x T x *`` if batch_first is True
        :rtype: Tensor
        """
        return pad_sequence(sequences, padding_value=padding_value, batch_first=batch_first)

    @classmethod
    def _organize_predictions_for_trainer(
        cls, batch_predictions: List[List[np.ndarray]], img_metas: List[Dict]
    ) -> Dict[str, Tensor]:
        """
        Transform the batch of predicted labels as required by the HF trainer.
        :param batch_predictions: batch of predicted labels
        :type batch_predictions: List of bbox list for each image
        :param img_metas: batch of predicted labels
        :type img_metas: List of image metadata dictionary
        :return: Dict of predicted labels in tensor format
        :rtype: Dict[str, Tensor]

        Note: Same reasoning like _organize_ground_truth_for_trainer function but for predicted label
        """
        batch_bboxes, batch_labels = [], []
        for prediction in batch_predictions:
            bboxes, labels = ObjectDetectionModelWrapper._get_bboxes_and_labels(
                prediction
            )
            batch_bboxes.append(bboxes)
            batch_labels.append(labels)

        output = dict()
        output[MmDetectionDatasetLiterals.BBOXES] = ObjectDetectionModelWrapper._pad_sequence(batch_bboxes)
        output[MmDetectionDatasetLiterals.LABELS] = ObjectDetectionModelWrapper._pad_sequence(batch_labels)
        return output

    def forward(
        self, **data
    ) -> Union[Dict[str, Any], Tuple[Tensor, Dict[str, Tensor]]]:
        """
        Model forward pass for training and validation mode
        :param data: Input data to model
        :type data: Dict
        :return: A dictionary of loss components in training mode OR Tuple of dictionary of predicted and ground
        labels in validation mode
        :rtype: Dict[str, Any] in training mode; Tuple[Tensor, Dict[str, Tensor]] in validation mode;

        Note: Input data dictionary consist of
            img: Tensor of shape (N, C, H, W) encoding input images.
            img_metas: list of image info dict where each dict has: "img_shape", "scale_factor", "flip",
             and may also contain "filename", "ori_shape", "pad_shape", and "img_norm_cfg". For details on the values
             of these keys see `mmdet/datasets/pipelines/formatting.py:Collect`.
            gt_bboxes - Ground truth bboxes for each image with shape (num_gts, 4) in [tl_x, tl_y, br_x, br_y] format.
            gt_labels - List of class indices corresponding to each box
            gt_crowds - List of "is crowds" (boolean) to each box
            gt_masks - List of masks (type BitmapMasks) for each image if task is instance_segmentation
        """
        # test mode
        img = data[MmDetectionDatasetLiterals.IMG]
        img_metas = data[MmDetectionDatasetLiterals.IMG_METAS]
        batch_predictions = self.model(
            img=[img], img_metas=[img_metas], return_loss=False
        )
        output: dict = self._organize_predictions_for_trainer(
            batch_predictions, img_metas
        )

        return torch.asarray([]), output
