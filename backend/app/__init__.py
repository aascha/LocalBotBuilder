import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
    CORS(app, supports_credentials=True)

    # Define directories
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    APP_DIR = os.path.join(ROOT_DIR, "app")
    DATA_DIR = os.path.join(APP_DIR, "data")
    GENERATED_DIR = os.path.join(APP_DIR, "generated_bots")
    UPLOAD_DIR = os.path.join(APP_DIR, "uploaded_files")
    INDEX_DIR = os.path.join(APP_DIR, "index_storage")

    # App config
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{os.path.join(DATA_DIR, 'history.db')}",
        'BASE_DIR': ROOT_DIR,
        'GENERATED_FOLDER': GENERATED_DIR,
        'UPLOAD_FOLDER': UPLOAD_DIR,
        'INDEX_FOLDER': INDEX_DIR,
    })

    # Ensure all necessary folders exist
    for folder in [DATA_DIR, GENERATED_DIR, UPLOAD_DIR, INDEX_DIR]:
        os.makedirs(folder, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
