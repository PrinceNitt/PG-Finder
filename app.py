"""
PGFinder - PG Finder and Management System
Main application entry point.
"""
import os
import logging
from flask import Flask, render_template
from config import config
from models.database import get_db, close_connection
from routes.auth import auth_bp, signup, login, logout
from routes.main import main_bp, home, dashboard
from routes.pg import pg_bp
from routes.requests import requests_bp
from routes.admin import admin_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory pattern.
    Creates and configures the Flask app.
    
    Args:
        config_name: Name of configuration to use (development, production, testing)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(pg_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(admin_bp)
    
    # Register backward compatibility routes (without /auth prefix)
    app.add_url_rule('/signup', 'signup', signup, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET'])
    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET'])
    
    # Initialize database connection
    try:
        get_db()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.teardown_appcontext
    def close_db(error):
        """Close database connection on app context teardown"""
        pass  # MongoDB connection is handled globally
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    try:
        port = app.config.get('PORT', 8000)
        host = app.config.get('HOST', '127.0.0.1')
        debug = app.config.get('DEBUG', False)
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Error running application: {e}")
    finally:
        close_connection()
