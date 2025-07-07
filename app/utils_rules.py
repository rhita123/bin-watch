from PIL import Image as PILImage
import os

# Extrait les caractéristiques visuelles de l'image : dimensions, couleur moyenne, taille du fichier
def extract_features(filepath):
    with PILImage.open(filepath) as img:
        width, height = img.size
        pixels = list(img.getdata())
        num_pixels = len(pixels)

        avg_red = sum(p[0] for p in pixels) / num_pixels
        avg_green = sum(p[1] for p in pixels) / num_pixels
        avg_blue = sum(p[2] for p in pixels) / num_pixels

        # Calcule la taille du fichier en kilooctets
    file_size_kb = os.path.getsize(filepath) / 1024

    return {
        'width': width,
        'height': height,
        'avg_red': avg_red,
        'avg_green': avg_green,
        'avg_blue': avg_blue,
        'file_size_kb': file_size_kb
    }

# Prédit l'état de la poubelle (pleine, vide ou indéterminé) en fonction de règles simples sur les couleurs et la taille
def rule_based_prediction(features):
    avg_red = features["avg_red"]
    avg_green = features["avg_green"]
    avg_blue = features["avg_blue"]
    file_size_kb = features["file_size_kb"]
    mean_rgb = (avg_red + avg_green + avg_blue) / 3

    # Debug
    print(f"[Règles] Rouge: {avg_red:.2f}, Vert: {avg_green:.2f}, Bleu: {avg_blue:.2f}, Moyenne: {mean_rgb:.2f}, Taille: {file_size_kb:.2f} KB")

    # Applique les règles conditionnelles pour déterminer l'état
    if mean_rgb < 130 and file_size_kb > 25:
        return "pleine"
    elif mean_rgb > 180 and file_size_kb > 100:
        return "vide"
    else:
        return "non déterminé"