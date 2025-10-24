import numpy as np
import numba
from PIL import Image

@numba.jit(nopython=True)
def _jit_find_closest_palette_color(pixel, palette):
    min_dist_sq = np.inf; best_color = palette[0]
    for color in palette:
        dist_sq = np.sum((pixel - color)**2)
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq; best_color = color
    return best_color

@numba.jit(nopython=True)
def _jit_apply_quantization(img_array, palette):
    height, width, _ = img_array.shape; quantized_array = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            quantized_array[y, x] = _jit_find_closest_palette_color(img_array[y, x], palette)
    return quantized_array

@numba.jit(nopython=True)
def _jit_apply_floyd_steinberg(img_array, palette):
    height, width, _ = img_array.shape
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy(); new_pixel = _jit_find_closest_palette_color(old_pixel, palette)
            img_array[y, x] = new_pixel; quant_error = old_pixel - new_pixel
            if x + 1 < width: img_array[y, x + 1] += quant_error * 7.0 / 16.0
            if x - 1 >= 0 and y + 1 < height: img_array[y + 1, x - 1] += quant_error * 3.0 / 16.0
            if y + 1 < height: img_array[y + 1, x] += quant_error * 5.0 / 16.0
            if x + 1 < width and y + 1 < height: img_array[y + 1, x + 1] += quant_error * 1.0 / 16.0
    return img_array

@numba.jit(nopython=True)
def _jit_apply_atkinson(img_array, palette):
    height, width, _ = img_array.shape
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy(); new_pixel = _jit_find_closest_palette_color(old_pixel, palette)
            img_array[y, x] = new_pixel; quant_error = old_pixel - new_pixel; error_share = quant_error / 8.0
            if x + 1 < width: img_array[y, x + 1] += error_share
            if x + 2 < width: img_array[y, x + 2] += error_share
            if x - 1 >= 0 and y + 1 < height: img_array[y + 1, x - 1] += error_share
            if y + 1 < height: img_array[y + 1, x] += error_share
            if x + 1 < width and y + 1 < height: img_array[y + 1, x + 1] += error_share
            if y + 2 < height: img_array[y + 2, x] += error_share
    return img_array

@numba.jit(nopython=True)
def _jit_apply_jnn(img_array, palette):
    height, width, _ = img_array.shape
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy(); new_pixel = _jit_find_closest_palette_color(old_pixel, palette)
            img_array[y, x] = new_pixel; quant_error = old_pixel - new_pixel
            if x + 1 < width: img_array[y, x + 1] += quant_error * 7.0 / 48.0
            if x + 2 < width: img_array[y, x + 2] += quant_error * 5.0 / 48.0
            if y + 1 < height:
                if x - 2 >= 0: img_array[y + 1, x - 2] += quant_error * 3.0 / 48.0
                if x - 1 >= 0: img_array[y + 1, x - 1] += quant_error * 5.0 / 48.0
                img_array[y + 1, x] += quant_error * 7.0 / 48.0
                if x + 1 < width: img_array[y + 1, x + 1] += quant_error * 5.0 / 48.0
                if x + 2 < width: img_array[y + 1, x + 2] += quant_error * 3.0 / 48.0
            if y + 2 < height:
                if x - 2 >= 0: img_array[y + 2, x - 2] += quant_error * 1.0 / 48.0
                if x - 1 >= 0: img_array[y + 2, x - 1] += quant_error * 3.0 / 48.0
                img_array[y + 2, x] += quant_error * 5.0 / 48.0
                if x + 1 < width: img_array[y + 2, x + 1] += quant_error * 3.0 / 48.0
                if x + 2 < width: img_array[y + 2, x + 2] += quant_error * 1.0 / 48.0
    return img_array

@numba.jit(nopython=True)
def _jit_apply_stucki(img_array, palette):
    height, width, _ = img_array.shape
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy(); new_pixel = _jit_find_closest_palette_color(old_pixel, palette)
            img_array[y, x] = new_pixel; quant_error = old_pixel - new_pixel
            if x + 1 < width: img_array[y, x + 1] += quant_error * 8.0 / 42.0
            if x + 2 < width: img_array[y, x + 2] += quant_error * 4.0 / 42.0
            if y + 1 < height:
                if x - 2 >= 0: img_array[y + 1, x - 2] += quant_error * 2.0 / 42.0
                if x - 1 >= 0: img_array[y + 1, x - 1] += quant_error * 4.0 / 42.0
                img_array[y + 1, x] += quant_error * 8.0 / 42.0
                if x + 1 < width: img_array[y + 1, x + 1] += quant_error * 4.0 / 42.0
                if x + 2 < width: img_array[y + 1, x + 2] += quant_error * 2.0 / 42.0
            if y + 2 < height:
                if x - 2 >= 0: img_array[y + 2, x - 2] += quant_error * 1.0 / 42.0
                if x - 1 >= 0: img_array[y + 2, x - 1] += quant_error * 2.0 / 42.0
                img_array[y + 2, x] += quant_error * 4.0 / 42.0
                if x + 1 < width: img_array[y + 2, x + 1] += quant_error * 2.0 / 42.0
                if x + 2 < width: img_array[y + 2, x + 2] += quant_error * 1.0 / 42.0
    return img_array

@numba.jit(nopython=True)
def _jit_apply_bayer_palette(img_array, palette):
    height, width, _ = img_array.shape; dithered_array = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            dithered_array[y,x] = _jit_find_closest_palette_color(img_array[y,x], palette)
    return dithered_array

class DitherAlgorithms:
    PREDEFINED_PALETTES = {
        "Game Boy": [[15, 56, 15], [48, 98, 48], [139, 172, 15], [155, 188, 15]],
        "PICO-8": [[0,0,0], [29,43,83], [126,37,83], [0,135,81], [171,82,54], [95,87,79], [194,195,199], [255,241,232], [255,0,77], [255,163,0], [255,236,39], [0,228,54], [41,173,255], [131,118,156], [255,119,168], [255,204,170]],
        "CGA": [[0,0,0], [0,170,0], [170,0,0], [170,85,0]]
    }
    @staticmethod
    def _process_error_diffusion(image: Image.Image, palette_array: np.ndarray, strength: float, func) -> Image.Image:
        img_array = np.array(image, dtype=np.float64)
        if strength < 1.0: quantized_array = _jit_apply_quantization(img_array.copy(), palette_array)
        dithered_array = func(img_array, palette_array)
        if strength < 1.0: final_array = (dithered_array * strength) + (quantized_array * (1.0 - strength))
        else: final_array = dithered_array
        final_array = np.clip(final_array, 0, 255).astype(np.uint8)
        return Image.fromarray(final_array)
    @staticmethod
    def floyd_steinberg(image: Image.Image, palette: list, strength: float) -> Image.Image:
        palette_array = np.array(palette, dtype=np.float64); return DitherAlgorithms._process_error_diffusion(image, palette_array, strength, _jit_apply_floyd_steinberg)
    @staticmethod
    def atkinson(image: Image.Image, palette: list, strength: float) -> Image.Image:
        palette_array = np.array(palette, dtype=np.float64); return DitherAlgorithms._process_error_diffusion(image, palette_array, strength, _jit_apply_atkinson)
    @staticmethod
    def jnn(image: Image.Image, palette: list, strength: float) -> Image.Image:
        palette_array = np.array(palette, dtype=np.float64); return DitherAlgorithms._process_error_diffusion(image, palette_array, strength, _jit_apply_jnn)
    @staticmethod
    def stucki(image: Image.Image, palette: list, strength: float) -> Image.Image:
        palette_array = np.array(palette, dtype=np.float64); return DitherAlgorithms._process_error_diffusion(image, palette_array, strength, _jit_apply_stucki)
    @staticmethod
    def _apply_ordered_dither(image: Image.Image, palette: list, strength: float, matrix: np.ndarray) -> Image.Image:
        img_array = np.array(image, dtype=np.float64); height, width, _ = img_array.shape; palette_array = np.array(palette, dtype=np.float64)
        m_size = matrix.shape[0]
        tiled_matrix = np.tile(matrix, (height // m_size + 1, width // m_size + 1))[:height, :width]
        factor = strength * (m_size**2 / 2.0)
        threshold = (tiled_matrix / (m_size**2) - 0.5) * factor
        threshold = np.expand_dims(threshold, axis=2)
        img_array += threshold
        dithered_array = _jit_apply_bayer_palette(img_array, palette_array)
        dithered_array = np.clip(dithered_array, 0, 255).astype(np.uint8)
        return Image.fromarray(dithered_array)
    @staticmethod
    def bayer(image: Image.Image, palette: list, strength: float) -> Image.Image:
        bayer_matrix_8x8 = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]])
        return DitherAlgorithms._apply_ordered_dither(image, palette, strength, bayer_matrix_8x8)
    @staticmethod
    def clustered_dot_halftone(image: Image.Image, palette: list, strength: float) -> Image.Image:
        halftone_matrix_4x4 = np.array([[12,5,6,13],[4,0,1,7],[8,2,3,9],[15,11,10,14]])
        return DitherAlgorithms._apply_ordered_dither(image, palette, strength, halftone_matrix_4x4)
    @staticmethod
    def random(image: Image.Image, palette: list, strength: float) -> Image.Image:
        img_array = np.array(image, dtype=np.float64)
        palette_array = np.array(palette, dtype=np.float64)
        noise = np.random.uniform(-1, 1, img_array.shape) * (strength * 25)
        img_array += noise
        dithered_array = _jit_apply_bayer_palette(img_array, palette_array)
        dithered_array = np.clip(dithered_array, 0, 255).astype(np.uint8)
        return Image.fromarray(dithered_array)