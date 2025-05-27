from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    bots = db.relationship('BotHistory', backref='owner', lazy=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
