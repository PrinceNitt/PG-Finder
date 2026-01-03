"""
Decorators for route protection and utilities.
"""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Decorator to require user login for a route.
    
    Usage:
        @app.route('/dashboard')
        @login_required
        def dashboard():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Decorator to require user to be logged out (for login/signup pages).
    
    Usage:
        @app.route('/login')
        @logout_required
        def login():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            flash('You are already logged in.', 'info')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require specific user roles.
    
    Usage:
        @app.route('/admin')
        @role_required('admin')
        def admin_panel():
            ...
            
        @app.route('/pg/manage')
        @role_required('pg_owner', 'admin')
        def manage_pg():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            user_role = session.get('user_role', 'student')
            if user_role not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role"""
    return role_required('admin')(f)


def pg_owner_required(f):
    """Decorator to require PG owner role"""
    return role_required('pg_owner', 'admin')(f)

