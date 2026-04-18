"""
Voice-based AI Assistant for farmers
Handles voice input, processes questions, and provides voice output
"""

from utils.gemini_helper import generate_crop_explanation
import google.generativeai as genai
import os

def get_gemini_api_key():
    """Get Gemini API key from environment"""
    return os.getenv('GEMINI_API_KEY', '')

def process_farming_question(question, context=None):
    """
    Process a farming question using Gemini AI
    
    Args:
        question: Farmer's question (in Hindi/English)
        context: Optional context (crop name, location, etc.)
    
    Returns:
        Answer in both Hindi and English
    """
    
    try:
        api_key = get_gemini_api_key()
        if not api_key:
            return {
                'success': False,
                'error': 'Gemini API key not configured',
                'answer_en': 'Sorry, AI assistant is not configured.',
                'answer_hi': 'Maaf kijiye, AI assistant configure nahi hai.'
            }
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Build context-aware prompt
        system_prompt = """You are a helpful farming assistant for Indian farmers. 
        Answer farming questions in a simple, practical way.
        Provide answers in both English and Hindi/Hinglish.
        
        Format your response as:
        ENGLISH: [Answer in English]
        HINDI: [Answer in Hindi/Hinglish]
        """
        
        if context:
            system_prompt += f"\nContext: {context}"
        
        full_prompt = f"{system_prompt}\n\nFarmer's Question: {question}"
        
        response = model.generate_content(full_prompt)
        
        if response.text:
            # Parse response
            text = response.text
            
            # Extract English and Hindi parts
            answer_en = text
            answer_hi = text
            
            if 'ENGLISH:' in text and 'HINDI:' in text:
                parts = text.split('HINDI:')
                answer_en = parts[0].replace('ENGLISH:', '').strip()
                answer_hi = parts[1].strip()
            
            return {
                'success': True,
                'question': question,
                'answer_en': answer_en,
                'answer_hi': answer_hi,
                'context': context
            }
        else:
            return {
                'success': False,
                'error': 'No response from AI',
                'answer_en': 'Sorry, I could not generate an answer.',
                'answer_hi': 'Maaf kijiye, mujhe jawab nahi mil saka.'
            }
    
    except Exception as e:
        print(f"Error processing question: {e}")
        return {
            'success': False,
            'error': str(e),
            'answer_en': 'Sorry, there was an error processing your question.',
            'answer_hi': 'Maaf kijiye, aapke sawaal ko process karte samay error aaya.'
        }

def get_quick_answers(question_type):
    """Get quick answers for common farming questions"""
    
    quick_answers = {
        'watering': {
            'en': 'Water your crops early morning or late evening. Check soil moisture before watering. Most crops need 1-2 inches of water per week.',
            'hi': 'Apne fasal ko subah jaldi ya shaam ko paani dein. Paani dene se pehle mitti ki nammi check karein. Zyada tar faslein 1-2 inch paani per hafte chahti hain.'
        },
        'fertilizer': {
            'en': 'Use balanced fertilizer (NPK) for most crops. Apply during growing season. Follow package instructions for dosage.',
            'hi': 'Zyada tar faslein ke liye balanced khad (NPK) use karein. Growing season mein apply karein. Dosage ke liye package instructions follow karein.'
        },
        'pest_control': {
            'en': 'Monitor crops regularly for pests. Use organic methods first (neem oil, soap spray). Use pesticides only if necessary.',
            'hi': 'Apni faslein ko regularly keede ke liye check karein. Pehle organic methods use karein (neem ka tel, soap spray). Pesticide sirf zaroori ho to use karein.'
        },
        'disease': {
            'en': 'Remove infected leaves immediately. Improve air circulation. Use fungicide if needed. Consult local agricultural officer.',
            'hi': 'Infected patte ko turant nikaal dein. Hawa ka sangchar badhayein. Zaroori ho to fungicide use karein. Local agricultural officer se salah lein.'
        },
        'harvest': {
            'en': 'Harvest when crop is fully mature. Check color and firmness. Harvest early morning for best quality.',
            'hi': 'Jab fasal bilkul paak jaye tab kaatein. Rang aur firmness check karein. Sabse achha quality ke liye subah jaldi kaatein.'
        }
    }
    
    return quick_answers.get(question_type.lower(), None)

def get_crop_specific_advice(crop_name, question_type):
    """Get crop-specific advice"""
    
    crop_advice = {
        'moong': {
            'watering': 'Moong needs moderate watering. Water every 7-10 days. Avoid waterlogging.',
            'fertilizer': 'Moong needs nitrogen and phosphorus. Apply 20kg nitrogen per acre.',
            'pest_control': 'Watch for spider mites and pod borers. Use neem oil spray.',
            'harvest': 'Harvest moong when pods turn brown. Yield: 8-10 quintals per acre.'
        },
        'rice': {
            'watering': 'Rice needs standing water. Maintain 5-10cm water level throughout growing season.',
            'fertilizer': 'Rice needs high nitrogen. Apply 60kg nitrogen per acre in splits.',
            'pest_control': 'Watch for stem borers and leaf folders. Use pheromone traps.',
            'harvest': 'Harvest rice when 80% grains are golden. Yield: 40-50 quintals per acre.'
        },
        'wheat': {
            'watering': 'Wheat needs 4-5 irrigations. First irrigation at 21 days after sowing.',
            'fertilizer': 'Wheat needs 60kg nitrogen per acre. Apply in 2-3 splits.',
            'pest_control': 'Watch for armyworms and Hessian flies. Use recommended pesticides.',
            'harvest': 'Harvest wheat when grains are hard. Yield: 40-50 quintals per acre.'
        }
    }
    
    crop_lower = crop_name.lower()
    if crop_lower in crop_advice:
        return crop_advice[crop_lower].get(question_type.lower(), None)
    
    return None

def format_voice_response(answer_en, answer_hi):
    """Format response for voice output"""
    return {
        'text_en': answer_en,
        'text_hi': answer_hi,
        'audio_text_en': answer_en,  # This will be converted to audio by frontend
        'audio_text_hi': answer_hi
    }
