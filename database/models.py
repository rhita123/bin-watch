
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Modèle représentant une image uploadée dans la base de données
class Image(db.Model):
    # Identifiants et informations de base sur l'image
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Annotations manuelle et automatique (pleine, vide, etc.)
    annotation = db.Column(db.String(50), nullable=True)
    annotation_auto = db.Column(db.String(50), nullable=True)  # ← ajout ici

    # Caractéristiques visuelles extraites de l'image
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    file_size_kb = db.Column(db.Float, nullable=True)
    avg_red = db.Column(db.Float, nullable=True)
    avg_green = db.Column(db.Float, nullable=True)
    avg_blue = db.Column(db.Float, nullable=True)

    # Coordonnées GPS associées à l'image
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)