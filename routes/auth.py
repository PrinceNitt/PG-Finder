"""
Authentication routes (login, signup, logout).
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from utils.validators import validate_email, validate_password, validate_name
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def signup():
    """User registration route"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'student').strip()
        
        # Validate inputs
        name_valid, name_error = validate_name(name)
        email_valid, email_error = validate_email(email)
        password_valid, password_error = validate_password(password)
        
        if not name_valid:
            flash(name_error, 'danger')
            return render_template('signup.html', name=name, email=email, role=role)
        
        if not email_valid:
            flash(email_error, 'danger')
            return render_template('signup.html', name=name, email=email, role=role)
        
        if not password_valid:
            flash(password_error, 'danger')
            return render_template('signup.html', name=name, email=email, role=role)
        
        # Validate role
        valid_roles = ['student', 'pg_owner']
        if role not in valid_roles:
            role = 'student'
        
        try:
            User.create(name, email, password, role)
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('signup.html', name=name, email=email, role=role)
        except Exception as e:
            logger.error(f"Signup error: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return render_template('signup.html', name=name, email=email, role=role)
    
    return render_template('signup.html')


def login():
    """User login route"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html', email=email)
        
        # Validate email format
        email_valid, email_error = validate_email(email)
        if not email_valid:
            flash(email_error, 'danger')
            return render_template('login.html', email=email)
        
        user = User.authenticate(email, password)
        if user:
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user.get('role', 'student')
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html', email=email)
    
    return render_template('login.html')


def logout():
    """User logout route"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# Register routes with blueprint (for /auth prefix)
auth_bp.add_url_rule('/signup', 'signup', signup, methods=['GET', 'POST'])
auth_bp.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', 'logout', logout, methods=['GET'])
