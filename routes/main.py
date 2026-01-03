"""
Main application routes (home, dashboard).
"""
from flask import Blueprint, render_template, session, redirect, url_for
from utils.decorators import login_required
from models.pg_listing import PGListing
from models.join_request import JoinRequest
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)


def home():
    """Home page route"""
    user_logged_in = 'user_id' in session
    user_name = session.get('user_name', '')
    user_role = session.get('user_role', 'student')
    
    # Get featured/approved PGs for homepage
    featured_pgs = PGListing.find_approved()[:6]  # Show first 6 approved PGs
    for pg in featured_pgs:
        pg['_id'] = str(pg['_id'])
        pg['owner_id'] = str(pg['owner_id'])
    
    return render_template('index.html', 
                         user_logged_in=user_logged_in, 
                         user_name=user_name,
                         user_role=user_role,
                         featured_pgs=featured_pgs)


@login_required
def dashboard():
    """User dashboard route"""
    user_name = session.get('user_name', 'User')
    user_email = session.get('user_email', '')
    user_role = session.get('user_role', 'student')
    user_id = session.get('user_id')
    
    # Role-specific data
    requests = None
    listings = None
    received_requests = None
    
    if user_role == 'student':
        # Get student's join requests
        requests = JoinRequest.find_by_student(user_id)
        for req in requests:
            req['_id'] = str(req['_id'])
            req['pg_id'] = str(req['pg_id'])
            pg = PGListing.find_by_id(req['pg_id'])
            if pg:
                pg['_id'] = str(pg['_id'])
                req['pg_details'] = pg
    elif user_role == 'pg_owner':
        # Get PG owner's listings
        listings = PGListing.find_by_owner(user_id)
        for listing in listings:
            listing['_id'] = str(listing['_id'])
        
        # Get received requests
        received_requests = JoinRequest.find_by_pg_owner(user_id)
        for req in received_requests:
            req['_id'] = str(req['_id'])
            req['pg_id'] = str(req['pg_id'])
    elif user_role == 'admin':
        # Redirect to admin dashboard
        return redirect(url_for('admin.dashboard'))
    
    return render_template('dashboard.html', 
                         name=user_name, 
                         email=user_email,
                         user_role=user_role,
                         requests=requests,
                         listings=listings,
                         received_requests=received_requests)


# Register routes
main_bp.add_url_rule('/', 'home', home, methods=['GET'])
main_bp.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET'])
