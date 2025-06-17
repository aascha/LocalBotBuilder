import os
import zipfile
from datetime import datetime
import requests
from flask import Blueprint, request, send_from_directory, current_app, jsonify, send_file, session
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename 
from . import db
from .models import BotHistory, User, SharedBot

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

    # Validate input
    if not all([data.get('name'), data.get('email'), data.get('password')]):
        return jsonify({'error': 'Please fill out all fields.'}), 400

    # Check for existing user
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists.'}), 400

    # Create new user
    new_user = User(
        fullname=data['name'],
        email=data['email'],
        questionnaire_completed=False  # ✅ ensure they go through questionnaire first
    )
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()

        # Log in the user by setting session
        session['user_id'] = new_user.id

        return jsonify({'message': 'User registered successfully'}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Registration failed due to database error.'}), 500


@bp.route('/api/complete_questionnaire', methods=['POST'])
def complete_questionnaire():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401


    user = User.query.get(user_id)
    user.questionnaire_completed = True
    db.session.commit()
    return jsonify({'message': 'Questionnaire completed'})

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
    return jsonify({
        'user': {
            'id': user.id,
            'name': user.fullname,
            'email': user.email,
            'questionnaire_completed': user.questionnaire_completed
        }
    })

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
        temperature = form['temperature']
        context_window = form['context_window']
        system_prompt = " ".join(form['system_prompt'].split())
        tone_prompt = TONE_TEMPLATES.get(form['tone'], "")
        full_prompt = f"{tone_prompt} {system_prompt}".strip()

        filename = f"{bot_name.replace(' ', '_')}_modelfile.txt"
        filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)
        with open(filepath, "w", newline='\n') as f:
            f.write("\n".join([
                f"FROM {model_name}",
                f'SYSTEM "{full_prompt}"',
                f"PARAMETER temperature {temperature}",
                f"PARAMETER num_ctx {context_window}",
            ]) + "\n")

        uploaded_filename = None
        uploaded_path = None

        if file and file.filename:
            folder_name = f"temp_{bot_name.replace(' ', '_')}"
            temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(temp_dir, exist_ok=True)

            safe_name = secure_filename(file.filename)  # ✅ secure filename
            uploaded_path = os.path.join(temp_dir, safe_name)
            file.save(uploaded_path)

            uploaded_filename = safe_name
            image_folder = folder_name
        else:
            image_folder = None

        bot = BotHistory(
            bot_name=bot_name,
            model_name=model_name,
            system_prompt=full_prompt,
            temperature=temperature,
            context_window=context_window,
            filename=filename,
            indexed_file=uploaded_filename,
            tone=form['tone'],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id=user_id,
            image_file=uploaded_filename,
            image_folder=image_folder
        )
        db.session.add(bot)
        db.session.commit()

        zip_path = os.path.join(current_app.config['GENERATED_FOLDER'], f"{bot_name.replace(' ', '_')}_package.zip")
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.write(filepath, arcname=filename)
            if uploaded_path:
                z.write(uploaded_path, arcname=uploaded_filename)

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        print("ERROR during bot creation:", e)
        return "Failed to create bot", 500

# ──────────────── Other Routes ────────────────
@bp.route('/api/update/<int:bot_id>', methods=['POST'])
def update_bot(bot_id):
    try:
        user_id = session.get('user_id')
        form = request.form
        file = request.files.get('file')

        bot = BotHistory.query.filter_by(id=bot_id, user_id=user_id).first()

        if not bot:
            # Shared bot — clone it
            shared_entry = SharedBot.query.filter_by(bot_id=bot_id, shared_with_user_id=user_id).first()
            if not shared_entry:
                return jsonify({'error': 'Unauthorized'}), 403

            source_bot = shared_entry.bot
            new_bot = BotHistory(
                bot_name=form['bot_name'],
                model_name=form['model_name'],
                temperature=form['temperature'],
                context_window=form['context_window'],
                tone=form['tone'],
                system_prompt=f"{TONE_TEMPLATES.get(form['tone'], '')} {' '.join(form['system_prompt'].split())}".strip(),
                user_id=user_id,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                image_file=source_bot.image_file,
                image_folder=source_bot.image_folder,
            )

            if file and file.filename:
                folder_name = f"temp_{new_bot.bot_name.replace(' ', '_')}"
                temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
                os.makedirs(temp_dir, exist_ok=True)

                safe_name = secure_filename(file.filename)
                uploaded_path = os.path.join(temp_dir, safe_name)
                file.save(uploaded_path)

                new_bot.image_file = safe_name
                new_bot.image_folder = folder_name

            db.session.add(new_bot)
            db.session.commit()
            return jsonify({'message': 'Bot copied & updated'})

        # Editing own bot
        bot.bot_name = form['bot_name']
        bot.model_name = form['model_name']
        bot.temperature = form['temperature']
        bot.context_window = form['context_window']
        bot.tone = form['tone']
        bot.system_prompt = f"{TONE_TEMPLATES.get(form['tone'], '')} {' '.join(form['system_prompt'].split())}".strip()

        if file and file.filename:
            folder_name = f"temp_{bot.bot_name.replace(' ', '_')}"
            temp_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
            os.makedirs(temp_dir, exist_ok=True)

            safe_name = secure_filename(file.filename)
            uploaded_path = os.path.join(temp_dir, safe_name)
            file.save(uploaded_path)

            bot.image_file = safe_name
            bot.image_folder = folder_name

        bot.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        # ✅ Generate model file and ZIP
        safe_name = bot.bot_name.replace(' ', '_')
        filename = f"{safe_name}_modelfile.txt"
        filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)

        with open(filepath, "w", newline='\n') as f:
            f.write("\n".join([
                f"FROM {bot.model_name}",
                f'SYSTEM "{bot.system_prompt}"',
                f"PARAMETER temperature {bot.temperature}",
                f"PARAMETER num_ctx {bot.context_window}",
            ]) + "\n")

        zip_path = os.path.join(current_app.config['GENERATED_FOLDER'], f"{safe_name}_package.zip")
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.write(filepath, arcname=filename)

            if bot.image_file and bot.image_folder:
                uploaded_path = os.path.join(current_app.config['UPLOAD_FOLDER'], bot.image_folder, bot.image_file)
                if os.path.exists(uploaded_path):
                    z.write(uploaded_path, arcname=bot.image_file)

        return jsonify({'message': 'Bot aktualisiert'})

    except Exception as e:
        print("Update Error:", e)
        return "Fehler beim Aktualisieren", 500


@bp.route('/api/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    owned = BotHistory.query.filter_by(user_id=user_id).all()

    shared = (
        db.session.query(BotHistory)
        .join(SharedBot, SharedBot.bot_id == BotHistory.id)
        .filter(SharedBot.shared_with_user_id == user_id)
        .all()
    )

    combined = owned + shared
    return jsonify([{
    "id": b.id,
    "bot_name": b.bot_name,
    "model_name": b.model_name,
    "system_prompt": b.system_prompt.replace(TONE_TEMPLATES.get(b.tone, ""), "").strip(),
    "tone": b.tone,
    "image_url": (
        f"/uploads/{b.image_folder}/{b.image_file}"
        if b.image_file and b.image_folder
        else "/src/assets/default-bot-icon.jpg"  # Your frontend public path
    ),
    "owner_id": b.user_id
} for b in combined])




@bp.route('/api/bot/<int:bot_id>')
def fetch_bot_by_id(bot_id):
    user_id = session.get('user_id')
    bot = BotHistory.query.filter_by(id=bot_id, user_id=user_id).first()
    if not bot:
        return jsonify({'error': 'Nicht gefunden'}), 404

    return jsonify({
        "id": bot.id,
        "bot_name": bot.bot_name,
        "model_name": bot.model_name,
        "system_prompt": bot.system_prompt.replace(TONE_TEMPLATES.get(bot.tone, ""), "").strip(),
        "tone": bot.tone,
        "image_file": bot.image_file,
        "image_folder": bot.image_folder,
        "temperature": bot.temperature,
        "context_window": bot.context_window
    })

@bp.route('/uploads/<path:subpath>/<filename>')
def uploaded_file(subpath, filename):
    folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subpath)
    full_path = os.path.join(folder, filename)
    print(f"Trying to serve: {full_path}")
    if not os.path.exists(full_path):
        print("File not found!")
        return "File not found", 404
    return send_from_directory(folder, filename)

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

@bp.route('/api/share/<int:bot_id>', methods=['POST'])
def share_bot(bot_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    emails = data.get('emails', [])

    bot = BotHistory.query.filter_by(id=bot_id, user_id=user_id).first()
    if not bot:
        return jsonify({'error': 'Bot not found'}), 404

    shared = []
    failed = []

    for email in emails:
        email_cleaned = email.strip().lower()
        user = User.query.filter(User.email.ilike(email_cleaned)).first()  # Case-insensitive match

        if not user:
            failed.append(email_cleaned)
            continue

        # Prevent duplicate sharing
        exists = SharedBot.query.filter_by(bot_id=bot.id, shared_with_user_id=user.id).first()
        if exists:
            continue

        new_share = SharedBot(bot_id=bot.id, shared_with_user_id=user.id)
        db.session.add(new_share)
        shared.append(email_cleaned)

    db.session.commit()

    return jsonify({
        'shared': list(set(shared)),  # Remove duplicates if any
        'not_found': list(set(failed))  # Remove duplicates if any
    })
