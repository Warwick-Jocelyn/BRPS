from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np


class DistortionModel(ABC):
    @abstractmethod
    def apply(self, data: Any) -> Any:
        pass


class CameraDistortionModel(DistortionModel):
    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        pass


class DistortionSequence(DistortionModel):

    models: List[DistortionModel]

    def __init__(self) -> None:
        self.models = list()

    def add_distortion(self, model: DistortionModel) -> DistortionModel:
        self.models.append(model)
        return self

    def apply(self, data: Any) -> Any:
        for model in self.models:
            data = model.apply(data)
        return data
