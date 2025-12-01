from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from .extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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
