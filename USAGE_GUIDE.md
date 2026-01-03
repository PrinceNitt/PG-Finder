# PG Assistant System - Usage Guide (हिंदी/English)

## 📋 Prerequisites (जरूरी चीजें)

1. **Python 3.8+** installed
2. **MongoDB** running (local ya MongoDB Atlas)
3. **Internet connection** (for Tailwind CSS CDN)

---

## 🚀 Step 1: Setup (सेटअप)

### 1.1 MongoDB Setup

**Option A: Local MongoDB**
```bash
# Check if MongoDB is running
mongosh
# या
mongo
```

**Option B: MongoDB Atlas (Cloud)**
- MongoDB Atlas account बनाएं
- Free cluster create करें
- Connection string copy करें

### 1.2 Install Dependencies

```bash
# Project folder में जाएं
cd /Users/princekumar/Downloads/pg

# Dependencies install करें
pip3 install -r requirements.txt
```

**Required packages:**
- Flask==3.0.0
- pymongo==4.6.0
- python-dotenv==1.0.0
- Werkzeug==3.0.1

### 1.3 Environment Configuration (Optional)

`.env` file create करें (optional):
```env
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=pgfinder_db
DEBUG=True
PORT=8000
HOST=127.0.0.1
```

**Note:** Agar `.env` file नहीं है, तो default values use होंगी।

---

## 🏃 Step 2: Run the Application (एप्लिकेशन चलाएं)

### Method 1: Using Python
```bash
python3 app.py
```

### Method 2: Using Run Script
```bash
chmod +x run.sh
./run.sh
```

### Success Message:
```
INFO:models.database:Successfully connected to MongoDB
INFO:__main__:Database connection established
 * Running on http://127.0.0.1:8000
```

---

## 🌐 Step 3: Access the Application

1. **Browser खोलें**
2. **URL enter करें:** `http://127.0.0.1:8000`
3. **Homepage** दिखेगा

---

## 👤 Step 4: Create Accounts (अकाउंट बनाएं)

### 4.1 Student Account

1. **Sign Up** पर click करें
2. **Role select करें:** "Student / Working Professional"
3. **Details fill करें:**
   - Name
   - Email
   - Password (minimum 8 characters, letter + number)
4. **Sign Up** button click करें

### 4.2 PG Owner Account

1. **Sign Up** पर click करें
2. **Role select करें:** "PG Owner"
3. **Details fill करें**
4. **Sign Up** button click करें

### 4.3 Admin Account

**Note:** Admin account manually database में set करना होगा:

```python
# Python script run करें
python3 -c "
from models.database import get_collection
users = get_collection('users')
users.update_one(
    {'email': 'your-email@example.com'},
    {'\$set': {'role': 'admin'}}
)
print('Admin role set successfully!')
"
```

**या sample data use करें:**
```bash
python3 insert_sample_data.py
```

**Sample Admin Account:**
- Email: `admin@example.com`
- Password: `admin123`

---

## 🎯 Step 5: Using as Different Roles

### 👨‍🎓 As a STUDENT

#### 5.1 Login
- Email: `student@example.com`
- Password: `student123`

#### 5.2 Search PGs
1. **"Search PGs"** menu पर click करें
2. **Filters use करें:**
   - City
   - Min/Max Rent
   - Facilities
   - Nearby Colleges/Workplaces
3. **Search** button click करें

#### 5.3 View PG Details
1. **PG card** पर click करें
2. **Complete details** देखें:
   - Rent, Deposit
   - Facilities
   - Available rooms
   - Contact info
   - Nearby locations

#### 5.4 Submit Join Request
1. **PG details page** पर जाएं
2. **"Submit Join Request"** button click करें
3. **Optional message** add करें
4. **Submit** करें

#### 5.5 Track Requests
1. **Dashboard** पर जाएं
2. **"My Requests"** section देखें
3. **Status check करें:**
   - Pending (yellow)
   - Approved (green)
   - Rejected (red)

---

### 🏠 As a PG OWNER

#### 5.1 Login
- Email: `pgowner1@example.com`
- Password: `owner123`

#### 5.2 Create PG Listing
1. **"Add PG"** या **"My Listings"** → **"+ Add New PG"**
2. **Form fill करें:**
   - PG Name
   - Address (City, State, Pincode)
   - Rent & Deposit
   - Total Rooms & Available Rooms
   - Facilities (checkboxes)
   - Description
   - Contact Info
   - Nearby Colleges/Workplaces
3. **"Submit for Review"** click करें
4. **Admin approval** का wait करें

#### 5.3 Manage Listings
1. **"My Listings"** पर जाएं
2. **Actions:**
   - **View** - Details देखें
   - **Edit** - Update करें
   - **Delete** - Remove करें

#### 5.4 Manage Join Requests
1. **"Requests"** menu पर click करें
2. **Received requests** देखें
3. **Actions:**
   - **Approve** - Student को accept करें
   - **Reject** - Request reject करें
   - **Response message** add करें (optional)

---

### 👨‍💼 As an ADMIN

#### 5.1 Login
- Email: `admin@example.com`
- Password: `admin123`

#### 5.2 Admin Dashboard
1. **"Admin"** menu पर click करें
2. **Statistics देखें:**
   - Total Listings
   - Pending Reviews
   - Approved/Rejected

#### 5.3 Review Pending Listings
1. **Pending listings** list देखें
2. **Actions:**
   - **View Details** - Complete info देखें
   - **Approve** - Listing publish करें
   - **Reject** - Reject करें (reason add करें)

#### 5.4 Manage All Listings
1. **"All Listings"** पर जाएं
2. **Filter by status:**
   - All
   - Pending
   - Approved
   - Rejected
3. **View/Manage** any listing

---

## 🔍 Common Features

### Search & Filter
- **City** - Location based search
- **Rent Range** - Budget filter
- **Facilities** - WiFi, AC, Food, etc.
- **Nearby** - Colleges/Workplaces

### PG Details Include
- ✅ Rent & Deposit
- ✅ Room Availability
- ✅ Facilities List
- ✅ Contact Information
- ✅ Nearby Locations
- ✅ Description

### Request Management
- ✅ Submit with message
- ✅ Track status
- ✅ Owner response
- ✅ Automatic room update on approval

---

## 🛠️ Troubleshooting (समस्याएं और समाधान)

### Problem: MongoDB Connection Error
**Solution:**
```bash
# Check MongoDB is running
mongosh

# या restart MongoDB
brew services restart mongodb-community
# (macOS)
```

### Problem: Port Already in Use
**Solution:**
```bash
# Different port use करें
export PORT=8001
python3 app.py
```

### Problem: Module Not Found
**Solution:**
```bash
# Dependencies install करें
pip3 install -r requirements.txt
```

### Problem: Login Not Working
**Solution:**
- Check email/password correct है
- Database में user exists है
- Try sample account: `student@example.com` / `student123`

### Problem: Templates Not Found
**Solution:**
- Check `templates/` folder exists
- All template files present हैं
- Flask app correct path use कर रहा है

---

## 📊 Sample Data

**Quick Start के लिए sample data insert करें:**
```bash
python3 insert_sample_data.py
```

**Sample Accounts:**
- **Student:** student@example.com / student123
- **PG Owner:** pgowner1@example.com / owner123
- **Admin:** admin@example.com / admin123

**Sample PGs:**
- Green Valley PG (Delhi) - ₹8,000/month
- Sunshine Hostel (Bangalore) - ₹12,000/month
- Comfort Zone PG (Mumbai) - ₹15,000/month
- And more...

---

## 🎯 Quick Start Checklist

- [ ] MongoDB running है
- [ ] Dependencies installed हैं
- [ ] Application started है (`python3 app.py`)
- [ ] Browser में `http://127.0.0.1:8000` open है
- [ ] Account create किया है (या sample data use किया है)
- [ ] Login successful है
- [ ] Features test किए हैं

---

## 📝 Important Notes

1. **First Time:** Sample data insert करें for testing
2. **Admin Role:** Manually set करना होगा
3. **PG Listings:** Admin approval के बाद ही visible होंगे
4. **Join Requests:** Owner approve/reject कर सकता है
5. **Room Availability:** Automatically update होता है

---

## 🎉 You're Ready!

अब आप PG Assistant System use कर सकते हैं!

**Next Steps:**
1. Application start करें
2. Account create करें
3. Features explore करें
4. Test करें!

**Happy Coding! 🚀**

