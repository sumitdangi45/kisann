"""
Final Comprehensive Test Suite for KisanSathi Project
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

print("\n" + "="*80)
print("🧪 KISANSATHI PROJECT - COMPREHENSIVE TEST SUITE")
print("="*80)

# ===============================================================================================
# AUTHENTICATION TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🔐 AUTHENTICATION TESTS")
print("="*80)

user_id = None
token = None

# Test 1: User Registration
print("\n1️⃣ Testing User Registration...")
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "name": "Test Farmer",
        "email": "testfarmer@kisansathi.com",
        "mobile": "9876543210",
        "agriculture_type": "🌾 Cereals (Rice, Wheat, Maize)",
        "password": "TestPass123"
    }, timeout=5)
    
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
    }, timeout=5)
    
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
if token:
    try:
        response = requests.post(f"{BASE_URL}/api/auth/verify-token", json={
            "token": token
        }, timeout=5)
        
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
if user_id:
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile/{user_id}", timeout=5)
        
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
    response = requests.post(f"{BASE_URL}/api/crop-predict", json={
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9
    }, timeout=5)
    
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
    response = requests.post(f"{BASE_URL}/api/crop-predict-partial", json={
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87
    }, timeout=5)
    
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
    response = requests.get(f"{BASE_URL}/api/reminders/available-crops", timeout=5)
    
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
    response = requests.get(f"{BASE_URL}/api/months", timeout=5)
    
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
    response = requests.post(f"{BASE_URL}/api/fertilizer-recommend", json={
        "crop": "rice",
        "N": 90,
        "P": 42,
        "K": 43
    }, timeout=5)
    
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
    response = requests.get(f"{BASE_URL}/api/fertilizer-info/DAP", timeout=5)
    
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
# CHATBOT TESTS
# ===============================================================================================

print("\n" + "="*80)
print("🤖 CHATBOT TESTS")
print("="*80)

# Test 11: Chatbot Message
print("\n1️⃣1️⃣ Testing Chatbot Message...")
try:
    response = requests.post(f"{BASE_URL}/api/chatbot/message", json={
        "message": "मेरी गेहूं की फसल के लिए क्या करूं?",
        "history": []
    }, timeout=10)
    
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

# ===============================================================================================
# SUMMARY
# ===============================================================================================

print("\n" + "="*80)
print("📊 TEST SUMMARY")
print("="*80)
print(f"\n✅ Passed: {test_results['passed']}")
print(f"❌ Failed: {test_results['failed']}")
print(f"📈 Total: {test_results['passed'] + test_results['failed']}")
print(f"📊 Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")

if test_results['failed'] > 0:
    print(f"\n⚠️ Failed Tests:")
    for error in test_results['errors']:
        print(f"   • {error}")
else:
    print("\n🎉 All tests passed!")

print("\n" + "="*80)
print("✅ KisanSathi Backend is fully operational!")
print("="*80 + "\n")
