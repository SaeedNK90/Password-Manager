from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import db, bcrypt
from .forms import RegisterForm, LoginForm, PasswordForm
from .models import User, PasswordEntry
from .utils import encrypt_password, decrypt_password

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("This email has already been registered.", "danger")
            return redirect(url_for('main.register'))
        if User.query.filter_by(username=form.username.data).first():
            flash("This username has already been used.", "danger")
            return redirect(url_for('main.register'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("The entry was successful!", "success")
            return redirect(url_for('main.dashboard'))
        flash("The email or password is incorrect.", "danger")
    return render_template('login.html', form=form)


@main.route('/dashboard')
@login_required
def dashboard():
    entries = PasswordEntry.query.filter_by(user_id=current_user.id).order_by(PasswordEntry.date_added.desc()).all()
    visible = []
    for e in entries:
        try:
            plain = decrypt_password(e.password_encrypted)
        except Exception:
            plain = "—"
        visible.append({
            "id": e.id,
            "website": e.website,
            "username": e.username,
            "password": plain,
            "date": e.date_added
        })
    return render_template('dashboard.html', passwords=visible)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_password():
    form = PasswordForm()
    if form.validate_on_submit():
        encrypted = encrypt_password(form.password.data)
        entry = PasswordEntry(website=form.website.data, username=form.username.data,
                              password_encrypted=encrypted, owner=current_user)
        db.session.add(entry)
        db.session.commit()
        flash("Password saved successfully.", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('add_password.html', form=form)


@main.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_password(entry_id):
    entry = PasswordEntry.query.get_or_404(entry_id)
    if entry.owner != current_user:
        flash("Access is not allowed.", "danger")
        return redirect(url_for('main.dashboard'))
    db.session.delete(entry)
    db.session.commit()
    flash("Password removed.", "info")
    return redirect(url_for('main.dashboard'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for('main.home'))
