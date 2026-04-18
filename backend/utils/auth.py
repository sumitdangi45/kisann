import json
import os
import re
from datetime import datetime, timedelta
import hashlib
import secrets
from pathlib import Path

# Database file for storing user data
USERS_DB_FILE = os.path.join(os.path.dirname(__file__), "../Data/users.json")

def ensure_users_db():
    """Ensure users database file exists"""
    Path(USERS_DB_FILE).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'w') as f:
            json.dump({"users": []}, f)

def load_users():
    """Load users from database"""
    ensure_users_db()
    try:
        with open(USERS_DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"users": []}

def save_users(data):
    """Save users to database"""
    ensure_users_db()
    with open(USERS_DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_mobile_number(mobile):
    """Validate Indian mobile number (10 digits)"""
    if not mobile:
        return False, "Mobile number is required"
    
    # Remove any spaces or dashes
    mobile = mobile.replace(" ", "").replace("-", "")
    
    # Check if it's exactly 10 digits
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
    
    # Allow letters, spaces, and hyphens
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

def user_exists(mobile):
    """Check if user already exists"""
    users_data = load_users()
    for user in users_data.get("users", []):
        if user.get("mobile") == mobile:
            return True
    return False

def email_exists(email):
    """Check if email already exists"""
    users_data = load_users()
    for user in users_data.get("users", []):
        if user.get("email") == email:
            return True
    return False

def generate_token():
    """Generate a secure token"""
    return secrets.token_urlsafe(32)

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
    
    # Check if user already exists
    if user_exists(mobile):
        return False, "Mobile number already registered"
    
    if email_exists(email):
        return False, "Email already registered"
    
    # Create new user
    users_data = load_users()
    
    new_user = {
        "user_id": f"farmer_{len(users_data['users']) + 1}",
        "name": name,
        "email": email,
        "mobile": mobile,
        "agriculture_type": agriculture_type,
        "password_hash": hash_password(password),
        "token": generate_token(),
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "is_active": True,
        "profile_complete": False,
        "crops": [],
        "reminders": []
    }
    
    users_data["users"].append(new_user)
    save_users(users_data)
    
    return True, {
        "user_id": new_user["user_id"],
        "token": new_user["token"],
        "name": new_user["name"],
        "message": "Registration successful!"
    }

def login_user(mobile, password):
    """Login user"""
    
    # Validate inputs
    is_valid, msg = validate_mobile_number(mobile)
    if not is_valid:
        return False, msg
    
    if not password:
        return False, "Password is required"
    
    # Find user
    users_data = load_users()
    user = None
    
    for u in users_data.get("users", []):
        if u.get("mobile") == mobile:
            user = u
            break
    
    if not user:
        return False, "Mobile number not registered"
    
    # Check password
    if user.get("password_hash") != hash_password(password):
        return False, "Invalid password"
    
    if not user.get("is_active"):
        return False, "Account is inactive"
    
    # Update last login
    user["last_login"] = datetime.now().isoformat()
    save_users(users_data)
    
    return True, {
        "user_id": user["user_id"],
        "token": user["token"],
        "name": user["name"],
        "email": user["email"],
        "agriculture_type": user["agriculture_type"],
        "message": "Login successful!"
    }

def verify_token(token):
    """Verify if token is valid"""
    if not token:
        return False, None
    
    users_data = load_users()
    for user in users_data.get("users", []):
        if user.get("token") == token and user.get("is_active"):
            return True, user
    
    return False, None

def get_user_by_id(user_id):
    """Get user by ID"""
    users_data = load_users()
    for user in users_data.get("users", []):
        if user.get("user_id") == user_id:
            return user
    return None

def update_user_profile(user_id, **kwargs):
    """Update user profile"""
    users_data = load_users()
    
    for user in users_data.get("users", []):
        if user.get("user_id") == user_id:
            # Only allow updating specific fields
            allowed_fields = ["name", "email", "agriculture_type"]
            for field in allowed_fields:
                if field in kwargs:
                    user[field] = kwargs[field]
            
            user["profile_complete"] = True
            save_users(users_data)
            return True, "Profile updated successfully"
    
    return False, "User not found"

def change_password(user_id, old_password, new_password):
    """Change user password"""
    
    # Validate new password
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg
    
    users_data = load_users()
    
    for user in users_data.get("users", []):
        if user.get("user_id") == user_id:
            # Verify old password
            if user.get("password_hash") != hash_password(old_password):
                return False, "Current password is incorrect"
            
            # Update password
            user["password_hash"] = hash_password(new_password)
            save_users(users_data)
            return True, "Password changed successfully"
    
    return False, "User not found"

def reset_password(mobile, new_password):
    """Reset password (for forgot password feature)"""
    
    # Validate inputs
    is_valid, msg = validate_mobile_number(mobile)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg
    
    users_data = load_users()
    
    for user in users_data.get("users", []):
        if user.get("mobile") == mobile:
            user["password_hash"] = hash_password(new_password)
            save_users(users_data)
            return True, "Password reset successfully"
    
    return False, "Mobile number not found"

def get_all_users():
    """Get all users (admin only)"""
    users_data = load_users()
    # Remove sensitive data
    users = []
    for user in users_data.get("users", []):
        safe_user = {
            "user_id": user.get("user_id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "mobile": user.get("mobile"),
            "agriculture_type": user.get("agriculture_type"),
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login"),
            "is_active": user.get("is_active")
        }
        users.append(safe_user)
    return users

def deactivate_user(user_id):
    """Deactivate user account"""
    users_data = load_users()
    
    for user in users_data.get("users", []):
        if user.get("user_id") == user_id:
            user["is_active"] = False
            save_users(users_data)
            return True, "Account deactivated"
    
    return False, "User not found"

def activate_user(user_id):
    """Activate user account"""
    users_data = load_users()
    
    for user in users_data.get("users", []):
        if user.get("user_id") == user_id:
            user["is_active"] = True
            save_users(users_data)
            return True, "Account activated"
    
    return False, "User not found"
