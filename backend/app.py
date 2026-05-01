# Importing essential libraries and modules

from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from markupsafe import Markup
import numpy as np
import pandas as pd
from utils.gemini_helper import generate_crop_explanation
from utils.month_crops import filter_crops_by_month, get_all_months
from utils.fertilizer_recommendation import recommend_fertilizer, get_fertilizer_info
from utils.crop_identifier import identify_crop_from_image, get_crop_default_nutrients
from utils.disease import disease_dic
from utils.weather_alerts import get_weather_alerts, get_weather_summary, get_crop_specific_alerts
from utils.crop_lifecycle import get_crop_lifecycle, get_tasks_for_crop, get_upcoming_tasks, get_all_crops_with_lifecycle
from utils.reminders_db import (
    add_crop, get_farmer_crops, get_crop_by_id, create_reminders_for_crop,
    get_crop_reminders, get_pending_reminders, get_today_reminders, get_upcoming_reminders,
    mark_reminder_complete, get_reminder_progress, add_photo, get_crop_photos,
    update_photo_analysis, get_photo_timeline, get_crop_statistics, get_days_elapsed
)
from utils.smart_notifications import (
    generate_personalized_reminder, generate_crop_stage_message, 
    generate_alert_message, generate_encouragement_message, format_notification
)
from utils.voice_assistant import process_farming_question, get_quick_answers, get_crop_specific_advice
from utils.unified_chatbot import process_unified_chat, detect_language, detect_feature_request
import requests
import config
import pickle
import io
import os
import json
from PIL import Image
import hashlib
import base64

# ── Load trained fertilizer model ────────────────────────────────────────────
fertilizer_ml_model = None
fertilizer_soil_enc = None
fertilizer_crop_enc = None
fertilizer_label_enc = None
fertilizer_feature_info = None

try:
    fertilizer_ml_model    = pickle.load(open('models/fertilizer_model.pkl', 'rb'))
    fertilizer_soil_enc    = pickle.load(open('models/fertilizer_soil_encoder.pkl', 'rb'))
    fertilizer_crop_enc    = pickle.load(open('models/fertilizer_crop_encoder.pkl', 'rb'))
    fertilizer_label_enc   = pickle.load(open('models/fertilizer_label_encoder.pkl', 'rb'))
    fertilizer_feature_info = pickle.load(open('models/fertilizer_feature_info.pkl', 'rb'))
    print("✅ Fertilizer ML model loaded successfully!")
    print(f"   Fertilizers: {fertilizer_feature_info['fertilizers']}")
except Exception as e:
    print(f"⚠️  Fertilizer ML model not found, using rule-based fallback: {e}")

# ── Load PlantVillage MobileNetV2 disease model ───────────────────────────────
TORCH_AVAILABLE = False
disease_model = None
disease_class_names = []

try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms

    with open('models/class_names.json') as f:
        disease_class_names = json.load(f)

    _m = models.mobilenet_v2(weights=None)
    _m.classifier[1] = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(_m.classifier[1].in_features, 38)
    )
    _m.load_state_dict(torch.load('models/mobilenetv2_plant.pth', map_location='cpu'))
    _m.eval()
    disease_model = _m
    TORCH_AVAILABLE = True

    _disease_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    print(f"✅ PlantVillage MobileNetV2 disease model loaded! ({len(disease_class_names)} classes)")
except Exception as e:
    print(f"⚠️  Disease model load error: {e}")

# ── Load Rice Leaf Disease model ──────────────────────────────────────────────
rice_disease_model = None
rice_disease_classes = []

try:
    import torch, torch.nn as nn
    from torchvision import models, transforms
    with open('models/rice_disease_info.json') as f:
        _rice_info = json.load(f)
    rice_disease_classes = _rice_info['classes']

    _rm = models.mobilenet_v2(weights=None)
    _rm.classifier[1] = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(_rm.classifier[1].in_features, len(rice_disease_classes))
    )
    _rm.load_state_dict(torch.load('models/rice_disease_model.pth', map_location='cpu'))
    _rm.eval()
    rice_disease_model = _rm

    _rice_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    print(f"✅ Rice disease model loaded! Classes: {rice_disease_classes}")
except Exception as e:
    print(f"⚠️  Rice disease model load error: {e}")

# ── predict_image using MobileNetV2 ──────────────────────────────────────────
def predict_image(img_data, model=None):
    """
    Predict plant disease from image bytes.
    Returns (class_name, confidence) tuple.
    Uses MobileNetV2 PlantVillage model when available.
    """
    if TORCH_AVAILABLE and disease_model is not None:
        try:
            import torch
            image = Image.open(io.BytesIO(img_data)).convert('RGB')
            tensor = _disease_transform(image).unsqueeze(0)
            with torch.no_grad():
                out = disease_model(tensor)
                probs = torch.softmax(out, dim=1)[0]
                idx = probs.argmax().item()
                confidence = float(probs[idx])
            return disease_class_names[idx], confidence
        except Exception as e:
            print(f"MobileNetV2 inference error: {e}")

    # Fallback
    return 'Tomato___healthy', 0.0


# Loading crop recommendation model

crop_recommendation_model = None
crop_features = None
crop_encoder = None

try:
    crop_recommendation_model_path = 'models/crop_model_trained.pkl'
    crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))
    crop_features = pickle.load(open('models/crop_features.pkl', 'rb'))
    crop_encoder = pickle.load(open('models/crop_encoder.pkl', 'rb'))
    print("✅ Trained crop model loaded successfully!")
except Exception as e:
    print(f"⚠️ Could not load trained crop model: {e}")
    print("Trying to load old model...")
    try:
        crop_recommendation_model = pickle.load(open('models/RandomForest.pkl', 'rb'))
        print("✅ Old crop model loaded as fallback")
    except:
        print("Using mock model for crop recommendation")
        crop_recommendation_model = None


# =========================================================================================

# Custom functions for calculations

def mock_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    """
    Mock crop recommendation based on simple rules
    """
    crops = {
        'Rice': (40, 40, 40, 25, 80, 6.5, 200),
        'Wheat': (60, 45, 45, 20, 60, 7.0, 50),
        'Corn': (60, 60, 60, 21, 60, 6.5, 60),
        'Potato': (100, 60, 60, 18, 70, 6.0, 50),
        'Tomato': (100, 60, 60, 25, 70, 6.5, 50),
        'Cotton': (80, 40, 40, 25, 50, 6.5, 50),
    }
    
    best_crop = 'Rice'
    best_score = 0
    
    for crop, (n_req, p_req, k_req, temp_opt, humid_opt, ph_opt, rain_opt) in crops.items():
        # Simple scoring based on how close inputs are to requirements
        score = 0
        score += min(N, n_req) / max(N, n_req) * 20
        score += min(P, p_req) / max(P, p_req) * 20
        score += min(K, k_req) / max(K, k_req) * 20
        score += (1 - abs(temperature - temp_opt) / 30) * 15
        score += (1 - abs(humidity - humid_opt) / 100) * 15
        score += (1 - abs(ph - ph_opt) / 2) * 10
        
        if score > best_score:
            best_score = score
            best_crop = crop
    
    return best_crop


def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    try:
        api_key = config.weather_api_key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url, timeout=5)
        x = response.json()

        if x.get("cod") != "404" and "main" in x:
            y = x["main"]
            temperature = round((y["temp"] - 273.15), 2)
            humidity = y["humidity"]
            return temperature, humidity
        else:
            # Return default values if city not found
            return 25.0, 60
    except Exception as e:
        print(f"Weather fetch error: {e}")
        # Return default values on error
        return 25.0, 60

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080", "http://localhost:3000", "*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# render home page with services


@ app.route('/')
def home():
    title = 'KisanSathi - Services'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'KisanSathi - Crop Recommendation'
    return render_template('crop.html', title=title)

# render fertilizer recommendation form page


@ app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'KisanSathi - Fertilizer Suggestion'
    return render_template('fertilizer.html', title=title)

# render disease prediction input page


@ app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'KisanSathi - Disease Detection'

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', title=title)
        try:
            img = file.read()
            prediction, _ = predict_image(img, disease_model)
            prediction = Markup(str(disease_dic[prediction]))
            return render_template('disease-result.html', prediction=prediction, title=title)
        except:
            pass
    return render_template('disease.html', title=title)

# render crop recommendation result page


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'KisanSathi - Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        city = request.form.get("city")

        temperature, humidity = weather_fetch(city)
        
        # Use loaded model or mock model
        if crop_recommendation_model is not None:
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
        else:
            final_prediction = mock_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall)

        return render_template('crop-result.html', prediction=final_prediction, title=title)

# render fertilizer recommendation result page


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'KisanSathi - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer-result.html', recommendation=response, title=title)


# ===============================================================================================
# API ENDPOINTS FOR REACT FRONTEND
# ===============================================================================================

# API: Crop Recommendation
@app.route('/api/crop-predict', methods=['POST'])
def api_crop_prediction():
    try:
        data = request.get_json()
        N = int(data['nitrogen'])
        P = int(data.get('phosphorous') or data.get('phosphorus'))
        K = int(data.get('potassium') or data.get('pottasium'))
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        city = data.get('city', 'Delhi')
        month = data.get('month', None)

        temperature, humidity = weather_fetch(city)
        
        if crop_recommendation_model is not None:
            # Use trained model
            pred_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            prediction = crop_recommendation_model.predict(pred_data)[0]
        else:
            # Fallback to mock model
            prediction = mock_crop_recommendation(N, P, K, temperature, humidity, ph, rainfall)

        # Check if crop is suitable for the month
        month_info = None
        if month:
            month_info = filter_crops_by_month(prediction, month)
            # If not suitable, use recommended crop
            if not month_info['suitable']:
                prediction = month_info['recommended']

        # Generate explanation using Gemini
        explanation = generate_crop_explanation(prediction, N, P, K, temperature, humidity, ph, rainfall)

        response_data = {
            'success': True,
            'crop': str(prediction),
            'temperature': temperature,
            'humidity': humidity,
            'explanation': explanation
        }
        
        # Add month info if provided
        if month_info:
            response_data['month_info'] = month_info

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Fertilizer Recommendation
@app.route('/api/fertilizer-predict', methods=['POST'])
def api_fert_recommend():
    try:
        data = request.get_json()
        crop_name = str(data['cropname']).lower()
        N = int(data['nitrogen'])
        P = int(data['phosphorous'])
        K = int(data['potassium'])

        df = pd.read_csv('Data/fertilizer.csv')
        
        # Filter by crop name (case-insensitive)
        crop_data = df[df['Crop'].str.lower() == crop_name]
        
        if crop_data.empty:
            return jsonify({'success': False, 'error': f'Crop "{crop_name}" not found in database'}), 400
        
        nr = crop_data['N'].iloc[0]
        pr = crop_data['P'].iloc[0]
        kr = crop_data['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        
        if max_value == "N":
            key = 'NHigh' if n < 0 else "Nlow"
        elif max_value == "P":
            key = 'PHigh' if p < 0 else "Plow"
        else:
            key = 'KHigh' if k < 0 else "Klow"

        recommendation = fertilizer_dic[key]
        
        return jsonify({
            'success': True,
            'recommendation': recommendation,
            'deficiency': key
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get All Months
@app.route('/api/months', methods=['GET'])
def api_get_months():
    try:
        months = get_all_months()
        return jsonify({
            'success': True,
            'months': months
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Disease Detection (Multiple Images)
@app.route('/api/disease-predict', methods=['POST'])
def api_disease_prediction():
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'success': False, 'error': 'No files selected'}), 400
        
        predictions = []
        
        # Process each image
        for file in files:
            if not file or file.filename == '':
                continue
            
            # Check if file is image
            if not any(file.filename.lower().endswith('.' + ext) for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']):
                continue
            
            try:
                img_data = file.read()
                prediction, confidence = predict_image(img_data, disease_model)
                disease_info = disease_dic.get(prediction, 'Disease not found')
                
                predictions.append({
                    'filename': file.filename,
                    'disease': prediction,
                    'confidence': round(confidence * 100, 1),
                    'info': disease_info,
                    'success': True
                })
            except Exception as e:
                predictions.append({
                    'filename': file.filename,
                    'error': str(e),
                    'success': False
                })
        
        if len(predictions) == 0:
            return jsonify({'success': False, 'error': 'No valid images found'}), 400
        
        # Determine most common disease
        disease_counts = {}
        for pred in predictions:
            if pred['success']:
                disease = pred['disease']
                disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        most_common_disease = max(disease_counts, key=disease_counts.get) if disease_counts else 'Unknown'
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'total_images': len(predictions),
            'most_common_disease': most_common_disease,
            'disease_info': disease_dic.get(most_common_disease, 'Disease not found'),
            'summary': f'Analyzed {len(predictions)} images. Most common disease: {most_common_disease}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Rice Leaf Disease Detection
@app.route('/api/rice-disease-predict', methods=['POST'])
def api_rice_disease_predict():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if rice_disease_model is None:
            return jsonify({'success': False, 'error': 'Rice disease model not loaded'}), 500

        img_data = file.read()

        import torch
        image = Image.open(io.BytesIO(img_data)).convert('RGB')
        tensor = _rice_transform(image).unsqueeze(0)
        with torch.no_grad():
            out   = rice_disease_model(tensor)
            probs = torch.softmax(out, dim=1)[0]
            idx   = probs.argmax().item()
            confidence = float(probs[idx])

        disease = rice_disease_classes[idx]

        # All class confidences
        all_probs = {rice_disease_classes[i]: round(float(probs[i]) * 100, 1)
                     for i in range(len(rice_disease_classes))}

        rice_disease_info = {
            'Bacterial leaf blight': 'Bacterial disease caused by Xanthomonas oryzae. Leaves show water-soaked to yellowish stripes. Treat with copper-based bactericides and avoid excess nitrogen.',
            'Brown spot':            'Fungal disease caused by Cochliobolus miyabeanus. Brown oval spots on leaves. Apply Mancozeb or Tricyclazole fungicide. Ensure balanced potassium nutrition.',
            'Leaf smut':             'Fungal disease caused by Entyloma oryzae. Small, angular, black spots on leaves. Use certified disease-free seeds and apply Propiconazole fungicide.'
        }

        return jsonify({
            'success':     True,
            'disease':     disease,
            'confidence':  round(confidence * 100, 1),
            'all_probabilities': all_probs,
            'info':        rice_disease_info.get(disease, 'No info available'),
            'is_rice':     True,
            'filename':    file.filename
        })

    except Exception as e:
        print(f"Rice disease prediction error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Soil Report PDF Upload and Analysis
@app.route('/api/soil-report-predict', methods=['POST'])
def api_soil_report_prediction():
    try:
        from utils.pdf_extractor import extract_text_from_pdf, extract_soil_parameters, validate_extracted_parameters
        import os
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if file is PDF
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'Only PDF files are supported'}), 400
        
        # Save uploaded file temporarily
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        
        try:
            # Extract text from PDF
            pdf_text = extract_text_from_pdf(filepath)
            if not pdf_text:
                return jsonify({'success': False, 'error': 'Could not extract text from PDF'}), 400
            
            # Extract soil parameters
            extracted_params = extract_soil_parameters(pdf_text)
            validated_params = validate_extracted_parameters(extracted_params)
            
            # Get month from request if provided
            month = request.form.get('month', '')
            
            # Check if we have minimum required parameters (at least 4)
            available_params = {k: v for k, v in validated_params.items() if v is not None}
            
            if len(available_params) < 4:
                return jsonify({
                    'success': False,
                    'error': f'Need at least 4 parameters. Found only {len(available_params)}: {list(available_params.keys())}',
                    'extracted': validated_params,
                    'available_count': len(available_params),
                    'pdf_text_preview': pdf_text[:500]
                }), 400
            
            # Prepare data for prediction with defaults for missing values
            N = validated_params['nitrogen'] or 50
            P = validated_params['phosphorus'] or 25
            K = validated_params['potassium'] or 25
            temperature = validated_params['temperature'] or 25
            humidity = validated_params['humidity'] or 60
            ph = validated_params['ph'] or 6.5
            rainfall = validated_params['rainfall'] or 100
            
            # Make prediction
            prediction = crop_recommendation_model.predict([[N, P, K, temperature, humidity, ph, rainfall]])[0]
            
            # Get explanation from Gemini
            explanation = generate_crop_explanation(prediction, N, P, K, temperature, humidity, ph, rainfall)
            
            # Get month info if month is provided
            month_info = None
            if month:
                month_info = filter_crops_by_month(prediction, month)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'crop': prediction,
                'explanation': explanation,
                'temperature': temperature,
                'humidity': humidity,
                'extracted_parameters': validated_params,
                'available_parameters': list(available_params.keys()),
                'parameters_count': len(available_params),
                'month_info': month_info
            })
        
        finally:
            # Ensure file is deleted even if error occurs
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        print(f"Error in soil report prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Soil Report Image Upload and Analysis
@app.route('/api/soil-image-predict', methods=['POST'])
def api_soil_image_prediction():
    try:
        from utils.image_extractor import extract_soil_parameters_from_image
        import os
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if file is image
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
        if not any(file.filename.lower().endswith('.' + ext) for ext in allowed_extensions):
            return jsonify({'success': False, 'error': 'Only image files are supported (JPG, PNG, GIF, BMP)'}), 400
        
        # Read image data
        image_data = file.read()
        
        # Get month from request if provided
        month = request.form.get('month', '')
        
        try:
            # Extract soil parameters from image
            extracted_params = extract_soil_parameters_from_image(image_data)
            validated_params = validate_extracted_parameters(extracted_params)
            
            # Get available parameters
            available_params = {k: v for k, v in validated_params.items() if v is not None}
            
            if not available_params:
                return jsonify({
                    'success': False,
                    'error': 'Could not extract any soil parameters from the image',
                    'extracted': validated_params
                }), 400
            
            # Check if we have minimum required parameters for prediction
            required_params = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
            missing_params = [p for p in required_params if validated_params.get(p) is None]
            
            # If we have at least 4 parameters, make prediction with defaults for missing ones
            if len(available_params) < 4:
                return jsonify({
                    'success': False,
                    'error': f'Need at least 4 parameters. Found only {len(available_params)}: {list(available_params.keys())}',
                    'extracted': validated_params,
                    'available_count': len(available_params)
                }), 400
            
            # Use extracted values or defaults for missing ones
            N = validated_params['nitrogen'] or 50
            P = validated_params['phosphorus'] or 25
            K = validated_params['potassium'] or 25
            temperature = validated_params['temperature'] or 25
            humidity = validated_params['humidity'] or 60
            ph = validated_params['ph'] or 6.5
            rainfall = validated_params['rainfall'] or 100
            
            # Make prediction
            prediction = crop_recommendation_model.predict([[N, P, K, temperature, humidity, ph, rainfall]])[0]
            
            # Get explanation from Gemini
            explanation = generate_crop_explanation(prediction, N, P, K, temperature, humidity, ph, rainfall)
            
            # Get month info if month is provided
            month_info = None
            if month:
                month_info = filter_crops_by_month(prediction, month)
            
            return jsonify({
                'success': True,
                'crop': prediction,
                'explanation': explanation,
                'temperature': temperature,
                'humidity': humidity,
                'extracted_parameters': validated_params,
                'available_parameters': list(available_params.keys()),
                'parameters_count': len(available_params),
                'month_info': month_info
            })
        
        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({'success': False, 'error': f'Error processing image: {str(e)}'}), 400
    
    except Exception as e:
        print(f"Error in soil image prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Partial Data Prediction (with available parameters)
@app.route('/api/crop-predict-partial', methods=['POST'])
def api_crop_prediction_partial():
    try:
        data = request.get_json()
        
        # Get available parameters
        N = data.get('nitrogen')
        P = data.get('phosphorus')
        K = data.get('potassium')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        ph = data.get('ph')
        rainfall = data.get('rainfall')
        month = data.get('month', '')
        
        # Count available parameters
        available = sum([1 for v in [N, P, K, temperature, humidity, ph, rainfall] if v is not None])
        
        if available < 4:
            return jsonify({
                'success': False,
                'error': f'Need at least 4 parameters. Got {available}',
                'available_count': available
            }), 400
        
        # Use defaults for missing parameters
        N = N or 50
        P = P or 25
        K = K or 25
        temperature = temperature or 25
        humidity = humidity or 60
        ph = ph or 6.5
        rainfall = rainfall or 100
        
        # Make prediction
        prediction = crop_recommendation_model.predict([[N, P, K, temperature, humidity, ph, rainfall]])[0]
        
        # Get explanation from Gemini
        explanation = generate_crop_explanation(prediction, N, P, K, temperature, humidity, ph, rainfall)
        
        # Get month info if month is provided
        month_info = None
        if month:
            month_info = filter_crops_by_month(prediction, month)
        
        return jsonify({
            'success': True,
            'crop': prediction,
            'explanation': explanation,
            'temperature': temperature,
            'humidity': humidity,
            'parameters_used': available,
            'month_info': month_info
        })
    
    except Exception as e:
        print(f"Error in partial prediction: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Fertilizer Recommendation
@app.route('/api/fertilizer-recommend', methods=['POST'])
def api_fertilizer_recommendation():
    try:
        data = request.get_json()

        crop      = data.get('crop', '').strip()
        nitrogen  = data.get('nitrogen')
        phosphorus = data.get('phosphorus')
        potassium  = data.get('potassium')
        soil_type  = data.get('soil_type', 'Loamy').strip().title()
        temperature = data.get('temperature', 30.0)
        humidity    = data.get('humidity', 60.0)
        moisture    = data.get('moisture', 45.0)

        if not crop:
            return jsonify({'success': False, 'error': 'Crop name is required'}), 400
        if nitrogen is None or phosphorus is None or potassium is None:
            return jsonify({'success': False, 'error': 'Nitrogen, Phosphorus, and Potassium values are required'}), 400

        ml_fertilizer = None
        ml_used = False

        # ── Try ML model first ────────────────────────────────────────────────
        if fertilizer_ml_model is not None:
            try:
                crop_title = crop.strip().title()
                soil_title = soil_type.strip().title()

                known_soils = fertilizer_feature_info['soil_types']
                known_crops = fertilizer_feature_info['crop_types']

                if soil_title not in known_soils:
                    soil_title = known_soils[0]
                if crop_title not in known_crops:
                    crop_title = known_crops[0]

                soil_enc = fertilizer_soil_enc.transform([soil_title])[0]
                crop_enc = fertilizer_crop_enc.transform([crop_title])[0]

                N, P, K = float(nitrogen), float(phosphorus), float(potassium)
                n_p_ratio  = N / (P + 1)
                n_k_ratio  = N / (K + 1)
                npk_total  = N + P + K

                features = np.array([[
                    float(temperature), float(humidity), float(moisture),
                    soil_enc, crop_enc,
                    N, K, P,
                    n_p_ratio, n_k_ratio, npk_total
                ]])

                pred_enc = fertilizer_ml_model.predict(features)[0]
                ml_fertilizer = fertilizer_label_enc.inverse_transform([pred_enc])[0]
                ml_used = True
            except Exception as e:
                print(f"ML model prediction error: {e}")

        # ── Rule-based recommendation (always computed for details) ───────────
        rule_rec = recommend_fertilizer(crop, float(nitrogen), float(phosphorus), float(potassium))

        if not rule_rec.get('success'):
            # If crop not in rule DB, still return ML result if available
            if ml_fertilizer:
                return jsonify({
                    'success': True,
                    'crop': crop,
                    'ml_fertilizer': ml_fertilizer,
                    'ml_used': ml_used,
                    'soil_status': {
                        'nitrogen':   {'value': nitrogen,   'level': 'unknown'},
                        'phosphorus': {'value': phosphorus, 'level': 'unknown'},
                        'potassium':  {'value': potassium,  'level': 'unknown'},
                    },
                    'primary_deficiency': 'unknown',
                    'primary_recommendation': {'fertilizer': ml_fertilizer, 'quantity': 'As per label', 'timing': 'At planting', 'reason': 'ML model recommendation', 'benefits': 'Balanced nutrition'},
                    'secondary_recommendations': [],
                    'summary': f"ML model recommends {ml_fertilizer} for {crop}."
                })
            return jsonify(rule_rec), 400

        # Override fertilizer name with ML prediction if available
        if ml_fertilizer:
            rule_rec['primary_recommendation']['fertilizer'] = ml_fertilizer
            rule_rec['ml_fertilizer'] = ml_fertilizer
            rule_rec['ml_used'] = True
            rule_rec['summary'] = (
                f"ML model recommends {ml_fertilizer} for {crop}. "
                f"Soil has {rule_rec['soil_status']['nitrogen']['level']} nitrogen, "
                f"{rule_rec['soil_status']['phosphorus']['level']} phosphorus, "
                f"{rule_rec['soil_status']['potassium']['level']} potassium."
            )
        else:
            rule_rec['ml_used'] = False

        return jsonify(rule_rec)

    except Exception as e:
        print(f"Error in fertilizer recommendation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get Fertilizer Info
@app.route('/api/fertilizer-info/<fertilizer_name>', methods=['GET'])
def api_get_fertilizer_info(fertilizer_name):
    try:
        info = get_fertilizer_info(fertilizer_name)
        if info:
            return jsonify({'success': True, 'fertilizer': fertilizer_name, 'info': info})
        else:
            return jsonify({'success': False, 'error': 'Fertilizer not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Identify Crop from Image and Recommend Fertilizer
@app.route('/api/fertilizer-from-image', methods=['POST'])
def api_fertilizer_from_image():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if file is image
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
        if not any(file.filename.lower().endswith('.' + ext) for ext in allowed_extensions):
            return jsonify({'success': False, 'error': 'Only image files are supported'}), 400
        
        # Read image data
        image_data = file.read()
        
        # Identify crop from image
        crop_identification = identify_crop_from_image(image_data)
        
        if not crop_identification.get('success'):
            return jsonify(crop_identification), 400
        
        identified_crop = crop_identification['crop']
        
        # Get default nutrients for identified crop
        default_nutrients = get_crop_default_nutrients(identified_crop)
        
        # Get fertilizer recommendation
        recommendation = recommend_fertilizer(
            identified_crop,
            default_nutrients['nitrogen'],
            default_nutrients['phosphorus'],
            default_nutrients['potassium']
        )
        
        if not recommendation.get('success'):
            return jsonify(recommendation), 400
        
        return jsonify({
            'success': True,
            'crop_identification': crop_identification,
            'fertilizer_recommendation': recommendation,
            'default_nutrients': default_nutrients,
            'summary': f"Identified {identified_crop} from image. Recommended fertilizer: {recommendation['primary_recommendation']['fertilizer']}",
            'note': 'Crop identified using color analysis. For accurate results, add your GEMINI_API_KEY in backend/.env' if crop_identification.get('method') == 'color_heuristic' else None
        })
    
    except Exception as e:
        print(f"Error in fertilizer from image: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ===============================================================================================
# WEATHER & ALERTS API ENDPOINTS
# ===============================================================================================

# API: Get Weather and Alerts for a Location
@app.route('/api/weather', methods=['POST'])
def api_get_weather():
    try:
        data = request.get_json()
        city = data.get('city', 'Delhi')
        
        # Fetch weather data
        temperature, humidity = weather_fetch(city)
        
        # Get rainfall and wind speed (mock data for now)
        rainfall = data.get('rainfall', 50)
        wind_speed = data.get('wind_speed', 20)
        
        # Get weather alerts
        alerts = get_weather_alerts(temperature, humidity, rainfall, wind_speed)
        
        # Get weather summary
        summary = get_weather_summary(temperature, humidity, rainfall, wind_speed)
        
        return jsonify({
            'success': True,
            'city': city,
            'weather': summary,
            'alerts': alerts,
            'alerts_count': len(alerts)
        })
    
    except Exception as e:
        print(f"Error in weather API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get Crop-Specific Weather Alerts
@app.route('/api/weather-alerts/<crop>', methods=['POST'])
def api_get_crop_alerts(crop):
    try:
        data = request.get_json()
        city = data.get('city', 'Delhi')
        
        # Fetch weather data
        temperature, humidity = weather_fetch(city)
        
        # Get rainfall and wind speed (mock data for now)
        rainfall = data.get('rainfall', 50)
        wind_speed = data.get('wind_speed', 20)
        
        # Get crop-specific alerts
        crop_alerts = get_crop_specific_alerts(crop, temperature, humidity, rainfall)
        
        # Get general alerts
        general_alerts = get_weather_alerts(temperature, humidity, rainfall, wind_speed)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'city': city,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'wind_speed': wind_speed,
            'crop_specific_alerts': crop_alerts,
            'general_alerts': general_alerts,
            'total_alerts': len(crop_alerts) + len(general_alerts)
        })
    
    except Exception as e:
        print(f"Error in crop alerts API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ===============================================================================================
# SMART REMINDERS API ENDPOINTS
# ===============================================================================================

# API: Add a new crop and create reminders
@app.route('/api/reminders/add-crop', methods=['POST'])
def api_add_crop():
    try:
        data = request.get_json()
        
        farmer_id = data.get('farmer_id', 'default_farmer')
        crop_name = data.get('crop_name')
        planting_date = data.get('planting_date')
        field_name = data.get('field_name', 'Field 1')
        area_acres = data.get('area_acres', 1)
        
        if not crop_name or not planting_date:
            return jsonify({'success': False, 'error': 'Crop name and planting date required'}), 400
        
        # Add crop
        crop = add_crop(farmer_id, crop_name, planting_date, field_name, area_acres)
        
        # Get lifecycle tasks
        tasks = get_tasks_for_crop(crop_name)
        if not tasks:
            return jsonify({'success': False, 'error': f'No lifecycle defined for {crop_name}'}), 400
        
        # Create reminders
        reminders = create_reminders_for_crop(crop['id'], tasks)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'reminders_created': len(reminders),
            'message': f'Crop {crop_name} added! {len(reminders)} reminders scheduled.'
        })
    
    except Exception as e:
        print(f"Error adding crop: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get farmer's crops
@app.route('/api/reminders/crops/<farmer_id>', methods=['GET'])
def api_get_crops(farmer_id):
    try:
        crops = get_farmer_crops(farmer_id)
        
        # Add statistics to each crop
        crops_with_stats = []
        for crop in crops:
            stats = get_crop_statistics(crop['id'])
            crop['statistics'] = stats
            crops_with_stats.append(crop)
        
        return jsonify({
            'success': True,
            'farmer_id': farmer_id,
            'crops': crops_with_stats,
            'total_crops': len(crops)
        })
    
    except Exception as e:
        print(f"Error getting crops: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get crop details
@app.route('/api/reminders/crop/<crop_id>', methods=['GET'])
def api_get_crop(crop_id):
    try:
        crop = get_crop_by_id(crop_id)
        if not crop:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        stats = get_crop_statistics(crop_id)
        photos = get_crop_photos(crop_id)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'statistics': stats,
            'photos_count': len(photos)
        })
    
    except Exception as e:
        print(f"Error getting crop: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get today's reminders
@app.route('/api/reminders/today/<crop_id>', methods=['GET'])
def api_get_today_reminders(crop_id):
    try:
        reminders = get_today_reminders(crop_id)
        
        return jsonify({
            'success': True,
            'crop_id': crop_id,
            'reminders': reminders,
            'count': len(reminders)
        })
    
    except Exception as e:
        print(f"Error getting today's reminders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get upcoming reminders
@app.route('/api/reminders/upcoming/<crop_id>', methods=['GET'])
def api_get_upcoming_reminders(crop_id):
    try:
        days_ahead = request.args.get('days', 7, type=int)
        reminders = get_upcoming_reminders(crop_id, days_ahead)
        
        return jsonify({
            'success': True,
            'crop_id': crop_id,
            'days_ahead': days_ahead,
            'reminders': reminders,
            'count': len(reminders)
        })
    
    except Exception as e:
        print(f"Error getting upcoming reminders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get all reminders for a crop
@app.route('/api/reminders/all/<crop_id>', methods=['GET'])
def api_get_all_reminders(crop_id):
    try:
        reminders = get_crop_reminders(crop_id)
        progress = get_reminder_progress(crop_id)
        
        return jsonify({
            'success': True,
            'crop_id': crop_id,
            'reminders': reminders,
            'progress': progress,
            'total': len(reminders)
        })
    
    except Exception as e:
        print(f"Error getting reminders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Mark reminder as complete
@app.route('/api/reminders/complete', methods=['POST'])
def api_complete_reminder():
    try:
        data = request.get_json()
        reminder_id = data.get('reminder_id')
        notes = data.get('notes', '')
        
        if not reminder_id:
            return jsonify({'success': False, 'error': 'Reminder ID required'}), 400
        
        reminder = mark_reminder_complete(reminder_id, notes)
        
        if not reminder:
            return jsonify({'success': False, 'error': 'Reminder not found'}), 404
        
        return jsonify({
            'success': True,
            'reminder': reminder,
            'message': 'Reminder marked as complete!'
        })
    
    except Exception as e:
        print(f"Error completing reminder: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Upload crop photo
@app.route('/api/reminders/upload-photo/<crop_id>', methods=['POST'])
def api_upload_photo(crop_id):
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check if file is image
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
        if not any(file.filename.lower().endswith('.' + ext) for ext in allowed_extensions):
            return jsonify({'success': False, 'error': 'Only image files are supported'}), 400
        
        notes = request.form.get('notes', '')
        
        # Read image data
        image_data = file.read()
        
        # Add photo to database
        photo = add_photo(crop_id, file.filename, image_data.hex(), notes)
        
        # Analyze photo for disease
        try:
            prediction = predict_image(image_data, disease_model)
            disease_info = disease_dic.get(prediction, 'Disease not found')
            
            analysis = {
                'disease': prediction,
                'info': disease_info,
                'healthy': 'healthy' in prediction.lower()
            }
            
            update_photo_analysis(photo['id'], analysis)
            photo['analysis'] = analysis
        except Exception as e:
            print(f"Error analyzing photo: {e}")
        
        return jsonify({
            'success': True,
            'photo': photo,
            'message': 'Photo uploaded and analyzed!'
        })
    
    except Exception as e:
        print(f"Error uploading photo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get crop photos
@app.route('/api/reminders/photos/<crop_id>', methods=['GET'])
def api_get_photos(crop_id):
    try:
        photos = get_photo_timeline(crop_id)
        
        return jsonify({
            'success': True,
            'crop_id': crop_id,
            'photos': photos,
            'count': len(photos)
        })
    
    except Exception as e:
        print(f"Error getting photos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get crop statistics
@app.route('/api/reminders/stats/<crop_id>', methods=['GET'])
def api_get_stats(crop_id):
    try:
        stats = get_crop_statistics(crop_id)
        
        if not stats:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get available crops for lifecycle
@app.route('/api/reminders/available-crops', methods=['GET'])
def api_get_available_crops():
    try:
        crops = get_all_crops_with_lifecycle()
        
        crop_info = []
        for crop in crops:
            lifecycle = get_crop_lifecycle(crop)
            crop_info.append({
                'name': crop,
                'duration_days': lifecycle['duration_days'],
                'season': lifecycle['season'],
                'tasks_count': len(lifecycle['tasks'])
            })
        
        return jsonify({
            'success': True,
            'crops': crop_info,
            'total': len(crop_info)
        })
    
    except Exception as e:
        print(f"Error getting available crops: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ===============================================================================================
# SMART NOTIFICATIONS API ENDPOINTS
# ===============================================================================================

# API: Get personalized reminder notification
@app.route('/api/reminders/notification/<reminder_id>', methods=['POST'])
def api_get_notification(reminder_id):
    try:
        data = request.get_json()
        farmer_name = data.get('farmer_name', 'Farmer')
        
        # Find the reminder
        reminders_data = _load_json('data/reminders/reminders.json') if os.path.exists('data/reminders/reminders.json') else {}
        
        reminder = None
        crop_id = None
        for cid, reminders_list in reminders_data.items():
            for r in reminders_list:
                if r['id'] == reminder_id:
                    reminder = r
                    crop_id = cid
                    break
        
        if not reminder:
            return jsonify({'success': False, 'error': 'Reminder not found'}), 404
        
        crop = get_crop_by_id(crop_id)
        if not crop:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        # Generate personalized notification
        notification = format_notification(reminder, farmer_name, crop['crop_name'])
        
        return jsonify({
            'success': True,
            'notification': notification,
            'crop': crop['crop_name'],
            'farmer_name': farmer_name
        })
    
    except Exception as e:
        print(f"Error getting notification: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get crop stage message
@app.route('/api/reminders/crop-stage/<crop_id>', methods=['POST'])
def api_get_crop_stage(crop_id):
    try:
        data = request.get_json()
        farmer_name = data.get('farmer_name', 'Farmer')
        
        crop = get_crop_by_id(crop_id)
        if not crop:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        days_elapsed = get_days_elapsed(crop_id)
        stage_message = generate_crop_stage_message(farmer_name, crop['crop_name'], days_elapsed)
        
        return jsonify({
            'success': True,
            'stage_message': stage_message,
            'days_elapsed': days_elapsed,
            'crop': crop['crop_name']
        })
    
    except Exception as e:
        print(f"Error getting crop stage: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get encouragement message
@app.route('/api/reminders/encouragement/<crop_id>', methods=['POST'])
def api_get_encouragement(crop_id):
    try:
        data = request.get_json()
        farmer_name = data.get('farmer_name', 'Farmer')
        
        crop = get_crop_by_id(crop_id)
        if not crop:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        progress = get_reminder_progress(crop_id)
        encouragement = generate_encouragement_message(
            farmer_name,
            crop['crop_name'],
            progress['percentage']
        )
        
        return jsonify({
            'success': True,
            'encouragement': encouragement,
            'progress': progress
        })
    
    except Exception as e:
        print(f"Error getting encouragement: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get all notifications for today
@app.route('/api/reminders/notifications-today/<crop_id>', methods=['POST'])
def api_get_notifications_today(crop_id):
    try:
        data = request.get_json()
        farmer_name = data.get('farmer_name', 'Farmer')
        
        crop = get_crop_by_id(crop_id)
        if not crop:
            return jsonify({'success': False, 'error': 'Crop not found'}), 404
        
        # Get today's reminders
        today_reminders = get_today_reminders(crop_id)
        
        # Format each reminder as notification
        notifications = []
        for reminder in today_reminders:
            notification = format_notification(reminder, farmer_name, crop['crop_name'])
            notifications.append(notification)
        
        # Get crop stage
        days_elapsed = get_days_elapsed(crop_id)
        stage_message = generate_crop_stage_message(farmer_name, crop['crop_name'], days_elapsed)
        
        # Get progress
        progress = get_reminder_progress(crop_id)
        
        return jsonify({
            'success': True,
            'notifications': notifications,
            'stage_message': stage_message,
            'progress': progress,
            'total_notifications': len(notifications),
            'crop': crop['crop_name'],
            'farmer_name': farmer_name
        })
    
    except Exception as e:
        print(f"Error getting today's notifications: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# Helper function to load JSON
def _load_json(filepath):
    """Load JSON file"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

# ===============================================================================================
# VOICE ASSISTANT API ENDPOINTS
# ===============================================================================================

# API: Process voice question
@app.route('/api/voice-assistant/ask', methods=['POST'])
def api_voice_assistant_ask():
    try:
        data = request.get_json()
        question = data.get('question', '')
        crop_name = data.get('crop_name', '')
        location = data.get('location', '')
        
        if not question:
            return jsonify({'success': False, 'error': 'Question is required'}), 400
        
        # Build context
        context = ''
        if crop_name:
            context += f"Crop: {crop_name}. "
        if location:
            context += f"Location: {location}."
        
        # Process question using Gemini AI
        result = process_farming_question(question, context if context else None)
        
        return jsonify({
            'success': result.get('success', False),
            'question': question,
            'answer_en': result.get('answer_en', ''),
            'answer_hi': result.get('answer_hi', ''),
            'error': result.get('error', '')
        })
    
    except Exception as e:
        print(f"Error in voice assistant: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get quick answers
@app.route('/api/voice-assistant/quick-answer/<question_type>', methods=['GET'])
def api_get_quick_answer(question_type):
    try:
        answer = get_quick_answers(question_type)
        
        if answer:
            return jsonify({
                'success': True,
                'question_type': question_type,
                'answer_en': answer['en'],
                'answer_hi': answer['hi']
            })
        else:
            return jsonify({'success': False, 'error': 'Question type not found'}), 404
    
    except Exception as e:
        print(f"Error getting quick answer: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# API: Get crop-specific advice
@app.route('/api/voice-assistant/crop-advice/<crop_name>/<question_type>', methods=['GET'])
def api_get_crop_advice(crop_name, question_type):
    try:
        advice = get_crop_specific_advice(crop_name, question_type)
        
        if advice:
            return jsonify({
                'success': True,
                'crop': crop_name,
                'question_type': question_type,
                'advice': advice
            })
        else:
            return jsonify({'success': False, 'error': 'Advice not found'}), 404
    
    except Exception as e:
        print(f"Error getting crop advice: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ===============================================================================================
# UNIFIED CHATBOT API ENDPOINTS
# ===============================================================================================

# API: Unified Chatbot
@app.route('/api/chatbot/message', methods=['POST'])
def api_chatbot_message():
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        attachments = data.get('attachments', [])
        
        # Process attachments if any
        extracted_text = ""
        if attachments:
            for attachment in attachments:
                att_type = attachment.get('type', '')
                att_data = attachment.get('data', '')
                
                if att_type == 'image' and att_data:
                    try:
                        # Extract image data (base64)
                        import base64
                        from io import BytesIO
                        from PIL import Image
                        
                        # Remove data URL prefix if present
                        if ',' in att_data:
                            att_data = att_data.split(',')[1]
                        
                        image_bytes = base64.b64decode(att_data)
                        image = Image.open(BytesIO(image_bytes))
                        
                        # Extract text from image
                        from utils.image_extractor import extract_text_from_image
                        text = extract_text_from_image(image)
                        if text:
                            extracted_text += f"\n[Image: {attachment.get('name', 'image')}]\n{text}"
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        extracted_text += f"\n[Could not read image: {attachment.get('name', 'image')}]"
                
                elif att_type == 'pdf' and att_data:
                    try:
                        # Extract PDF data (base64)
                        import base64
                        from io import BytesIO
                        import PyPDF2
                        
                        # Remove data URL prefix if present
                        if ',' in att_data:
                            att_data = att_data.split(',')[1]
                        
                        pdf_bytes = base64.b64decode(att_data)
                        pdf_file = BytesIO(pdf_bytes)
                        
                        # Extract text from PDF
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        
                        if text:
                            extracted_text += f"\n[PDF: {attachment.get('name', 'document')}]\n{text}"
                    except Exception as e:
                        print(f"Error processing PDF: {e}")
                        extracted_text += f"\n[Could not read PDF: {attachment.get('name', 'document')}]"
        
        # Combine message with extracted text
        full_message = message
        if extracted_text:
            full_message = f"{message}\n\n[Attached Files Content]:{extracted_text}" if message else f"[Attached Files Content]:{extracted_text}"
        
        if not full_message.strip():
            return jsonify({'success': False, 'error': 'Message or attachments required'}), 400
        
        # Process message
        result = process_unified_chat(full_message, conversation_history)
        
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'response': result.get('response', ''),
            'language': result.get('language', 'en'),
            'feature': result.get('feature', 'general_advice'),
            'error': result.get('error', '')
        })
    
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

# ===============================================================================================
# AUTHENTICATION ENDPOINTS
# ===============================================================================================

from utils.auth_mongo import (
    register_user, login_user, verify_token, get_user_by_id,
    update_user_profile, change_password, reset_password
)

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """Register a new farmer"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        mobile = data.get('mobile', '').strip()
        agriculture_type = data.get('agriculture_type', '').strip()
        password = data.get('password', '')
        
        success, result = register_user(name, email, mobile, agriculture_type, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': result.get('message'),
                'user_id': result.get('user_id'),
                'token': result.get('token'),
                'name': result.get('name')
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
    
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Login farmer"""
    try:
        data = request.get_json()
        
        mobile = data.get('mobile', '').strip()
        password = data.get('password', '')
        
        success, result = login_user(mobile, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': result.get('message'),
                'user_id': result.get('user_id'),
                'token': result.get('token'),
                'name': result.get('name'),
                'email': result.get('email'),
                'agriculture_type': result.get('agriculture_type')
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 401
    
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/verify-token', methods=['POST'])
def api_verify_token():
    """Verify authentication token"""
    try:
        data = request.get_json()
        token = data.get('token', '')
        
        if not token:
            return jsonify({'success': False, 'error': 'Token required'}), 400
        
        is_valid, user = verify_token(token)
        
        if is_valid:
            return jsonify({
                'success': True,
                'user_id': str(user.get('_id')),
                'name': user.get('name'),
                'email': user.get('email'),
                'mobile': user.get('mobile'),
                'agriculture_type': user.get('agriculture_type')
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
    
    except Exception as e:
        print(f"Token verification error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/profile/<user_id>', methods=['GET'])
def api_get_profile(user_id):
    """Get user profile"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user_id': str(user.get('_id')),
            'name': user.get('name'),
            'email': user.get('email'),
            'mobile': user.get('mobile'),
            'agriculture_type': user.get('agriculture_type'),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None,
            'last_login': user.get('last_login').isoformat() if user.get('last_login') else None,
            'profile_complete': user.get('profile_complete')
        }), 200
    
    except Exception as e:
        print(f"Get profile error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/profile/<user_id>', methods=['PUT'])
def api_update_profile(user_id):
    """Update user profile"""
    try:
        data = request.get_json()
        
        success, message = update_user_profile(user_id, **data)
        
        if success:
            user = get_user_by_id(user_id)
            return jsonify({
                'success': True,
                'message': message,
                'user': {
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'agriculture_type': user.get('agriculture_type')
                }
            }), 200
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/change-password', methods=['POST'])
def api_change_password():
    """Change user password"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        success, message = change_password(user_id, old_password, new_password)
        
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        print(f"Change password error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    """Reset password (forgot password)"""
    try:
        data = request.get_json()
        
        mobile = data.get('mobile', '').strip()
        new_password = data.get('new_password', '')
        
        success, message = reset_password(mobile, new_password)
        
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'error': message}), 400
    
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ===============================================================================================

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
