import traceback
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot
from PIL import Image
from algorithms import DitherAlgorithms

class ImageProcessor(QObject):
    finished = Signal(Image.Image, list)
    error = Signal(str)

    def __init__(self, pil_image, dither_params):
        super().__init__()
        self.pil_image = pil_image
        self.dither_params = dither_params

    @Slot()
    def run(self):
        try:
            params = self.dither_params
            palette_name = params['palette_name']
            num_colors = params['num_colors']
            
            if palette_name == "Auto (From Image)":
                quant_img = self.pil_image.quantize(colors=num_colors)
                palette_rgb = [quant_img.getpalette()[i:i+3] for i in range(0, len(quant_img.getpalette()), 3)]
            elif palette_name == "Grayscale":
                palette_rgb = [[int(i)]*3 for i in np.linspace(0, 255, num_colors)]
            else:
                palette_rgb = DitherAlgorithms.PREDEFINED_PALETTES[palette_name]
            
            strength_float = params['dither_strength'] / 100.0
            algo = params['algorithm_name']

            if algo == "Floyd-Steinberg": processed_image = DitherAlgorithms.floyd_steinberg(self.pil_image, palette_rgb, strength_float)
            elif algo == "Atkinson": processed_image = DitherAlgorithms.atkinson(self.pil_image, palette_rgb, strength_float)
            elif algo == "Jarvis, Judice, Ninke": processed_image = DitherAlgorithms.jnn(self.pil_image, palette_rgb, strength_float)
            elif algo == "Stucki": processed_image = DitherAlgorithms.stucki(self.pil_image, palette_rgb, strength_float)
            elif algo == "Bayer (Ordered)": processed_image = DitherAlgorithms.bayer(self.pil_image, palette_rgb, strength_float)
            elif algo == "Clustered Dot Halftone": processed_image = DitherAlgorithms.clustered_dot_halftone(self.pil_image, palette_rgb, strength_float)
            elif algo == "Random": processed_image = DitherAlgorithms.random(self.pil_image, palette_rgb, strength_float)
            else: raise NotImplementedError(f"Algorithm '{algo}' is not implemented.")

            self.finished.emit(processed_image, palette_rgb)
        except Exception:
            self.error.emit(traceback.format_exc())