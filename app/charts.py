import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Pour Mac / backend non-interactif
from io import BytesIO
import base64
from database.models import Image
import pandas as pd

 # Génère un diagramme circulaire de la répartition des annotations (pleine, vide, non annotée)
def generate_annotation_pie_chart():
    pleines = Image.query.filter_by(annotation='pleine').count()
    vides = Image.query.filter_by(annotation='vide').count()
    non_annotees = Image.query.filter_by(annotation=None).count()

    total = pleines + vides + non_annotees
    if total == 0:
        return None

    labels, sizes, colors = [], [], []
    if pleines > 0:
        labels.append('Pleine')
        sizes.append(pleines)
        colors.append('#dc3545')
    if vides > 0:
        labels.append('Vide')
        sizes.append(vides)
        colors.append('#198754')
    if non_annotees > 0:
        labels.append('Non annotée')
        sizes.append(non_annotees)
        colors.append('#6c757d')

    # Préparation des données pour le graphique circulaire
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title("Répartition des annotations")

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return image_base64

 # Génère un boxplot des tailles de fichiers image (en kilooctets)
def generate_file_size_boxplot():
    images = Image.query.filter(Image.file_size_kb != None).all()
    file_sizes = [img.file_size_kb for img in images]
    if not file_sizes:
        return None

    # Création du boxplot à partir des tailles de fichiers
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(file_sizes, vert=False)
    ax.set_title("Distribution des tailles de fichiers (en KB)")
    ax.set_xlabel("Taille (KB)")

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return image_base64

 # Génère une courbe cumulative du nombre d’images uploadées dans le temps
def generate_cumulative_curve():
    images = Image.query.filter(Image.date_uploaded != None).all()
    if not images:
        return None

    # Création DataFrame
    dates = [img.date_uploaded.date() for img in images]
    df = pd.DataFrame({'date': dates})
    df_count = df.groupby('date').size().cumsum()

    # Génération de la courbe cumulative à partir des dates d'upload
    fig, ax = plt.subplots(figsize=(8, 4))
    df_count.plot(ax=ax)
    ax.set_title("Courbe cumulative des images dans le temps")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre cumulé d’images")
    ax.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return image_base64