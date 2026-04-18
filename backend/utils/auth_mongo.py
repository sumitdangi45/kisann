import os
import re
import hashlib
import secrets
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/kisansathi")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "kisansathi")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    db = client[MONGODB_DATABASE]
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
    db = None

# Collections
def get_users_collection():
    """Get users collection"""
    if db is None:
        raise Exception("MongoDB not connected")
    return db.users

def get_crops_collection():
    """Get crops collection"""
    if db is None:
        raise Exception("MongoDB not connected")
    return db.crops

def get_reminders_collection():
    """Get reminders collection"""
    if db is None:
        raise Exception("MongoDB not connected")
    return db.reminders

def create_indexes():
    """Create database indexes"""
    try:
        users = get_users_collection()
        users.create_index("mobile", unique=True)
        users.create_index("email", unique=True)
        users.create_index("token", unique=True)
        print("✅ Database indexes created")
    except Exception as e:
        print(f"Index creation error: {e}")

# Validation Functions
def validate_mobile_number(mobile):
    """Validate Indian mobile number (10 digits)"""
    if not mobile:
        return False, "Mobile number is required"
    
    mobile = mobile.replace(" ", "").replace("-", "")
    
    if not re.match(r"^[0-9]{10}$", mobile):
        return False, "Mobile number must be 10 digits"
    
    return True, "Valid"

def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, "Valid"

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if len(password) > 50:
        return False, "Password must be less than 50 characters"
    
    return True, "Valid"

def validate_name(name):
    """Validate farmer name"""
    if not name:
        return False, "Name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 100:
        return False, "Name must be less than 100 characters"
    
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, and hyphens"
    
    return True, "Valid"

def validate_agriculture_type(ag_type):
    """Validate agriculture type"""
    valid_types = [
        "🌾 Cereals (Rice, Wheat, Maize)",
        "🥬 Vegetables (Tomato, Onion, Potato)",
        "🌻 Cash Crops (Cotton, Sugarcane)",
        "🍎 Fruits & Orchards",
        "🌱 Organic Farming",
        "🐄 Dairy & Livestock",
        "🐟 Aquaculture",
        "🍯 Beekeeping",
        "🌿 Spices & Herbs",
        "🥕 Mixed Farming",
    ]
    
    if not ag_type:
        return False, "Agriculture type is required"
    
    if ag_type not in valid_types:
        return False, "Invalid agriculture type"
    
    return True, "Valid"

# Password Functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Generate a secure token"""
    return secrets.token_urlsafe(32)

# Authentication Functions
def register_user(name, email, mobile, agriculture_type, password):
    """Register a new user"""
    
    # Validate all inputs
    is_valid, msg = validate_name(name)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_email(email)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_mobile_number(mobile)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_agriculture_type(agriculture_type)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg
    
    try:
        users = get_users_collection()
        
        # Create new user document
        new_user = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "agriculture_type": agriculture_type,
            "password_hash": hash_password(password),
            "token": generate_token(),
            "created_at": datetime.now(),
            "last_login": None,
            "is_active": True,
            "profile_complete": False,
            "crops": [],
            "reminders": []
        }
        
        result = users.insert_one(new_user)
        
        return True, {
            "user_id": str(result.inserted_id),
            "token": new_user["token"],
            "name": new_user["name"],
            "message": "Registration successful!"
        }
    
    except DuplicateKeyError as e:
        if "mobile" in str(e):
            return False, "Mobile number already registered"
        elif "email" in str(e):
            return False, "Email already registered"
        else:
            return False, "User already exists"
    
    except Exception as e:
        print(f"Registration error: {e}")
        return False, "Registration failed"

def login_user(mobile, password):
    """Login user"""
    
    # Validate inputs
    is_valid, msg = validate_mobile_number(mobile)
    if not is_valid:
        return False, msg
    
    if not password:
        return False, "Password is required"
    
    try:
        users = get_users_collection()
        user = users.find_one({"mobile": mobile})
        
        if not user:
            return False, "Mobile number not registered"
        
        # Check password
        if user.get("password_hash") != hash_password(password):
            return False, "Invalid password"
        
        if not user.get("is_active"):
            return False, "Account is inactive"
        
        # Update last login
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.now()}}
        )
        
        return True, {
            "user_id": str(user["_id"]),
            "token": user["token"],
            "name": user["name"],
            "email": user["email"],
            "agriculture_type": user["agriculture_type"],
            "message": "Login successful!"
        }
    
    except Exception as e:
        print(f"Login error: {e}")
        return False, "Login failed"

def verify_token(token):
    """Verify if token is valid"""
    if not token:
        return False, None
    
    try:
        users = get_users_collection()
        user = users.find_one({"token": token, "is_active": True})
        
        if user:
            return True, user
        else:
            return False, None
    
    except Exception as e:
        print(f"Token verification error: {e}")
        return False, None

def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        users = get_users_collection()
        user = users.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception as e:
        print(f"Get user error: {e}")
        return None

def update_user_profile(user_id, **kwargs):
    """Update user profile"""
    try:
        users = get_users_collection()
        
        # Only allow updating specific fields
        allowed_fields = ["name", "email", "agriculture_type"]
        update_data = {}
        
        for field in allowed_fields:
            if field in kwargs:
                update_data[field] = kwargs[field]
        
        if update_data:
            update_data["profile_complete"] = True
            
            result = users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.matched_count > 0:
                return True, "Profile updated successfully"
            else:
                return False, "User not found"
        else:
            return False, "No valid fields to update"
    
    except Exception as e:
        print(f"Update profile error: {e}")
        return False, "Update failed"

def change_password(user_id, old_password, new_password):
    """Change user password"""
    
    # Validate new password
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg
    
    try:
        users = get_users_collection()
        user = users.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return False, "User not found"
        
        # Verify old password
        if user.get("password_hash") != hash_password(old_password):
            return False, "Current password is incorrect"
        
        # Update password
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password_hash": hash_password(new_password)}}
        )
        
        return True, "Password changed successfully"
    
    except Exception as e:
        print(f"Change password error: {e}")
        return False, "Password change failed"

def reset_password(mobile, new_password):
    """Reset password (for forgot password feature)"""
    
    # Validate inputs
    is_valid, msg = validate_mobile_number(mobile)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg
    
    try:
        users = get_users_collection()
        result = users.update_one(
            {"mobile": mobile},
            {"$set": {"password_hash": hash_password(new_password)}}
        )
        
        if result.matched_count > 0:
            return True, "Password reset successfully"
        else:
            return False, "Mobile number not found"
    
    except Exception as e:
        print(f"Reset password error: {e}")
        return False, "Password reset failed"

def deactivate_user(user_id):
    """Deactivate user account"""
    try:
        users = get_users_collection()
        result = users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False}}
        )
        
        if result.matched_count > 0:
            return True, "Account deactivated"
        else:
            return False, "User not found"
    
    except Exception as e:
        print(f"Deactivate user error: {e}")
        return False, "Deactivation failed"

def activate_user(user_id):
    """Activate user account"""
    try:
        users = get_users_collection()
        result = users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": True}}
        )
        
        if result.matched_count > 0:
            return True, "Account activated"
        else:
            return False, "User not found"
    
    except Exception as e:
        print(f"Activate user error: {e}")
        return False, "Activation failed"

def get_all_users():
    """Get all users (admin only)"""
    try:
        users = get_users_collection()
        all_users = []
        
        for user in users.find():
            safe_user = {
                "user_id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "mobile": user.get("mobile"),
                "agriculture_type": user.get("agriculture_type"),
                "created_at": user.get("created_at"),
                "last_login": user.get("last_login"),
                "is_active": user.get("is_active")
            }
            all_users.append(safe_user)
        
        return all_users
    
    except Exception as e:
        print(f"Get all users error: {e}")
        return []

# Initialize database
if db is not None:
    create_indexes()
