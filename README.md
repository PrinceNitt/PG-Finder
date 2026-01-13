# PG Assistant System

A comprehensive web-based platform for managing Paying Guest (PG) accommodations. The system connects students/working professionals with PG owners, providing a centralized solution for finding, listing, and managing PG accommodations.

## Features

### For Students/Working Professionals
- **Search & Filter PGs**: Search by city, rent range, facilities, and proximity to colleges/workplaces
- **View Detailed Listings**: See complete information including rent, facilities, availability, and contact details
- **Submit Join Requests**: Request accommodation directly from PG owners
- **Track Requests**: Monitor the status of your join requests (pending, approved, rejected)

### For PG Owners
- **List Your PG**: Create detailed listings with all necessary information
- **Manage Listings**: Update, edit, or delete your PG listings
- **Receive Requests**: View and manage join requests from students
- **Approve/Reject**: Respond to student requests with optional messages

### For Administrators
- **Verify Listings**: Review and approve/reject PG listings for authenticity
- **Dashboard**: View statistics and manage all listings
- **Quality Control**: Ensure only verified and reliable listings are published

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, Tailwind CSS, Jinja2 Templates
- **Authentication**: Session-based with role-based access control

## Installation

1. **Clone the repository**
```bash
cd pg
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
```env
   SECRET_KEY=your-secret-key-here
   MONGO_URI=mongodb://localhost:27017/
   DATABASE_NAME=pgfinder_db
DEBUG=True
   PORT=8000
HOST=127.0.0.1
   ```

4. **Start MongoDB**
   Make sure MongoDB is running on your system

5. **Run the application**
```bash
   python app.py
```

6. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## Deployment

### Deploy to Render (Recommended)

This project is configured for deployment on Render.

1.  **Push to GitHub**: Ensure your code is in a GitHub repository.
2.  **Sign up on Render**: Go to [render.com](https://render.com) and create an account.
3.  **New Web Service**:
    *   Click "New +" and select "Web Service".
    *   Connect your GitHub repository.
    *   Render will automatically detect the configuration from `render.yaml`.
    *   Add your environment variables (MONGO_URI, SECRET_KEY) in the Render dashboard.
4.  **Deploy**: Click "Create Web Service".

### Configuration Files
- `Procfile`: Used by Render/Heroku to start the app (`gunicorn app:app`).
- `render.yaml`: Infrastructure configuration for Render.


## User Roles

### Student
- Default role for new signups
- Can search and view PG listings
- Can submit join requests
- Can track their requests

### PG Owner
- Selected during signup
- Can create and manage PG listings
- Can view and respond to join requests
- Listings require admin approval before being published

### Admin
- Must be manually set in database (role: 'admin')
- Can approve/reject PG listings
- Has access to admin dashboard
- Can view all listings and statistics

## Project Structure

```
pg/
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── models/               # Database models
│   ├── user.py          # User model
│   ├── pg_listing.py    # PG listing model
│   └── join_request.py  # Join request model
├── routes/               # Route handlers
│   ├── auth.py          # Authentication routes
│   ├── main.py          # Main routes (home, dashboard)
│   ├── pg.py            # PG listing routes
│   ├── requests.py      # Join request routes
│   └── admin.py         # Admin routes
├── templates/            # Jinja2 templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── dashboard.html   # User dashboard
│   ├── pg/              # PG-related templates
│   ├── requests/        # Request-related templates
│   └── admin/           # Admin templates
└── utils/               # Utility functions
    ├── decorators.py    # Route decorators
    └── validators.py    # Input validation
```

## Key Features Implementation

### PG Listing Management
- PG owners can create listings with:
  - Basic information (name, address, city, state, pincode)
  - Pricing (rent, deposit)
  - Room availability
  - Facilities list
  - Nearby colleges and workplaces
  - Contact information
  - Optional location coordinates

### Search & Filter
- Search by city
- Filter by rent range (min/max)
- Filter by facilities
- Filter by nearby colleges/workplaces
- Results show only approved listings with available rooms

### Join Request System
- Students can submit requests with optional messages
- PG owners receive notifications of new requests
- Owners can approve/reject with optional response messages
- Automatic room availability update on approval

### Admin Verification
- All new listings start as "pending"
- Admin reviews and approves/rejects listings
- Only approved listings are visible in search results
- Rejected listings can include rejection reasons

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Input validation and sanitization
- CSRF protection (WTF-CSRF enabled)

## Usage Guide

### For Students
1. Sign up with role "Student / Working Professional"
2. Search for PGs using filters
3. View detailed PG information
4. Submit join requests for interested PGs
5. Track request status in dashboard

### For PG Owners
1. Sign up with role "PG Owner"
2. Create PG listings with all details
3. Wait for admin approval
4. View and respond to join requests
5. Manage your listings (edit/delete)

### For Administrators
1. Access admin dashboard
2. Review pending listings
3. Approve or reject listings
4. Monitor system statistics

## Future Enhancements

- Image uploads for PG listings
- Map integration for location visualization
- Email notifications
- Reviews and ratings system
- Payment integration
- Advanced search with distance calculation
- Mobile app support

## License

This project is developed for educational purposes.

## Support

For issues or questions, please refer to the project documentation or contact the development team.
