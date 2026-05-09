#!/usr/bin/env python3
"""
KisanSathi - Minimal Flask Backend for Render Deployment
This is a minimal version that starts the server without heavy ML dependencies
"""

import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_socketio import SocketIO
from dotenv import load_dotenv
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'kisansathi_secret_key_2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Rate Limiting Configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Caching Configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DATABASE', 'kisansathi')

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGODB_DB]
    # Test connection
    client.admin.command('ping')
    logger.info(f"✅ Connected to MongoDB: {MONGODB_DB}")
except Exception as e:
    logger.warning(f"⚠️ MongoDB connection failed: {e}")
    db = None

# ============================================================================
# ROOT & HEALTH CHECK ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'KisanSathi Backend API',
        'version': '5.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'status': '/api/status',
            'auth': '/api/auth/*',
            'community': '/api/community/*'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'kisansathi-backend'
    }), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    """Status endpoint"""
    db_status = 'connected' if db else 'disconnected'
    return jsonify({
        'status': 'running',
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        # Check if user exists
        users = db['users']
        if users.find_one({'email': data['email']}):
            return jsonify({'error': 'User already exists'}), 409
        
        # Create new user
        user = {
            'email': data['email'],
            'password': data['password'],  # In production, hash this!
            'created_at': datetime.now()
        }
        result = users.insert_one(user)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        if not db:
            return jsonify({'error': 'Database not available'}), 503
        
        # Find user
        users = db['users']
        user = users.find_one({'email': data['email']})
        
        if not user or user['password'] != data['password']:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'access_token': access_token,
            'user_id': str(user['_id']),
            'email': user['email']
        }), 200
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PLACEHOLDER ENDPOINTS (for future ML features)
# ============================================================================

@app.route('/api/recommendations/crop', methods=['POST'])
def crop_recommendation():
    """Placeholder for crop recommendation"""
    return jsonify({
        'message': 'Crop recommendation endpoint',
        'status': 'coming soon'
    }), 200

@app.route('/api/disease-predict', methods=['POST'])
def disease_predict():
    """Placeholder for disease prediction"""
    return jsonify({
        'message': 'Disease prediction endpoint',
        'status': 'coming soon'
    }), 200

@app.route('/api/fertilizer/recommend', methods=['POST'])
def fertilizer_recommend():
    """Placeholder for fertilizer recommendation"""
    return jsonify({
        'message': 'Fertilizer recommendation endpoint',
        'status': 'coming soon'
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
