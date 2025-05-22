import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    APP_DIR = os.path.join(ROOT_DIR, "app")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(APP_DIR, 'data', 'history.db')}"
    app.config['BASE_DIR'] = ROOT_DIR
    app.config['GENERATED_FOLDER'] = os.path.join(APP_DIR, 'generated_bots')
    app.config['UPLOAD_FOLDER'] = os.path.join(APP_DIR, 'uploaded_files')
    app.config['INDEX_FOLDER'] = os.path.join(APP_DIR, 'index_storage')


    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['INDEX_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(APP_DIR, 'data'), exist_ok=True)

    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
