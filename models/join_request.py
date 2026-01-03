"""
Join Request model for students to request PG accommodation.
"""
from datetime import datetime
from models.database import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class JoinRequest:
    """Join Request model class"""
    
    @staticmethod
    def create(student_id, pg_id, message=None):
        """
        Create a new join request.
        
        Args:
            student_id: ID of the student making the request
            pg_id: ID of the PG listing
            message: Optional message from student
            
        Returns:
            Join request document if created successfully
            
        Raises:
            ValueError: If validation fails
        """
        requests_collection = get_collection('join_requests')
        
        # Check if request already exists
        existing = requests_collection.find_one({
            'student_id': ObjectId(student_id),
            'pg_id': ObjectId(pg_id),
            'status': {'$in': ['pending', 'approved']}
        })
        if existing:
            raise ValueError("You have already submitted a request for this PG")
        
        # Validate PG exists and has availability
        from models.pg_listing import PGListing
        pg = PGListing.find_by_id(pg_id)
        if not pg:
            raise ValueError("PG listing not found")
        if pg['available_rooms'] <= 0:
            raise ValueError("No rooms available in this PG")
        
        # Create join request document
        request_data = {
            'student_id': ObjectId(student_id),
            'pg_id': ObjectId(pg_id),
            'pg_owner_id': pg['owner_id'],
            'message': message.strip() if message else '',
            'status': 'pending',  # pending, approved, rejected
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = requests_collection.insert_one(request_data)
            logger.info(f"Join request created: student {student_id} for PG {pg_id}")
            return requests_collection.find_one({'_id': result.inserted_id})
        except Exception as e:
            logger.error(f"Error creating join request: {e}")
            raise
    
    @staticmethod
    def find_by_id(request_id):
        """Find join request by ID"""
        requests_collection = get_collection('join_requests')
        try:
            return requests_collection.find_one({'_id': ObjectId(request_id)})
        except Exception:
            return None
    
    @staticmethod
    def find_by_student(student_id):
        """Find all join requests by student ID"""
        requests_collection = get_collection('join_requests')
        try:
            return list(requests_collection.find({'student_id': ObjectId(student_id)}).sort('created_at', -1))
        except Exception:
            return []
    
    @staticmethod
    def find_by_pg_owner(owner_id):
        """Find all join requests for PG owner"""
        requests_collection = get_collection('join_requests')
        try:
            return list(requests_collection.find({'pg_owner_id': ObjectId(owner_id)}).sort('created_at', -1))
        except Exception:
            return []
    
    @staticmethod
    def find_by_pg(pg_id):
        """Find all join requests for a specific PG"""
        requests_collection = get_collection('join_requests')
        try:
            return list(requests_collection.find({'pg_id': ObjectId(pg_id)}).sort('created_at', -1))
        except Exception:
            return []
    
    @staticmethod
    def update_status(request_id, status, message=None):
        """
        Update join request status.
        
        Args:
            request_id: ID of the join request
            status: New status (approved, rejected)
            message: Optional message
            
        Returns:
            Updated join request document
        """
        requests_collection = get_collection('join_requests')
        
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        
        if message:
            update_data['response_message'] = message
        
        try:
            result = requests_collection.update_one(
                {'_id': ObjectId(request_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                request = requests_collection.find_one({'_id': ObjectId(request_id)})
                
                # If approved, decrease available rooms
                if status == 'approved':
                    from models.pg_listing import PGListing
                    pg = PGListing.find_by_id(str(request['pg_id']))
                    if pg and pg['available_rooms'] > 0:
                        PGListing.update(str(request['pg_id']), 
                                       available_rooms=pg['available_rooms'] - 1)
                
                logger.info(f"Join request {request_id} status updated to {status}")
                return request
            return None
        except Exception as e:
            logger.error(f"Error updating join request status: {e}")
            raise
    
    @staticmethod
    def approve(request_id, message=None):
        """Approve a join request"""
        return JoinRequest.update_status(request_id, 'approved', message)
    
    @staticmethod
    def reject(request_id, message=None):
        """Reject a join request"""
        return JoinRequest.update_status(request_id, 'rejected', message)


