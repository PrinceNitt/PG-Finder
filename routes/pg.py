"""
PG listing routes (create, update, delete, search).
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.pg_listing import PGListing
from models.user import User
from utils.decorators import login_required, pg_owner_required
import logging

logger = logging.getLogger(__name__)

pg_bp = Blueprint('pg', __name__, url_prefix='/pg')


@pg_bp.route('/search', methods=['GET'])
def search():
    """Search PG listings"""
    city = request.args.get('city', '').strip()
    max_rent = request.args.get('max_rent', type=float)
    min_rent = request.args.get('min_rent', type=float)
    facilities = request.args.getlist('facilities')
    nearby_college = request.args.get('nearby_college', '').strip()
    nearby_workplace = request.args.get('nearby_workplace', '').strip()
    
    # Get all facilities for filter display
    all_pgs = PGListing.find_approved()
    all_facilities = set()
    for pg in all_pgs:
        all_facilities.update(pg.get('facilities', []))
    
    # Perform search
    results = PGListing.search(
        city=city if city else None,
        max_rent=max_rent,
        min_rent=min_rent,
        facilities=facilities if facilities else None,
        nearby_college=nearby_college if nearby_college else None,
        nearby_workplace=nearby_workplace if nearby_workplace else None
    )
    
    # Convert ObjectId to string for template rendering
    for pg in results:
        pg['_id'] = str(pg['_id'])
        pg['owner_id'] = str(pg['owner_id'])
    
    user_logged_in = 'user_id' in session
    user_role = session.get('user_role', 'student')
    
    return render_template('pg/search.html', 
                         pgs=results,
                         all_facilities=sorted(all_facilities),
                         search_params={
                             'city': city,
                             'max_rent': max_rent,
                             'min_rent': min_rent,
                             'facilities': facilities,
                             'nearby_college': nearby_college,
                             'nearby_workplace': nearby_workplace
                         },
                         user_logged_in=user_logged_in,
                         user_role=user_role)


@pg_bp.route('/<pg_id>', methods=['GET'])
def view(pg_id):
    """View a specific PG listing"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('pg.search'))
    
    # Convert ObjectId to string
    pg['_id'] = str(pg['_id'])
    pg['owner_id'] = str(pg['owner_id'])
    
    # Get owner info
    owner = User.find_by_id(pg['owner_id'])
    if owner:
        owner['_id'] = str(owner['_id'])
    
    user_logged_in = 'user_id' in session
    user_role = session.get('user_role', 'student')
    can_request = user_logged_in and user_role == 'student' and pg['status'] == 'approved' and pg['available_rooms'] > 0
    
    return render_template('pg/view.html', 
                         pg=pg, 
                         owner=owner,
                         user_logged_in=user_logged_in,
                         user_role=user_role,
                         can_request=can_request)


@pg_bp.route('/create', methods=['GET', 'POST'])
@login_required
@pg_owner_required
def create():
    """Create a new PG listing"""
    if request.method == 'POST':
        try:
            owner_id = session['user_id']
            name = request.form.get('name', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            pincode = request.form.get('pincode', '').strip()
            rent = request.form.get('rent', type=float)
            deposit = request.form.get('deposit', type=float) or 0
            available_rooms = request.form.get('available_rooms', type=int)
            total_rooms = request.form.get('total_rooms', type=int)
            facilities = request.form.getlist('facilities')
            description = request.form.get('description', '').strip()
            contact_phone = request.form.get('contact_phone', '').strip()
            contact_email = request.form.get('contact_email', '').strip()
            nearby_colleges = [c.strip() for c in request.form.get('nearby_colleges', '').split(',') if c.strip()]
            nearby_workplaces = [w.strip() for w in request.form.get('nearby_workplaces', '').split(',') if w.strip()]
            latitude = request.form.get('latitude', type=float)
            longitude = request.form.get('longitude', type=float)
            
            pg = PGListing.create(
                owner_id=owner_id,
                name=name,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                rent=rent,
                deposit=deposit,
                available_rooms=available_rooms,
                total_rooms=total_rooms,
                facilities=facilities,
                description=description,
                contact_phone=contact_phone,
                contact_email=contact_email,
                nearby_colleges=nearby_colleges,
                nearby_workplaces=nearby_workplaces,
                latitude=latitude,
                longitude=longitude
            )
            
            flash('PG listing created successfully! It will be reviewed by admin before being published.', 'success')
            return redirect(url_for('pg.my_listings'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            logger.error(f"Error creating PG listing: {e}")
            flash('An error occurred. Please try again.', 'danger')
    
    # Common facilities list
    common_facilities = [
        'WiFi', 'AC', 'Food', 'Laundry', 'Power Backup', 'Security', 
        'Parking', 'Gym', 'TV', 'Refrigerator', 'Washing Machine', 
        'Geyser', 'Housekeeping', 'Study Table', 'Cupboard'
    ]
    
    return render_template('pg/create.html', common_facilities=common_facilities)


@pg_bp.route('/my-listings', methods=['GET'])
@login_required
@pg_owner_required
def my_listings():
    """View all PG listings by the current owner"""
    owner_id = session['user_id']
    listings = PGListing.find_by_owner(owner_id)
    
    # Convert ObjectId to string
    for listing in listings:
        listing['_id'] = str(listing['_id'])
        listing['owner_id'] = str(listing['owner_id'])
    
    return render_template('pg/my_listings.html', listings=listings)


@pg_bp.route('/<pg_id>/edit', methods=['GET', 'POST'])
@login_required
@pg_owner_required
def edit(pg_id):
    """Edit a PG listing"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('pg.my_listings'))
    
    # Check ownership
    if str(pg['owner_id']) != session['user_id']:
        flash('You do not have permission to edit this listing.', 'danger')
        return redirect(url_for('pg.my_listings'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            pincode = request.form.get('pincode', '').strip()
            rent = request.form.get('rent', type=float)
            deposit = request.form.get('deposit', type=float) or 0
            available_rooms = request.form.get('available_rooms', type=int)
            total_rooms = request.form.get('total_rooms', type=int)
            facilities = request.form.getlist('facilities')
            description = request.form.get('description', '').strip()
            contact_phone = request.form.get('contact_phone', '').strip()
            contact_email = request.form.get('contact_email', '').strip()
            nearby_colleges = [c.strip() for c in request.form.get('nearby_colleges', '').split(',') if c.strip()]
            nearby_workplaces = [w.strip() for w in request.form.get('nearby_workplaces', '').split(',') if w.strip()]
            latitude = request.form.get('latitude', type=float)
            longitude = request.form.get('longitude', type=float)
            
            PGListing.update(
                pg_id,
                name=name,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                rent=rent,
                deposit=deposit,
                available_rooms=available_rooms,
                total_rooms=total_rooms,
                facilities=facilities,
                description=description,
                contact_phone=contact_phone,
                contact_email=contact_email,
                nearby_colleges=nearby_colleges,
                nearby_workplaces=nearby_workplaces,
                latitude=latitude,
                longitude=longitude,
                status='pending'  # Reset to pending after edit
            )
            
            flash('PG listing updated successfully! It will be reviewed again by admin.', 'success')
            return redirect(url_for('pg.my_listings'))
        except Exception as e:
            logger.error(f"Error updating PG listing: {e}")
            flash('An error occurred. Please try again.', 'danger')
    
    # Convert ObjectId to string
    pg['_id'] = str(pg['_id'])
    pg['owner_id'] = str(pg['owner_id'])
    
    # Common facilities list
    common_facilities = [
        'WiFi', 'AC', 'Food', 'Laundry', 'Power Backup', 'Security', 
        'Parking', 'Gym', 'TV', 'Refrigerator', 'Washing Machine', 
        'Geyser', 'Housekeeping', 'Study Table', 'Cupboard'
    ]
    
    return render_template('pg/edit.html', pg=pg, common_facilities=common_facilities)


@pg_bp.route('/<pg_id>/delete', methods=['POST'])
@login_required
@pg_owner_required
def delete(pg_id):
    """Delete a PG listing"""
    pg = PGListing.find_by_id(pg_id)
    if not pg:
        flash('PG listing not found.', 'danger')
        return redirect(url_for('pg.my_listings'))
    
    # Check ownership
    if str(pg['owner_id']) != session['user_id']:
        flash('You do not have permission to delete this listing.', 'danger')
        return redirect(url_for('pg.my_listings'))
    
    try:
        PGListing.delete(pg_id)
        flash('PG listing deleted successfully.', 'success')
    except Exception as e:
        logger.error(f"Error deleting PG listing: {e}")
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('pg.my_listings'))


