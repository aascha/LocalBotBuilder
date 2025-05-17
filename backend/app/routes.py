import os
from datetime import datetime
import requests

from flask import Blueprint, request, send_from_directory, current_app, render_template
from . import db
from .models import BotHistory

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

bp = Blueprint('main', __name__)

TONE_TEMPLATES = {
    "Einfache Antworten": "Respond using short, clear, and simple language that is easy for anyone to understand.",
    "Lustig": "Add humor and light-heartedness to your answers while still being informative.",
    "Motivierend": "Respond in an uplifting and encouraging way. Use a positive and inspirational tone.",
    "Detailliert": "Give thorough, step-by-step answers with as much detail as necessary for full understanding.",
    "Versichernd": "Be calm and reassuring. Make the user feel supported and understood in all situations.",
    "Freundlich": "Always use a warm and friendly tone. Make the user feel welcomed and appreciated.",
    "Professionell": "Use a formal, concise, and professional tone. Keep responses clear and business-like.",
    "Nachvollziehbar": "Break down complex ideas clearly and logically. Make it easy for the user to follow.",
    "Verständig": "Use everyday language and relatable examples to make your answers easy to grasp."
}

@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def serve_vue_app(path):
    static_dir = os.path.join(current_app.config['BASE_DIR'], 'static')
    if path != "" and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    else:
        return send_from_directory(static_dir, "index.html")


@bp.route('/api/create', methods=['POST'])
def create():
    try:
        data = request.form
        file = request.files.get('file')

        bot_name = data['bot_name']
        model_name = data['model_name']
        temperature = data['temperature']
        context_window = data['context_window']
        system_prompt = data['system_prompt']
        tone = data['tone']

        cleaned_prompt = " ".join(system_prompt.split())
        tone_prompt = TONE_TEMPLATES.get(tone, "")
        full_prompt = f"{tone_prompt} {cleaned_prompt}".strip()

        lines = [
            f"FROM {model_name}",
            f'SYSTEM "{full_prompt}"',
            f"PARAMETER temperature {temperature}",
            f"PARAMETER num_ctx {context_window}",
        ]

        filename = f"{bot_name.replace(' ', '_')}_modelfile.txt"
        filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)

        with open(filepath, "w", newline='\n') as f:
            f.write("\n".join(lines).strip() + "\n")

        uploaded_filename = None
        if file and file.filename:
            # ✅ Create a temp folder just for this file
            temp_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f"temp_{bot_name.replace(' ', '_')}")
            os.makedirs(temp_folder, exist_ok=True)

            # ✅ Save file there
            uploaded_path = os.path.join(temp_folder, file.filename)
            file.save(uploaded_path)

            # ✅ Index that file only
            reader = SimpleDirectoryReader(input_dir=temp_folder)
            documents = reader.load_data()
            print("📄 DOCUMENTS:", documents)


            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
            llm = Ollama(model=model_name, base_url=ollama_url)
            embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url=ollama_url)

            index = VectorStoreIndex.from_documents(documents, llm=llm, embed_model=embed_model)

            bot_index_folder = os.path.join(current_app.config['INDEX_FOLDER'], bot_name.replace(" ", "_"))
            os.makedirs(bot_index_folder, exist_ok=True)
            index.storage_context.persist(persist_dir=bot_index_folder)

            uploaded_filename = file.filename

        # ✅ Save metadata to DB
        bot = BotHistory(
            bot_name=bot_name,
            model_name=model_name,
            system_prompt=full_prompt,
            temperature=temperature,
            context_window=context_window,
            filename=filename,
            indexed_file=uploaded_filename,
            tone=tone,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(bot)
        db.session.commit()

        print("✅ BOT SAVED TO DB:", bot.bot_name)
        return f"✅ Bot '{bot_name}' created successfully!"

    except Exception as e:
        print("❌ ERROR during bot creation:", e)
        return "❌ Failed to create bot", 500



@bp.route('/api/build', methods=['POST'])
def build_model():
    filename = request.form['filename']
    model_name = filename.replace("_modelfile.txt", "")
    filepath = os.path.join(current_app.config['GENERATED_FOLDER'], filename)

    try:
        with open(filepath, "r") as f:
            modelfile_content = f.read()

        response = requests.post("http://ollama:11434/api/create", json={
            "name": model_name,
            "modelfile": modelfile_content
        })

        if response.status_code == 200:
            return f"<h1>✅ Model '{model_name}' created successfully!</h1><pre>{response.text}</pre><a href='/'>Back</a>"
        else:
            return f"<h1>❌ Failed to create model '{model_name}'</h1><pre>{response.text}</pre><a href='/'>Try Again</a>"

    except Exception as e:
        return f"<h1>❌ Unexpected Error</h1><pre>{str(e)}</pre><a href='/'>Back</a>"

@bp.route('/api/history')
def history():
    bots = BotHistory.query.all()
    return render_template('history.html', bots=bots)
