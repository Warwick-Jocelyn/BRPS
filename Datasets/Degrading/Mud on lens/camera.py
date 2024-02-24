from math import floor
from turtle import shape
from typing import Tuple

import cv2
import numpy as np

from . import distortion


def apply_pattern(image: np.ndarray, pattern: np.ndarray) -> np.ndarray:

    channels = image.shape[2] if len(image.shape) > 2 else 1
    out_image = np.zeros(image.shape, dtype=np.uint8)
    for c in range(channels):
        out_image[:, :, c] = np.round(image[:, :, c] * pattern)

    return out_image


class GaussianSoiledNoise(distortion.CameraDistortionModel):

    noise_pattern: np.ndarray

    def __init__(
        self,
        image_shape: Tuple[int, int],
        max_intensity: float,
        drop_min_size: int,
        drop_max_size: int,
        num_drops,
    ) -> None:
        super().__init__()

        assert len(image_shape) == 2
        assert 0 <= max_intensity <= 1
        assert drop_min_size % 2 == 1
        assert drop_max_size % 2 == 1
        assert drop_min_size < drop_max_size

        h, w = image_shape
        self.noise_pattern = np.ones((h, w), np.float32)
        h_points = np.random.randint(0, h, num_drops)
        w_points = np.random.randint(0, w, num_drops)

        for p_r, p_c in zip(h_points, w_points):

            # kernel_size = int(
            #    np.random.normal(
            #        loc=(drop_min_size + drop_max_size) // 2,
            #        scale=(drop_max_size - drop_min_size),
            #    )
            # )
            kernel_size = np.random.choice(range(drop_min_size, drop_max_size, 2))
            # if kernel_size % 2 == 0:
            #    kernel_size += 1

            kernel_1d: np.ndarray = cv2.getGaussianKernel(kernel_size, -1)
            kernel = kernel_1d @ kernel_1d.reshape((1, -1))
            kernel = cv2.normalize(kernel, None, 0, max_intensity, cv2.NORM_MINMAX)
            kernel = 1 - kernel
            half_size = kernel_size // 2

            image_min_r = max(p_r - half_size, 0)
            image_max_r = min(p_r + half_size + 1, h)
            image_min_c = max(p_c - half_size, 0)
            image_max_c = min(p_c + half_size + 1, w)

            kernel_min_r = abs(min(p_r - half_size, 0))
            kernel_max_r = kernel_size - abs(min(h - (p_r + half_size + 1), 0))
            kernel_min_c = abs(min(p_c - half_size, 0))
            kernel_max_c = kernel_size - abs(min(w - (p_c + half_size + 1), 0))

            self.noise_pattern[
                image_min_r:image_max_r, image_min_c:image_max_c
            ] *= kernel[kernel_min_r:kernel_max_r, kernel_min_c:kernel_max_c]

            # for i in range(kernel_size):
            #    for j in range(kernel_size):
            #        image_r = p_r - half_size + i
            #        image_c = p_c - half_size + j
            #        if image_r >= 0 and image_r < h and image_c >= 0 and image_c < w:
            #            self.noise_pattern[image_r, image_c] *= kernel[i, j]

    def apply(self, image: np.ndarray) -> np.ndarray:
        return apply_pattern(image, self.noise_pattern)


class BoxSoiledNoise(distortion.CameraDistortionModel):

    kernel: np.ndarray
    gaussian_kernel_size: Tuple[int, int]
    gaussian_sigma: Tuple[float, float]

    def __init__(
        self,
        soiled_kernel_size: tuple,
        soiled_intensity: float = 0.5,
        gaussian_kernel_size: tuple = (9, 9),
        gaussian_sigma: tuple = (0.5, 0.5),
    ) -> None:
        """Add soiled pattern noise to image
        TODO: review

        The function first computes a kernel of size soiled_kernel_size with uniform random distribution in [0,1).
        Then scales the kernel up to the image size and smooths it with a Gaussian Blur filter.
        Finally, blends the kernel on top of the image, creating a soiled effect.

        Parameters:
        soiled_kernel_size (tuple): 2 elements kernel size (rows, cols)
        soiled_intensity (float): intensity of the noise in range [0, 1] (default 0.5). Put 0 to disable it
        gaussian_kernel_size (tuple): 2 elements kernel size for Gaussian Blur filter (default (9,9))
        gaussian_sigma (tuple): 2 elements sigma values for Gaussian Blur filter (default (.5, .5))

        Returns:
        np.ndarray: OpenCV image with soiled noise applied
        """

        super().__init__()

        self.gaussian_kernel_size = gaussian_kernel_size
        self.gaussian_sigma = gaussian_sigma
        self.kernel = np.random.rand(*soiled_kernel_size)
        self.kernel[self.kernel < (1 - soiled_intensity)] = 1

    def apply(self, image: np.ndarray) -> np.ndarray:

        image_rows, image_cols, _ = image.shape

        # TODO: is INTER_LINEAR_EXACT interpolation correct?
        scaled_kernel = cv2.resize(
            self.kernel, (image_cols, image_rows), interpolation=cv2.INTER_LINEAR_EXACT
        )

        self.blurred_kernel = cv2.GaussianBlur(
            scaled_kernel,
            self.gaussian_kernel_size,
            sigmaX=self.gaussian_sigma[0],
            sigmaY=self.gaussian_sigma[1],
        )

        return apply_pattern(image, self.blurred_kernel)
