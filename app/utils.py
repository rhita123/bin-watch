from PIL import Image as PILImage
import os

def extract_features(image_path):
    with PILImage.open(image_path) as img:
        width, height = img.size
        pixels = list(img.getdata())
        num_pixels = len(pixels)

        avg_red = sum(p[0] for p in pixels) / num_pixels
        avg_green = sum(p[1] for p in pixels) / num_pixels
        avg_blue = sum(p[2] for p in pixels) / num_pixels

        size_kb = os.path.getsize(image_path) / 1024

        return {
            'width': width,
            'height': height,
            'file_size_kb': size_kb,
            'avg_red': avg_red,
            'avg_green': avg_green,
            'avg_blue': avg_blue
        }