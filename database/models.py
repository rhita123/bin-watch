
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    annotation = db.Column(db.String(50), nullable=True)
    annotation_auto = db.Column(db.String(50), nullable=True)  # ← ajout ici
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    file_size_kb = db.Column(db.Float, nullable=True)
    avg_red = db.Column(db.Float, nullable=True)
    avg_green = db.Column(db.Float, nullable=True)
    avg_blue = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)