# 🚀 Quick Start Guide - PG Assistant System

## ⚡ 3 Simple Steps

### Step 1: Install Dependencies
```bash
cd /Users/princekumar/Downloads/pg
pip3 install -r requirements.txt
```

### Step 2: Insert Sample Data (Optional but Recommended)
```bash
python3 insert_sample_data.py
```

### Step 3: Run the Application
```bash
python3 app.py
```

**That's it!** Open `http://127.0.0.1:8000` in your browser.

---

## 🎯 Test Accounts (After running insert_sample_data.py)

### Student
- **Email:** `student@example.com`
- **Password:** `student123`
- **Can do:** Search PGs, Submit requests

### PG Owner
- **Email:** `pgowner1@example.com`
- **Password:** `owner123`
- **Can do:** Create listings, Manage requests

### Admin
- **Email:** `admin@example.com`
- **Password:** `admin123`
- **Can do:** Approve listings, View all data

---

## 📋 What You Can Do

### As Student:
1. Login → Search PGs → View Details → Submit Request
2. Dashboard → Track Your Requests

### As PG Owner:
1. Login → Add PG → Wait for Admin Approval
2. Dashboard → View Requests → Approve/Reject

### As Admin:
1. Login → Admin Dashboard → Review Pending Listings
2. Approve/Reject Listings

---

## ⚠️ Important Notes

1. **MongoDB must be running** (local or Atlas)
2. **First time?** Run `insert_sample_data.py` for test data
3. **Admin role** is set automatically in sample data
4. **PG listings** need admin approval before appearing in search

---

## 🆘 Troubleshooting

**MongoDB not running?**
```bash
# Check MongoDB
mongosh
```

**Port 8000 already in use?**
```bash
# Use different port
export PORT=8001
python3 app.py
```

**Dependencies missing?**
```bash
pip3 install Flask pymongo python-dotenv Werkzeug
```

---

## 📖 Full Documentation

For detailed guide, see: `USAGE_GUIDE.md`

---

**Ready to go! 🎉**

