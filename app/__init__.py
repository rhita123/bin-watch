from flask import Flask
import os
from database.models import db  
from flask_migrate import Migrate
from flask_babel import Babel, get_locale

def create_app():
    app = Flask(__name__)

    from flask_babel import get_locale

    @app.context_processor
    def inject_locale():
        return dict(get_locale=get_locale)

    app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
    babel = Babel(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'database', 'images.db')

    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from flask import session

    @babel.localeselector
    def get_locale():
        return session.get('lang', 'fr')

    return app