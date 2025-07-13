# Import db dan login_manager dari extensions.py, BUKAN dari app.py
from extensions import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Dekorator ini memberi tahu Flask-Login bagaimana cara memuat pengguna dari ID pengguna.
@login_manager.user_loader
def load_user(user_id):
    """Memuat pengguna berdasarkan ID yang disimpan di sesi."""
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    attendances = db.relationship('Attendance', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False) # 'check_in' atau 'check_out'

    def __repr__(self):
        return f'<Attendance {self.user.username} - {self.status} at {self.timestamp}>'