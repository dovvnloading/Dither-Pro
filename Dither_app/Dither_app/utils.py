from PIL import Image

class ImageUtils:
    AVAILABLE_LUTS = ["Sepia", "Invert", "Cool"]
    _lut_cache = {}
    
    @staticmethod
    def apply_lut(image: Image.Image, lut_name: str) -> Image.Image:
        if lut_name == "Sepia":
            sepia_matrix = (
                0.393, 0.769, 0.189, 0,
                0.349, 0.686, 0.168, 0,
                0.272, 0.534, 0.131, 0)
            return image.convert("RGB", sepia_matrix)
        
        if lut_name not in ImageUtils._lut_cache:
            if lut_name == "Invert":
                ImageUtils._lut_cache[lut_name] = bytes([255 - i for i in range(256)]) * 3
            elif lut_name == "Cool":
                r = [int(c * 0.8) for c in range(256)]
                g = [int(c * 0.9) for c in range(256)]
                b = [int(min(255, c * 1.2)) for c in range(256)]
                ImageUtils._lut_cache[lut_name] = bytes(r + g + b)

        lut_data = ImageUtils._lut_cache.get(lut_name)
        if not lut_data:
            return image
            
        return image.point(lut_data)