from app import create_app
from database.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de données initialisée !")