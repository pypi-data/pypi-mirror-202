from pathlib import Path

import cv2
from cv2 import (
    imwrite as __cv2_imwrite,
    cvtColor as __cv2_cvtColor
)

import numpy as np
from numpy import (
    array as __np_array,
    ndarray as __np_ndarray
)

import PIL.Image
__PIL_Image_open = PIL.Image.open
__PIL_Image_Image = PIL.Image.Image

from katalytic.files import copy_file
from katalytic.pkg import get_version

__version__, __version_info__ = get_version(__name__)


def load_image(image, mode=None):
    if not(mode is None or isinstance(mode, str)):
        raise TypeError(f'mode expected None or str. Got {type(mode)!r}')

    if isinstance(image, (str, Path)):
        return __np_array(__PIL_Image_open(image))
    elif isinstance(image, __PIL_Image_Image):
        return __np_array(image)
    elif isinstance(image, __np_ndarray):
        return image.copy()
    else:
        raise TypeError(f'type(image) = {type(image)!r}')


def save_image(image, path, *, exists='error', mode='RGB'):
    if not isinstance(mode, str):
        raise ValueError(f'type(mode) = {type(mode)!r}')
    elif exists not in ('error', 'skip', 'replace'):
        raise ValueError(f'exists must be one of \'error\', \'skip\', \'replace\'. Got {exists!r}')

    if Path(path).exists():
        if exists == 'error':
            raise FileExistsError(f'[Errno 17] File exists: {str(path)!r}')
        elif exists == 'skip':
            return

    if isinstance(image, __PIL_Image_Image):
        image = __np_array(image)

    if isinstance(image, __np_ndarray):
        if mode != 'BGR':
            image = convert_image(image, mode, 'BGR')

        __cv2_imwrite(str(path), image)
    elif isinstance(image, (str, Path)):
        copy_file(image, path, exists=exists)
    else:
        raise TypeError(f'type(image) = {type(image)!r}')


def convert_image(image, before, after):
    if not isinstance(before, str):
        raise ValueError(f'type(before) = {type(before)!r}')
    elif not isinstance(after, str):
        raise ValueError(f'type(after) = {type(after)!r}')

    return_PIL = isinstance(image, PIL.Image.Image)
    image = load_image(image)

    conversion_code = f'COLOR_{before}2{after}'
    conversion_code = conversion_code.replace('gray', 'GRAY')
    conversion_code = getattr(cv2, conversion_code, None)

    if conversion_code:
        img = __cv2_cvtColor(image, conversion_code)
    elif before.startswith('binary') or after.startswith('binary'):
        raise NotImplementedError
    else:
        raise ValueError

    if return_PIL:
        return PIL.Image.fromarray(img)
    else:
        return img


def images_are_equal(image_1, image_2, check_type=False):
    image_1 = load_image(image_1)
    image_2 = load_image(image_2)
    if check_type and image_1.dtype != image_2.dtype:
        return False

    return (image_1 == image_2).all()
