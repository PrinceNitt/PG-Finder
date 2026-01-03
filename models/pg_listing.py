"""
PG Listing model for database operations.
"""
from datetime import datetime
from models.database import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class PGListing:
    """PG Listing model class"""
    
    @staticmethod
    def create(owner_id, name, address, city, state, pincode, rent, deposit, 
               available_rooms, total_rooms, facilities, description, 
               contact_phone, contact_email, nearby_colleges=None, nearby_workplaces=None,
               latitude=None, longitude=None):
        """
        Create a new PG listing.
        
        Args:
            owner_id: ID of the PG owner
            name: Name of the PG
            address: Full address
            city: City name
            state: State name
            pincode: Pincode
            rent: Monthly rent
            deposit: Security deposit
            available_rooms: Number of available rooms
            total_rooms: Total number of rooms
            facilities: List of facilities (e.g., ['WiFi', 'AC', 'Food'])
            description: Description of the PG
            contact_phone: Contact phone number
            contact_email: Contact email
            nearby_colleges: List of nearby colleges
            nearby_workplaces: List of nearby workplaces
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            PG listing document if created successfully
            
        Raises:
            ValueError: If validation fails
        """
        pg_collection = get_collection('pg_listings')
        
        # Validate required fields
        if not name or not name.strip():
            raise ValueError("PG name is required")
        if not address or not address.strip():
            raise ValueError("Address is required")
        if not city or not city.strip():
            raise ValueError("City is required")
        if rent is None or rent <= 0:
            raise ValueError("Valid rent amount is required")
        if available_rooms is None or available_rooms < 0:
            raise ValueError("Available rooms must be a non-negative number")
        if total_rooms is None or total_rooms <= 0:
            raise ValueError("Total rooms must be greater than 0")
        if available_rooms > total_rooms:
            raise ValueError("Available rooms cannot exceed total rooms")
        
        # Create PG listing document
        pg_data = {
            'owner_id': ObjectId(owner_id),
            'name': name.strip(),
            'address': address.strip(),
            'city': city.strip(),
            'state': state.strip() if state else '',
            'pincode': pincode.strip() if pincode else '',
            'rent': float(rent),
            'deposit': float(deposit) if deposit else 0,
            'available_rooms': int(available_rooms),
            'total_rooms': int(total_rooms),
            'facilities': facilities if isinstance(facilities, list) else [],
            'description': description.strip() if description else '',
            'contact_phone': contact_phone.strip() if contact_phone else '',
            'contact_email': contact_email.strip().lower() if contact_email else '',
            'nearby_colleges': nearby_colleges if isinstance(nearby_colleges, list) else [],
            'nearby_workplaces': nearby_workplaces if isinstance(nearby_workplaces, list) else [],
            'latitude': float(latitude) if latitude else None,
            'longitude': float(longitude) if longitude else None,
            'status': 'pending',  # pending, approved, rejected
            'is_verified': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = pg_collection.insert_one(pg_data)
            logger.info(f"PG listing created: {name} by owner {owner_id}")
            return pg_collection.find_one({'_id': result.inserted_id})
        except Exception as e:
            logger.error(f"Error creating PG listing: {e}")
            raise
    
    @staticmethod
    def find_by_id(pg_id):
        """Find PG listing by ID"""
        pg_collection = get_collection('pg_listings')
        try:
            return pg_collection.find_one({'_id': ObjectId(pg_id)})
        except Exception:
            return None
    
    @staticmethod
    def find_by_owner(owner_id):
        """Find all PG listings by owner ID"""
        pg_collection = get_collection('pg_listings')
        try:
            return list(pg_collection.find({'owner_id': ObjectId(owner_id)}))
        except Exception:
            return []
    
    @staticmethod
    def find_approved():
        """Find all approved PG listings"""
        pg_collection = get_collection('pg_listings')
        return list(pg_collection.find({'status': 'approved', 'available_rooms': {'$gt': 0}}))
    
    @staticmethod
    def search(city=None, max_rent=None, min_rent=None, facilities=None, 
               nearby_college=None, nearby_workplace=None):
        """
        Search PG listings with filters.
        
        Args:
            city: Filter by city
            max_rent: Maximum rent
            min_rent: Minimum rent
            facilities: List of required facilities
            nearby_college: Filter by nearby college
            nearby_workplace: Filter by nearby workplace
            
        Returns:
            List of matching PG listings
        """
        pg_collection = get_collection('pg_listings')
        query = {'status': 'approved', 'available_rooms': {'$gt': 0}}
        
        if city:
            query['city'] = {'$regex': city, '$options': 'i'}
        
        if max_rent is not None:
            query['rent'] = {'$lte': float(max_rent)}
        
        if min_rent is not None:
            if 'rent' in query and isinstance(query['rent'], dict):
                query['rent']['$gte'] = float(min_rent)
            else:
                query['rent'] = {'$gte': float(min_rent)}
        
        if facilities and isinstance(facilities, list):
            query['facilities'] = {'$all': facilities}
        
        if nearby_college:
            query['nearby_colleges'] = {'$regex': nearby_college, '$options': 'i'}
        
        if nearby_workplace:
            query['nearby_workplaces'] = {'$regex': nearby_workplace, '$options': 'i'}
        
        return list(pg_collection.find(query).sort('created_at', -1))
    
    @staticmethod
    def update(pg_id, **kwargs):
        """Update PG listing"""
        pg_collection = get_collection('pg_listings')
        
        # Remove None values and update timestamp
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        update_data['updated_at'] = datetime.utcnow()
        
        # If status is being changed, reset verification
        if 'status' in update_data and update_data['status'] != 'approved':
            update_data['is_verified'] = False
        
        try:
            result = pg_collection.update_one(
                {'_id': ObjectId(pg_id)},
                {'$set': update_data}
            )
            if result.modified_count > 0:
                logger.info(f"PG listing updated: {pg_id}")
                return pg_collection.find_one({'_id': ObjectId(pg_id)})
            return None
        except Exception as e:
            logger.error(f"Error updating PG listing: {e}")
            raise
    
    @staticmethod
    def delete(pg_id):
        """Delete PG listing"""
        pg_collection = get_collection('pg_listings')
        try:
            result = pg_collection.delete_one({'_id': ObjectId(pg_id)})
            logger.info(f"PG listing deleted: {pg_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting PG listing: {e}")
            raise
    
    @staticmethod
    def find_pending():
        """Find all pending PG listings for admin approval"""
        pg_collection = get_collection('pg_listings')
        return list(pg_collection.find({'status': 'pending'}).sort('created_at', -1))
    
    @staticmethod
    def approve(pg_id):
        """Approve a PG listing"""
        return PGListing.update(pg_id, status='approved', is_verified=True)
    
    @staticmethod
    def reject(pg_id, reason=None):
        """Reject a PG listing"""
        update_data = {'status': 'rejected'}
        if reason:
            update_data['rejection_reason'] = reason
        return PGListing.update(pg_id, **update_data)


