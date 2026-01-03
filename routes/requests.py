"""
Join request routes (submit, view, approve/reject).
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.join_request import JoinRequest
from models.pg_listing import PGListing
from models.user import User
from utils.decorators import login_required, pg_owner_required
import logging

logger = logging.getLogger(__name__)

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.route('/submit/<pg_id>', methods=['GET', 'POST'])
@login_required
def submit(pg_id):
    """Submit a join request for a PG"""
    user_role = session.get('user_role', 'student')
    if user_role != 'student':
        flash('Only students can submit join requests.', 'danger')
        return redirect(url_for('pg.view', pg_id=pg_id))
    
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('pg.search'))
    
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        student_id = session['user_id']
        
        try:
            JoinRequest.create(student_id, pg_id, message)
            flash('Join request submitted successfully! The PG owner will review your request.', 'success')
            return redirect(url_for('requests.my_requests'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            logger.error(f"Error submitting join request: {e}")
            flash('An error occurred. Please try again.', 'danger')
    
    # Convert ObjectId to string
    pg['_id'] = str(pg['_id'])
    
    return render_template('requests/submit.html', pg=pg)


@requests_bp.route('/my-requests', methods=['GET'])
@login_required
def my_requests():
    """View all join requests by the current student"""
    user_role = session.get('user_role', 'student')
    if user_role != 'student':
        flash('Only students can view join requests.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    student_id = session['user_id']
    requests = JoinRequest.find_by_student(student_id)
    
    # Convert ObjectId to string and get PG details
    for req in requests:
        req['_id'] = str(req['_id'])
        req['student_id'] = str(req['student_id'])
        req['pg_id'] = str(req['pg_id'])
        req['pg_owner_id'] = str(req['pg_owner_id'])
        
        # Get PG details
        pg = PGListing.find_by_id(req['pg_id'])
        if pg:
            pg['_id'] = str(pg['_id'])
            req['pg_details'] = pg
    
    return render_template('requests/my_requests.html', requests=requests)


@requests_bp.route('/received', methods=['GET'])
@login_required
@pg_owner_required
def received():
    """View all join requests received by PG owner"""
    owner_id = session['user_id']
    requests = JoinRequest.find_by_pg_owner(owner_id)
    
    # Convert ObjectId to string and get details
    for req in requests:
        req['_id'] = str(req['_id'])
        req['student_id'] = str(req['student_id'])
        req['pg_id'] = str(req['pg_id'])
        req['pg_owner_id'] = str(req['pg_owner_id'])
        
        # Get PG and student details
        pg = PGListing.find_by_id(req['pg_id'])
        student = User.find_by_id(req['student_id'])
        
        if pg:
            pg['_id'] = str(pg['_id'])
            req['pg_details'] = pg
        if student:
            student['_id'] = str(student['_id'])
            req['student_details'] = student
    
    return render_template('requests/received.html', requests=requests)


@requests_bp.route('/<request_id>/approve', methods=['POST'])
@login_required
@pg_owner_required
def approve(request_id):
    """Approve a join request"""
    req = JoinRequest.find_by_id(request_id)
    if not req:
        flash('Join request not found.', 'danger')
        return redirect(url_for('requests.received'))
    
    # Check ownership
    if str(req['pg_owner_id']) != session['user_id']:
        flash('You do not have permission to approve this request.', 'danger')
        return redirect(url_for('requests.received'))
    
    message = request.form.get('message', '').strip()
    
    try:
        JoinRequest.approve(request_id, message if message else None)
        flash('Join request approved successfully!', 'success')
    except Exception as e:
        logger.error(f"Error approving join request: {e}")
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('requests.received'))


@requests_bp.route('/<request_id>/reject', methods=['POST'])
@login_required
@pg_owner_required
def reject(request_id):
    """Reject a join request"""
    req = JoinRequest.find_by_id(request_id)
    if not req:
        flash('Join request not found.', 'danger')
        return redirect(url_for('requests.received'))
    
    # Check ownership
    if str(req['pg_owner_id']) != session['user_id']:
        flash('You do not have permission to reject this request.', 'danger')
        return redirect(url_for('requests.received'))
    
    message = request.form.get('message', '').strip()
    
    try:
        JoinRequest.reject(request_id, message if message else None)
        flash('Join request rejected.', 'info')
    except Exception as e:
        logger.error(f"Error rejecting join request: {e}")
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('requests.received'))


