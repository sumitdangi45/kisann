"""
Unified Chatbot for KisanSathi
Handles all features through conversational interface
Auto-detects language and feature requests
Supports both Gemini and ChatGPT APIs
"""

import google.generativeai as genai
import openai
import os
import re

def get_gemini_api_key():
    """Get Gemini API key"""
    return os.getenv('GEMINI_API_KEY', '')

def get_openai_api_key():
    """Get OpenAI API key"""
    return os.getenv('OPENAI_API_KEY', '')

def should_use_chatgpt():
    """Check if ChatGPT should be used"""
    return os.getenv('USE_CHATGPT', 'false').lower() == 'true'

def detect_language(text):
    """Detect if text is Hindi or English"""
    # Simple detection: if contains Devanagari script, it's Hindi
    hindi_pattern = re.compile(r'[\u0900-\u097F]')
    if hindi_pattern.search(text):
        return 'hi'
    return 'en'

def detect_feature_request(text):
    """Detect what feature farmer is asking for"""
    text_lower = text.lower()
    
    # Crop recommendation keywords
    if any(word in text_lower for word in ['crop', 'lagaun', 'lagayi', 'plant', 'kaunsi', 'kaun si', 'fasal', 'beej']):
        return 'crop_recommendation'
    
    # Fertilizer keywords
    if any(word in text_lower for word in ['fertilizer', 'khad', 'nutrient', 'nitrogen', 'phosphorus', 'potassium', 'npo']):
        return 'fertilizer'
    
    # Disease keywords
    if any(word in text_lower for word in ['disease', 'bimari', 'pest', 'keeda', 'insect', 'infected', 'spot', 'rot']):
        return 'disease'
    
    # Weather keywords
    if any(word in text_lower for word in ['weather', 'rain', 'barish', 'temperature', 'garmi', 'sardi', 'alert']):
        return 'weather'
    
    # Reminder/tracking keywords
    if any(word in text_lower for word in ['reminder', 'schedule', 'task', 'track', 'monitor', 'photo', 'progress']):
        return 'reminders'
    
    # General farming advice
    return 'general_advice'

def process_unified_chat(message, conversation_history=None):
    """
    Process chat message and return response
    Handles all features through conversational interface
    Supports both Gemini and ChatGPT APIs
    """
    
    try:
        # Check which API to use
        use_chatgpt = should_use_chatgpt()
        
        if use_chatgpt:
            return process_with_chatgpt(message, conversation_history)
        else:
            return process_with_gemini(message, conversation_history)
    
    except Exception as e:
        print(f"Error in unified chatbot: {e}")
        return {
            'success': False,
            'error': str(e),
            'response': 'Maaf kijiye, error aaya.'
        }

def process_with_chatgpt(message, conversation_history=None):
    """Process message using ChatGPT API"""
    try:
        api_key = get_openai_api_key()
        if not api_key:
            return {
                'success': False,
                'error': 'ChatGPT API not configured',
                'response': 'Maaf kijiye, ChatGPT configure nahi hai.'
            }
        
        openai.api_key = api_key
        
        # Detect language
        language = detect_language(message)
        
        # Detect feature
        feature = detect_feature_request(message)
        
        # Build system prompt
        system_prompt = get_system_prompt()
        
        # Build messages for ChatGPT
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for free tier, gpt-4 for paid
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        if response.choices and len(response.choices) > 0:
            return {
                'success': True,
                'message': message,
                'response': response.choices[0].message.content,
                'language': language,
                'feature': feature,
                'role': 'assistant'
            }
        else:
            return {
                'success': False,
                'error': 'No response generated',
                'response': 'Maaf kijiye, jawab generate nahi ho saka.'
            }
    
    except Exception as e:
        print(f"Error in ChatGPT: {e}")
        return {
            'success': False,
            'error': str(e),
            'response': 'Maaf kijiye, ChatGPT mein error aaya.'
        }

def process_with_gemini(message, conversation_history=None):
    """Process message using Gemini API"""
    try:
        api_key = get_gemini_api_key()
        if not api_key:
            return {
                'success': False,
                'error': 'Gemini API not configured',
                'response': 'Maaf kijiye, AI assistant configure nahi hai.'
            }
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Detect language
        language = detect_language(message)
        
        # Detect feature
        feature = detect_feature_request(message)
        
        # Build system prompt
        system_prompt = get_system_prompt()
        
        # Build conversation context
        messages = []
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    'role': msg['role'],
                    'parts': [msg['content']]
                })
        
        # Add current message
        messages.append({
            'role': 'user',
            'parts': [message]
        })
        
        # Build full prompt with system instruction
        full_prompt = f"{system_prompt}\n\n"
        for msg in messages:
            if msg['role'] == 'user':
                full_prompt += f"User: {msg['parts'][0]}\n"
            else:
                full_prompt += f"Assistant: {msg['parts'][0]}\n"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        if response.text:
            return {
                'success': True,
                'message': message,
                'response': response.text,
                'language': language,
                'feature': feature,
                'role': 'assistant'
            }
        else:
            return {
                'success': False,
                'error': 'No response generated',
                'response': 'Maaf kijiye, jawab generate nahi ho saka.'
            }
    
    except Exception as e:
        print(f"Error in Gemini: {e}")
        return {
            'success': False,
            'error': str(e),
            'response': 'Maaf kijiye, error aaya.'
        }

def get_system_prompt():
    """Get the system prompt for the chatbot"""
    return """You are KisanSathi, an AI farming assistant for Indian farmers.

You help farmers with:
1. Crop Recommendation - Suggest best crops based on soil, weather, season
2. Fertilizer Advice - Recommend fertilizers based on crop and soil
3. Disease Detection - Identify and treat crop diseases
4. Weather Alerts - Provide weather-based farming advice
5. Crop Tracking - Help track crop progress and schedule tasks
6. General Farming - Answer any farming question

IMPORTANT RULES:
- Respond in the SAME language as the farmer's input (Hindi or English)
- Be conversational and friendly
- Provide practical, actionable advice
- If farmer mentions a crop, remember it for context
- If farmer mentions location, remember it for weather advice
- Keep responses concise but helpful
- Use simple language that farmers understand

When farmer asks about:
- Crops: Suggest based on season, soil, water availability
- Fertilizer: Recommend specific products and quantities
- Diseases: Ask for symptoms, suggest treatment
- Weather: Provide farming recommendations based on weather
- Tracking: Help create schedule and reminders

Always be helpful and supportive."""
