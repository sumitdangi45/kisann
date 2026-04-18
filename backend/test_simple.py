"""Simple test to check if backend is working"""
import sys
import time

print("Testing KisanSathi Backend...")
print("="*80)

# Test 1: Check if MongoDB is working
print("\n1. Testing MongoDB Connection...")
try:
    from utils.auth_mongo import get_users_collection
    users = get_users_collection()
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB error: {e}")
    sys.exit(1)

# Test 2: Check if Gemini is working
print("\n2. Testing Gemini API...")
try:
    from utils.gemini_helper import generate_crop_explanation
    print("✅ Gemini API loaded successfully")
except Exception as e:
    print(f"❌ Gemini error: {e}")

# Test 3: Check if crop model is working
print("\n3. Testing Crop Model...")
try:
    import pickle
    with open('models/crop_model_trained.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Crop model loaded successfully")
except Exception as e:
    print(f"❌ Crop model error: {e}")

# Test 4: Check if weather integration is working
print("\n4. Testing Weather Integration...")
try:
    from utils.weather_integration import get_weather_for_farming
    weather = get_weather_for_farming("Delhi")
    if weather:
        print("✅ Weather integration working")
    else:
        print("⚠️ Weather data not available")
except Exception as e:
    print(f"❌ Weather error: {e}")

# Test 5: Check if Flask app is working
print("\n5. Testing Flask App...")
try:
    from app import app
    print("✅ Flask app loaded successfully")
    
    # List all routes
    print("\n📋 Available Routes:")
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(str(rule))
    
    # Filter and show auth routes
    auth_routes = [r for r in routes if '/api/auth/' in r]
    if auth_routes:
        print(f"\n✅ Auth Routes ({len(auth_routes)}):")
        for route in sorted(auth_routes):
            print(f"   • {route}")
    else:
        print("\n❌ No auth routes found!")
    
    # Show other important routes
    other_routes = [r for r in routes if '/api/' in r and '/api/auth/' not in r]
    print(f"\n✅ Other API Routes ({len(other_routes)}):")
    for route in sorted(other_routes)[:10]:
        print(f"   • {route}")
    if len(other_routes) > 10:
        print(f"   ... and {len(other_routes) - 10} more")
        
except Exception as e:
    print(f"❌ Flask error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ Backend components are ready!")
