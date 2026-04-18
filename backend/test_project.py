"""
Comprehensive Test Suite for KisanSathi Project
Tests all major features: Authentication, Crop Recommendation, Disease Detection, etc.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

# Test Results
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def print_test(name, status, message=""):
    """Print test result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if message:
        print(f"   └─ {message}")
    
    if status:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
        test_results["errors"].append(f"{name}: {message}")

# ===============================================================================================
# AUTHENTICATION TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🔐 AUTHENTICATION TESTS")
print("="*80)

# Test 1: User Registration
print("\n1️⃣ Testing User Registration...")
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "name": "Test Farmer",
        "email": "testfarmer@kisansathi.com",
        "mobile": "9876543210",
        "agriculture_type": "🌾 Cereals (Rice, Wheat, Maize)",
        "password": "TestPass123"
    })
    
    if response.status_code == 201:
        data = response.json()
        if data.get("success"):
            user_id = data.get("user_id")
            token = data.get("token")
            print_test("User Registration", True, f"User ID: {user_id}")
        else:
            print_test("User Registration", False, data.get("error"))
    else:
        print_test("User Registration", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("User Registration", False, str(e))

# Test 2: User Login
print("\n2️⃣ Testing User Login...")
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "mobile": "9876543210",
        "password": "TestPass123"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            token = data.get("token")
            user_id = data.get("user_id")
            print_test("User Login", True, f"Token: {token[:20]}...")
        else:
            print_test("User Login", False, data.get("error"))
    else:
        print_test("User Login", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("User Login", False, str(e))

# Test 3: Token Verification
print("\n3️⃣ Testing Token Verification...")
try:
    response = requests.post(f"{BASE_URL}/api/auth/verify-token", json={
        "token": token
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_test("Token Verification", True, f"User: {data.get('name')}")
        else:
            print_test("Token Verification", False, data.get("error"))
    else:
        print_test("Token Verification", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Token Verification", False, str(e))

# Test 4: Get User Profile
print("\n4️⃣ Testing Get User Profile...")
try:
    response = requests.get(f"{BASE_URL}/api/auth/profile/{user_id}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_test("Get User Profile", True, f"Name: {data.get('name')}")
        else:
            print_test("Get User Profile", False, data.get("error"))
    else:
        print_test("Get User Profile", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get User Profile", False, str(e))

# ===============================================================================================
# CROP RECOMMENDATION TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🌾 CROP RECOMMENDATION TESTS")
print("="*80)

# Test 5: Crop Prediction with Full Parameters
print("\n5️⃣ Testing Crop Prediction (Full Parameters)...")
try:
    response = requests.post(f"{BASE_URL}/api/crop-prediction", json={
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9
    })
    
    if response.status_code == 200:
        data = response.json()
        if "crop" in data:
            print_test("Crop Prediction (Full)", True, f"Recommended: {data.get('crop')}")
        else:
            print_test("Crop Prediction (Full)", False, str(data))
    else:
        print_test("Crop Prediction (Full)", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Crop Prediction (Full)", False, str(e))

# Test 6: Crop Prediction with Partial Parameters
print("\n6️⃣ Testing Crop Prediction (Partial Parameters)...")
try:
    response = requests.post(f"{BASE_URL}/api/crop-prediction-partial", json={
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87
    })
    
    if response.status_code == 200:
        data = response.json()
        if "crop" in data:
            print_test("Crop Prediction (Partial)", True, f"Recommended: {data.get('crop')}")
        else:
            print_test("Crop Prediction (Partial)", False, str(data))
    else:
        print_test("Crop Prediction (Partial)", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Crop Prediction (Partial)", False, str(e))

# Test 7: Get Available Crops
print("\n7️⃣ Testing Get Available Crops...")
try:
    response = requests.get(f"{BASE_URL}/api/get-available-crops")
    
    if response.status_code == 200:
        data = response.json()
        if "crops" in data:
            crops = data.get("crops", [])
            print_test("Get Available Crops", True, f"Total: {len(crops)} crops")
        else:
            print_test("Get Available Crops", False, str(data))
    else:
        print_test("Get Available Crops", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Available Crops", False, str(e))

# Test 8: Get Months Info
print("\n8️⃣ Testing Get Months Info...")
try:
    response = requests.get(f"{BASE_URL}/api/get-months")
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and len(data) > 0:
            print_test("Get Months Info", True, f"Months: {len(data)}")
        else:
            print_test("Get Months Info", False, str(data))
    else:
        print_test("Get Months Info", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Months Info", False, str(e))

# ===============================================================================================
# FERTILIZER RECOMMENDATION TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🧪 FERTILIZER RECOMMENDATION TESTS")
print("="*80)

# Test 9: Fertilizer Recommendation
print("\n9️⃣ Testing Fertilizer Recommendation...")
try:
    response = requests.post(f"{BASE_URL}/api/fert-recommend", json={
        "crop": "rice",
        "N": 90,
        "P": 42,
        "K": 43
    })
    
    if response.status_code == 200:
        data = response.json()
        if "fertilizer" in data:
            print_test("Fertilizer Recommendation", True, f"Recommended: {data.get('fertilizer')}")
        else:
            print_test("Fertilizer Recommendation", False, str(data))
    else:
        print_test("Fertilizer Recommendation", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Fertilizer Recommendation", False, str(e))

# Test 10: Get Fertilizer Info
print("\n🔟 Testing Get Fertilizer Info...")
try:
    response = requests.get(f"{BASE_URL}/api/get-fertilizer-info/DAP")
    
    if response.status_code == 200:
        data = response.json()
        if "name" in data:
            print_test("Get Fertilizer Info", True, f"Fertilizer: {data.get('name')}")
        else:
            print_test("Get Fertilizer Info", False, str(data))
    else:
        print_test("Get Fertilizer Info", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Fertilizer Info", False, str(e))

# ===============================================================================================
# WEATHER TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🌤️ WEATHER TESTS")
print("="*80)

# Test 11: Get Weather
print("\n1️⃣1️⃣ Testing Get Weather...")
try:
    response = requests.get(f"{BASE_URL}/api/get-weather?city=Delhi")
    
    if response.status_code == 200:
        data = response.json()
        if "temperature" in data:
            print_test("Get Weather", True, f"Temp: {data.get('temperature')}°C")
        else:
            print_test("Get Weather", False, str(data))
    else:
        print_test("Get Weather", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Weather", False, str(e))

# Test 12: Get Crop Alerts
print("\n1️⃣2️⃣ Testing Get Crop Alerts...")
try:
    response = requests.get(f"{BASE_URL}/api/get-crop-alerts?crop=rice")
    
    if response.status_code == 200:
        data = response.json()
        if "alerts" in data:
            print_test("Get Crop Alerts", True, f"Alerts: {len(data.get('alerts', []))}")
        else:
            print_test("Get Crop Alerts", False, str(data))
    else:
        print_test("Get Crop Alerts", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Crop Alerts", False, str(e))

# ===============================================================================================
# CHATBOT TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🤖 CHATBOT TESTS")
print("="*80)

# Test 13: Chatbot Message
print("\n1️⃣3️⃣ Testing Chatbot Message...")
try:
    response = requests.post(f"{BASE_URL}/api/chatbot/message", json={
        "message": "मेरी गेहूं की फसल के लिए क्या करूं?",
        "history": []
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_test("Chatbot Message", True, f"Response: {data.get('response')[:50]}...")
        else:
            print_test("Chatbot Message", False, data.get("error"))
    else:
        print_test("Chatbot Message", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Chatbot Message", False, str(e))

# Test 14: Quick Answer
print("\n1️⃣4️⃣ Testing Quick Answer...")
try:
    response = requests.get(f"{BASE_URL}/api/get-quick-answer?question_type=crop_care")
    
    if response.status_code == 200:
        data = response.json()
        if "answer" in data:
            print_test("Quick Answer", True, f"Answer: {data.get('answer')[:50]}...")
        else:
            print_test("Quick Answer", False, str(data))
    else:
        print_test("Quick Answer", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Quick Answer", False, str(e))

# ===============================================================================================
# CROP MANAGEMENT TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🌱 CROP MANAGEMENT TESTS")
print("="*80)

# Test 15: Add Crop
print("\n1️⃣5️⃣ Testing Add Crop...")
try:
    response = requests.post(f"{BASE_URL}/api/add-crop", json={
        "farmer_id": user_id,
        "crop_name": "rice",
        "planting_date": "2024-06-15",
        "area": 2.5,
        "soil_type": "loamy"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            crop_id = data.get("crop_id")
            print_test("Add Crop", True, f"Crop ID: {crop_id}")
        else:
            print_test("Add Crop", False, data.get("error"))
    else:
        print_test("Add Crop", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Add Crop", False, str(e))

# Test 16: Get Crops
print("\n1️⃣6️⃣ Testing Get Crops...")
try:
    response = requests.get(f"{BASE_URL}/api/get-crops/{user_id}")
    
    if response.status_code == 200:
        data = response.json()
        if "crops" in data:
            print_test("Get Crops", True, f"Total: {len(data.get('crops', []))} crops")
        else:
            print_test("Get Crops", False, str(data))
    else:
        print_test("Get Crops", False, f"Status: {response.status_code}")
except Exception as e:
    print_test("Get Crops", False, str(e))

# ===============================================================================================
# SUMMARY
# ===============================================================================================

print("\n" + "="*80)
print("📊 TEST SUMMARY")
print("="*80)
print(f"\n✅ Passed: {test_results['passed']}")
print(f"❌ Failed: {test_results['failed']}")
print(f"📈 Total: {test_results['passed'] + test_results['failed']}")

if test_results['failed'] > 0:
    print(f"\n⚠️ Failed Tests:")
    for error in test_results['errors']:
        print(f"   • {error}")
else:
    print("\n🎉 All tests passed!")

print("\n" + "="*80)
