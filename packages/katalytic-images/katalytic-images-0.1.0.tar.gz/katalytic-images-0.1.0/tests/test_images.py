from pathlib import Path

import numpy as np
import PIL.Image
import pytest
from PIL import Image

from katalytic.files import get_unique_path
from katalytic.images import convert_image, images_are_equal, load_image, save_image


class Test_convert_image:
    """TODO:
    - implement all with image as str/Path
    - if image is ndarray/Image -> you have to try infering what kind of mode it has
        - 4 channels -> rgba or hsva (or a weird one, but you can ignore that)
        - 3 ch -> rgb / hsv / Lab
            - how do I differentiate between them?
                - can I do it based on type or channel ranges?
                - can I use the gray world hypothesis
        - 1 ch and only 2 values -> binary x (nonzero, th, adaptive, otsu) x (1, 255, True) x ('inv', '')
        - 1 ch and (==0 or >= 3 values) -> gray
    - should I handle images saved as float differently?
    - for the binary cases I can split the mode str and parse the sequence
        - this will let me handle all cases with less code
        - e.g. 'binary_otsu_True_inv'.split('_') -> ['binary', 'otsu', 'True', 'inv'] ->
            - type = bool
            - values = False/True
            - invert bg with fg
            - use otsu
    """
    def test_returns_PIL_if_PIL(self):
        img = PIL.Image.fromarray(_create_RGB())
        img2 = convert_image(img, 'RGB', 'BGR')
        assert isinstance(img2, PIL.Image.Image)

    def test_returns_numpy_if_numpy(self):
        img = _create_RGB()
        img2 = convert_image(img, 'RGB', 'BGR')
        assert isinstance(img2, np.ndarray)

    def test_returns_numpy_if_str(self):
        path = get_unique_path('/tmp/{}.png')
        save_image(_create_RGB(), path)
        img2 = convert_image(path, 'RGB', 'BGR')
        assert isinstance(img2, np.ndarray)

    def test_returns_numpy_if_Path(self):
        path = Path(get_unique_path('/tmp/{}.png'))
        save_image(_create_RGB(), path)
        img2 = convert_image(path, 'RGB', 'BGR')
        assert isinstance(img2, np.ndarray)

    @pytest.mark.xfail(reason='Not implemented')
    def test_convert_binary(self):
        img = np.array([[[0, 0, 0], [255, 255, 255]]])
        img2 = convert_image(img, 'RGB', 'binary')
        assert np.all(img2 == img.astype(bool).astype(np.uint8))

    def test_convert_to_unknown(self):
        img = np.array([[[0, 0, 0], [255, 255, 255]]])
        with pytest.raises(ValueError):
            _ = convert_image(img, 'RGB', 'unknown')

    def test_convert_from_unknown(self):
        img = np.array([[[0, 0, 0], [255, 255, 255]]])
        with pytest.raises(ValueError):
            _ = convert_image(img, 'unknown', 'RGB')

    @pytest.mark.parametrize('before', [1, True, None, [], {}, (), object()])
    def test_save_raises_ValueError_for_before(self, before):
        with pytest.raises(ValueError):
            convert_image(_create_RGB(), before, 'RGB')

    @pytest.mark.parametrize('after', [1, True, None, [], {}, (), object()])
    def test_save_raises_ValueError_for_after(self, after):
        with pytest.raises(ValueError):
            convert_image(_create_RGB(), 'RGB', after)


class Test_images_are_equal:
    def test_equal(self):
        img_1 = _create_RGB()
        img_2 = img_1.copy()
        assert images_are_equal(img_1, img_2)

        img_1 = _create_RGB(np.float32)
        img_2 = img_1.astype(np.uint8)
        assert images_are_equal(img_1, img_2)

        img_1 = np.array([[0,1], [2,3]]).astype(np.uint8)
        img_2 = img_1.copy()
        assert images_are_equal(img_1, img_2)

    def test_not_equal(self):
        img_1 = np.array([[1, 2], [3, 4]])
        img_2 = np.array([[3, 4], [1, 2]])
        assert not images_are_equal(img_1, img_2)

    def test_not_equal_type(self):
        img_1 = _create_RGB(np.float32)
        img_2 = img_1.astype(np.uint8)
        assert not images_are_equal(img_1, img_2, check_type=True)


class Test_load_and_save:
    def test_str(self):
        image_1 = _create_RGB()
        path = get_unique_path('/tmp/{}.png')
        save_image(image_1, path)
        assert images_are_equal(image_1, load_image(path))

    def test_Path(self):
        image_1 = _create_RGB()
        path = Path(get_unique_path('/tmp/{}.png'))
        save_image(image_1, path)
        assert images_are_equal(image_1, load_image(path))

    def test_save_PIL_Image(self):
        image_1 = _create_RGB()
        path = Path(get_unique_path('/tmp/{}.png'))
        save_image(Image.fromarray(image_1), path)
        assert images_are_equal(image_1, load_image(path))

    def test_load_PIL_Image(self):
        image_1 = _create_RGB()
        path = Path(get_unique_path('/tmp/{}.png'))
        save_image(image_1, path)
        assert images_are_equal(image_1, load_image(Image.fromarray(image_1)))

    def test_load_returns_copy(self):
        img = _create_RGB()
        img_copy = load_image(img)
        img[0][0] = [255, 255, 255]
        assert not images_are_equal(img, img_copy)

    def test_path_exists_replace(self):
        path = get_unique_path('/tmp/{}.png')
        Path(path).touch()

        img = _create_RGB()
        save_image(img, path, exists='replace')
        assert images_are_equal(load_image(path), img)

    def test_save_uses_copy_file(self):
        path = get_unique_path('/tmp/{}.png')
        save_image(_create_RGB(), path)

        path2 = get_unique_path('/tmp/{}.png')
        save_image(path, path2, exists='replace')

        assert images_are_equal(load_image(path2), load_image(path))

    def test_path_exists_skip(self):
        path = get_unique_path('/tmp/{}.png')
        img = _create_RGB()
        save_image(img, path)

        img2 = convert_image(img, 'RGB', 'BGR')
        save_image(img2, path, exists='skip')
        assert not images_are_equal(load_image(path), img2)

    def test_path_exists_error(self):
        path = get_unique_path('/tmp/{}.png')
        Path(path).touch()

        with pytest.raises(FileExistsError):
            save_image(_create_RGB(), path, exists='error')

    @pytest.mark.parametrize('img', [1, True, None, [], {}, (), object()])
    def test_load_raises_TypeError_for_image(self, img):
        with pytest.raises(TypeError):
            load_image(img)

    @pytest.mark.parametrize('mode', [1, True, [], {}, (), object()])
    def test_load_raises_TypeError_for_mode(self, mode):
        with pytest.raises(TypeError):
            load_image('img.png', mode)

    @pytest.mark.parametrize('path', [1, True, None, [], {}, (), object()])
    def test_save_raises_TypeError_for_path(self, path):
        with pytest.raises(TypeError):
            save_image(_create_RGB(), path)

    @pytest.mark.parametrize('image', [1, True, None, [], {}, (), object()])
    def test_save_raises_TypeError_for_image(self, image):
        with pytest.raises(TypeError):
            save_image(image, get_unique_path('/tmp/{}.png'))

    @pytest.mark.parametrize('mode', ['unkonwn', '', 1, True, None, [], {}, (), object()])
    def test_save_raises_ValueError_for_mode(self, mode):
        with pytest.raises(ValueError):
            save_image(_create_RGB(), get_unique_path('/tmp/{}.png'), mode=mode)

    @pytest.mark.parametrize('exists', ['unkonwn', '', 1, True, None, [], {}, (), object()])
    def test_save_raises_ValueError_for_exists(self, exists):
        with pytest.raises(ValueError):
            save_image(_create_RGB(), get_unique_path('/tmp/{}.png'), exists=exists)


def _create_RGB(dtype=np.uint8):
    return np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],        # RGB
        [[0, 255, 255], [255, 0, 255], [255, 255, 0]],  # CMY
        [[0, 0, 255], [0, 255, 0], [255, 0, 0]],        # BGR
        [[0, 0, 0], [128, 128, 128], [255, 255, 255]],  # black, gray, white
    ], dtype=dtype)
