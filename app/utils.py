from PIL import Image as PILImage
import os

# Extrait des caractéristiques d'une image : dimensions, taille en ko, et moyennes des couleurs RVB
def extract_features(image_path):
    with PILImage.open(image_path) as img:
        # Récupère les dimensions de l'image
        width, height = img.size
        # Récupère tous les pixels de l'image sous forme de liste
        pixels = list(img.getdata())
        num_pixels = len(pixels)

        # Calcule la moyenne des composantes rouge, verte et bleue
        avg_red = sum(p[0] for p in pixels) / num_pixels
        avg_green = sum(p[1] for p in pixels) / num_pixels
        avg_blue = sum(p[2] for p in pixels) / num_pixels

        # Calcule la taille du fichier image en kilooctets
        size_kb = os.path.getsize(image_path) / 1024

        # Retourne un dictionnaire contenant toutes les caractéristiques extraites
        return {
            'width': width,
            'height': height,
            'file_size_kb': size_kb,
            'avg_red': avg_red,
            'avg_green': avg_green,
            'avg_blue': avg_blue
        }