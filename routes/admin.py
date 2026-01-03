"""
Admin routes for verifying and approving PG listings.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.pg_listing import PGListing
from models.user import User
from utils.decorators import login_required, admin_required
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    from models.database import get_collection
    pg_collection = get_collection('pg_listings')
    
    total_listings = pg_collection.count_documents({})
    pending_listings = pg_collection.count_documents({'status': 'pending'})
    approved_listings = pg_collection.count_documents({'status': 'approved'})
    rejected_listings = pg_collection.count_documents({'status': 'rejected'})
    
    # Get pending listings
    pending = PGListing.find_pending()
    for pg in pending:
        pg['_id'] = str(pg['_id'])
        pg['owner_id'] = str(pg['owner_id'])
        
        # Get owner info
        owner = User.find_by_id(pg['owner_id'])
        if owner:
            owner['_id'] = str(owner['_id'])
            pg['owner_details'] = owner
    
    return render_template('admin/dashboard.html',
                         total_listings=total_listings,
                         pending_listings=pending_listings,
                         approved_listings=approved_listings,
                         rejected_listings=rejected_listings,
                         pending=pending)


@admin_bp.route('/listings', methods=['GET'])
@login_required
@admin_required
def listings():
    """View all PG listings"""
    status = request.args.get('status', 'all')
    
    from models.database import get_collection
    pg_collection = get_collection('pg_listings')
    
    query = {}
    if status != 'all':
        query['status'] = status
    
    all_listings = list(pg_collection.find(query).sort('created_at', -1))
    
    # Convert ObjectId to string and get owner details
    for pg in all_listings:
        pg['_id'] = str(pg['_id'])
        pg['owner_id'] = str(pg['owner_id'])
        
        owner = User.find_by_id(pg['owner_id'])
        if owner:
            owner['_id'] = str(owner['_id'])
            pg['owner_details'] = owner
    
    return render_template('admin/listings.html', listings=all_listings, status=status)


@admin_bp.route('/listings/<pg_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_listing(pg_id):
    """Approve a PG listing"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('admin.listings'))
    
    try:
        PGListing.approve(pg_id)
        flash('PG listing approved successfully!', 'success')
    except Exception as e:
        logger.error(f"Error approving PG listing: {e}")
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/listings/<pg_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_listing(pg_id):
    """Reject a PG listing"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('admin.listings'))
    
    reason = request.form.get('reason', '').strip()
    
    try:
        PGListing.reject(pg_id, reason if reason else None)
        flash('PG listing rejected.', 'info')
    except Exception as e:
        logger.error(f"Error rejecting PG listing: {e}")
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/listings/<pg_id>/view', methods=['GET'])
@login_required
@admin_required
def view_listing(pg_id):
    """View a specific PG listing for admin"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('admin.listings'))
    
    # Convert ObjectId to string
    pg['_id'] = str(pg['_id'])
    pg['owner_id'] = str(pg['owner_id'])
    
    # Get owner info
    owner = User.find_by_id(pg['owner_id'])
    if owner:
        owner['_id'] = str(owner['_id'])
    
    return render_template('admin/view_listing.html', pg=pg, owner=owner)


