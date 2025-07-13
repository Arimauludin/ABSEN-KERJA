from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

# Import db dan login_manager dari extensions.py
from extensions import db, login_manager, init_extensions

app = Flask(__name__)
app.config.from_object('config.Config')

# Inisialisasi ekstensi dengan objek 'app'
init_extensions(app)

# PENTING: Sekarang baru import models dan routes
# setelah db dan login_manager telah diinisialisasi sepenuhnya oleh init_extensions(app).
from models import User, Attendance, load_user # load_user tetap dari models.py
from routes import * # Mengimport semua route dari routes.py

# Pastikan tabel database dibuat sebelum aplikasi berjalan
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)