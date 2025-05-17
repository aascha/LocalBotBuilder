import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'app', 'data', 'history.db')}"
    app.config['BASE_DIR'] = BASE_DIR
    app.config['GENERATED_FOLDER'] = os.path.join(BASE_DIR, 'app', 'generated_bots')
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'app', 'uploaded_files')
    app.config['INDEX_FOLDER'] = os.path.join(BASE_DIR, 'app', 'index_storage')



    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['INDEX_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
