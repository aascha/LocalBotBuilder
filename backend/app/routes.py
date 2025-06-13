import os
import zipfile
from datetime import datetime
import requests
from flask import Blueprint, request, send_from_directory, current_app, jsonify, send_file, session
from sqlalchemy.exc import IntegrityError
from . import db
from .models import BotHistory, User
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

bp = Blueprint('main', __name__)

# ──────────────── Tone templates ────────────────
TONE_TEMPLATES = {
    "Einfache Antworten": "Respond using short, clear, and simple language that is easy for anyone to understand.",
    "Lustig": "Add humor and light-heartedness to your answers while still being informative.",
    "Motivierend": "Respond in an uplifting and encouraging way. Use a positive and inspirational tone.",
    "Detailliert": "Give thorough, step-by-step answers with as much detail as necessary for full understanding.",
    "Versichernd": "Be calm and reassuring. Make the user feel supported and understood in all situations.",
    "Freundlich": "Always use a warm and friendly tone. Make the user feel welcomed and appreciated.",
    "Professionell": "Use a formal, concise, and professional tone. Keep responses clear and business-like.",
    "Nachvollziehbar": "Break down complex ideas clearly and logically. Make it easy for the user to follow.",
    "Verständig": "Use everyday language and relatable examples to make your answers easy to grasp.",
}

# ──────────────── Static frontend ────────────────
@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def serve_vue_app(path):
    static_dir = os.path.join(current_app.config['BASE_DIR'], 'static')
    file_path = os.path.join(static_dir, path)
    return send_from_directory(static_dir, path if os.path.exists(file_path) else "index.html")

# ──────────────── Authentication ────────────────
@bp.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    if not all([data.get('name'), data.get('email'), data.get('password')]):
        return jsonify({'error': 'Please fill out all fields.'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists.'}), 400

    new_user = User(fullname=data['name'], email=data['email'])
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Registration failed.'}), 500

@bp.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

@bp.route('/api/logout', methods=['POST'])
def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

@bp.route('/api/me')
def current_user():
    user = User.query.get(session.get('user_id'))
    if not user:
        return jsonify({'user': None}), 200
    return jsonify({'user': {'id': user.id, 'name': user.fullname, 'email': user.email}})

# ──────────────── Bot Creation ────────────────
@bp.route('/api/create', methods=['POST'])
def create_bot():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        form = request.form
        file = request.files.get('file')

        bot_name = form['bot_name']
        model_name = form['model_name']
        temperature = form['temperature']  # Do we need this or no
        context_window = form['context_window']  # Do we need this or no
        system_prompt = " ".join(form['system_prompt'].split())
        tone_prompt = TONE_TEMPLATES.get(form['tone'], "")
        full_prompt = f"{tone_prompt} {system_prompt}".strip()

        # Create modelfile
        filename = f"{bot_name.replace(' ', '_')}_modelfile.txt"  # how should this be
        filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)
        with open(filepath, "w", newline='\n') as f:
            f.write("\n".join([
                f"FROM {model_name}",
                f'SYSTEM "{full_prompt}"',
                f"PARAMETER temperature {temperature}",  # Do we need this or no
                f"PARAMETER num_ctx {context_window}",  # Do we need this or no
            ]) + "\n")

        uploaded_filename = None
        index_dir = None

        # Index file (Should this be in the builder)  REMOVE THIS
        if file and file.filename:
            temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], f"temp_{bot_name.replace(' ', '_')}")
            os.makedirs(temp_dir, exist_ok=True)
            uploaded_path = os.path.join(temp_dir, file.filename)
            file.save(uploaded_path)

            reader = SimpleDirectoryReader(input_dir=temp_dir)
            documents = reader.load_data()
            llm = Ollama(model=model_name, base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434"))
            embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            index = VectorStoreIndex.from_documents(documents, llm=llm, embed_model=embed_model)

            index_dir = os.path.join(current_app.config['INDEX_FOLDER'], bot_name.replace(" ", "_"))
            os.makedirs(index_dir, exist_ok=True)
            index.storage_context.persist(persist_dir=index_dir)

            uploaded_filename = file.filename

        # Store bot history
        bot = BotHistory(
            bot_name=bot_name,
            model_name=model_name,
            system_prompt=full_prompt,
            temperature=temperature,   # Do we need this or no
            context_window=context_window,   # Do we need this or no
            filename=filename,
            indexed_file=uploaded_filename,
            tone=form['tone'],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Do we need this or no
            user_id=user_id
        )
        db.session.add(bot)
        db.session.commit()

        # Package as ZIP  (Which files should we zip)
        zip_path = os.path.join(current_app.config['GENERATED_FOLDER'], f"{bot_name.replace(' ', '_')}_package.zip")
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.write(filepath, arcname=filename)
            if index_dir:
                for root, _, files in os.walk(index_dir):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, index_dir)
                        z.write(full_path, arcname=os.path.join('index', rel_path))

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        print("ERROR during bot creation:", e)
        return "Failed to create bot", 500

# ──────────────── Other Routes ────────────────
@bp.route('/api/build', methods=['POST'])   #  Should this be in the builder  REMOVE THIS
def build_model():
    try:
        filename = request.form['filename']
        model_name = filename.replace("_modelfile.txt", "")
        filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)

        with open(filepath, "r") as f:
            modelfile_content = f.read()

        response = requests.post("http://ollama:11434/api/create", json={
            "name": model_name,
            "modelfile": modelfile_content
        })

        if response.ok:
            return f"<h1>Model '{model_name}' created successfully!</h1><pre>{response.text}</pre><a href='/'>Back</a>"
        return f"<h1>Failed to create model '{model_name}'</h1><pre>{response.text}</pre><a href='/'>Try Again</a>"
    except Exception as e:
        return f"<h1>Unexpected Error</h1><pre>{str(e)}</pre><a href='/'>Back</a>"

@bp.route('/api/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    bots = BotHistory.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "bot_name": b.bot_name,
        "model_name": b.model_name,
        "tone": b.tone,    # Do we need this or no
        "system_prompt": b.system_prompt   # Do we need this or no
    } for b in bots])

@bp.route('/api/download/<bot_name>')
def download_bot(bot_name):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    safe_name = bot_name.replace(" ", "_")
    zip_path = os.path.join(current_app.config['GENERATED_FOLDER'], f"{safe_name}_package.zip")

    if not os.path.exists(zip_path):
        return jsonify({'error': 'Datei nicht gefunden'}), 404

    return send_file(zip_path, as_attachment=True)
