from . import db

class BotHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(100))
    model_name = db.Column(db.String(50))
    system_prompt = db.Column(db.Text)
    temperature = db.Column(db.String(10))
    context_window = db.Column(db.String(10))
    filename = db.Column(db.String(100))
    indexed_file = db.Column(db.String(100))
    tone = db.Column(db.String(20))
    timestamp = db.Column(db.String(30))
