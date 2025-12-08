from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from .extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        confirm  = (request.form.get('confirm') or '').strip()

        if not username or not password or not confirm:
            flash('Completa todos los campos')
            return render_template('register.html')

        if password != confirm:
            flash('Las contraseñas no coinciden')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe')
            return render_template('register.html')

        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Error al registrar usuario')
            return render_template('register.html')

        flash('Usuario creado. Ahora inicia sesión.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('orders.menu'))
        flash('Usuario o contraseña inválidos')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ruta para crear usuario rápido (solo demo)
@auth_bp.route('/seed')
def seed_user():
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin')
        u.set_password('admin')
        db.session.add(u)
        db.session.commit()
    return 'ok'
