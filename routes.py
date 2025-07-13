from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

# Import app dan db dari extensions.py atau langsung app dari flask jika Anda tidak perlu db secara langsung di sini
# Untuk menghindari circular import, kita akan impor app secara langsung dari flask.
# Jika routes butuh db, impor dari extensions juga.
from app import app # Import objek app dari app.py
from extensions import db # Impor db dari extensions.py

from models import User, Attendance # Model tetap diimpor dari models.py
from datetime import datetime

# ... (sisa kode routes Anda tetap sama) ...

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Nama pengguna dan password tidak boleh kosong!', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nama pengguna sudah ada. Silakan pilih nama lain.', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login berhasil!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Nama pengguna atau password salah.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        action = request.form.get('action')
        user = current_user

        last_attendance = Attendance.query.filter_by(user_id=user.id)\
                                        .order_by(Attendance.timestamp.desc())\
                                        .first()

        if action == 'check_in':
            if last_attendance and last_attendance.status == 'check_in' \
               and last_attendance.timestamp.date() == datetime.utcnow().date():
                flash(f'Anda sudah melakukan Check-in hari ini.', 'warning')
            else:
                new_attendance = Attendance(user_id=user.id, status='check_in')
                db.session.add(new_attendance)
                db.session.commit()
                flash(f'Berhasil Check-in pada {new_attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S")}.', 'success')
        elif action == 'check_out':
            if not last_attendance or last_attendance.status == 'check_out' \
               or last_attendance.timestamp.date() != datetime.utcnow().date():
                flash(f'Anda belum melakukan Check-in hari ini.', 'warning')
            else:
                new_attendance = Attendance(user_id=user.id, status='check_out')
                db.session.add(new_attendance)
                db.session.commit()
                flash(f'Berhasil Check-out pada {new_attendance.timestamp.strftime("%Y-%m-%d %H:%M:%S")}.', 'success')
        
        return redirect(url_for('dashboard'))
    
    last_attendance = Attendance.query.filter_by(user_id=current_user.id)\
                                    .order_by(Attendance.timestamp.desc())\
                                    .first()
    return render_template('dashboard.html', user=current_user, last_attendance=last_attendance)

@app.route('/history')
@login_required
def history():
    attendances = Attendance.query.filter_by(user_id=current_user.id)\
                                  .order_by(Attendance.timestamp.desc())\
                                  .limit(50).all()
    return render_template('history.html', attendances=attendances, user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)