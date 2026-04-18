import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    print("✅ Gemini API configured successfully!")
else:
    print("⚠️ GEMINI_API_KEY not found in .env file")
    model = None


def generate_crop_explanation(crop_name, N, P, K, temperature, humidity, ph, rainfall):
    """
    Generate explanation for crop recommendation using Gemini API
    """
    if not model:
        return get_default_explanation(crop_name)
    
    try:
        prompt = f"""
        I recommended {crop_name} as the best crop for the following soil and weather conditions:
        - Nitrogen (N): {N} mg/kg
        - Phosphorus (P): {P} mg/kg
        - Potassium (K): {K} mg/kg
        - Temperature: {temperature}°C
        - Humidity: {humidity}%
        - pH: {ph}
        - Rainfall: {rainfall} mm
        
        Please provide a brief, simple explanation (2-3 sentences) in Hindi and English about:
        1. Why {crop_name} is suitable for these conditions
        2. Key benefits of growing {crop_name}
        3. Simple care tips
        
        Format the response as:
        ENGLISH: [explanation in English]
        HINDI: [explanation in Hindi]
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return get_default_explanation(crop_name)


def get_default_explanation(crop_name):
    """
    Default explanation if Gemini API fails
    """
    explanations = {
        'rice': {
            'english': f'{crop_name} is ideal for your soil conditions. It requires moderate nitrogen and good moisture. Ensure proper water management for best yield.',
            'hindi': f'{crop_name} आपकी मिट्टी के लिए आदर्श है। इसे मध्यम नाइट्रोजन और अच्छी नमी की आवश्यकता है। सर्वोत्तम उपज के लिए जल प्रबंधन सुनिश्चित करें।'
        },
        'wheat': {
            'english': f'{crop_name} thrives in cool weather with moderate rainfall. Your soil pH is suitable for this crop. Apply balanced fertilizer for optimal growth.',
            'hindi': f'{crop_name} ठंडे मौसम में अच्छी तरह बढ़ता है। आपकी मिट्टी इस फसल के लिए उपयुक्त है। इष्टतम वृद्धि के लिए संतुलित खाद लागू करें।'
        },
        'maize': {
            'english': f'{crop_name} requires good drainage and moderate nutrients. Your conditions are favorable. Ensure timely irrigation during critical growth stages.',
            'hindi': f'{crop_name} को अच्छी जल निकासी और मध्यम पोषक तत्वों की आवश्यकता है। आपकी स्थितियां अनुकूल हैं। महत्वपूर्ण वृद्धि चरणों के दौरान समय पर सिंचाई सुनिश्चित करें।'
        },
        'cotton': {
            'english': f'{crop_name} is well-suited to your soil and climate. It requires good potassium levels. Monitor for pests and provide adequate water during flowering.',
            'hindi': f'{crop_name} आपकी मिट्टी और जलवायु के लिए उपयुक्त है। इसे अच्छे पोटेशियम स्तर की आवश्यकता है। कीटों की निगरानी करें और फूल आने के दौरान पर्याप्त पानी दें।'
        },
        'coffee': {
            'english': f'{crop_name} thrives in your climate conditions. It prefers slightly acidic soil which matches your pH. Provide shade and maintain consistent moisture.',
            'hindi': f'{crop_name} आपकी जलवायु परिस्थितियों में पनपता है। यह थोड़ी अम्लीय मिट्टी पसंद करता है जो आपके pH से मेल खाता है। छाया प्रदान करें और नमी को सुसंगत रखें।'
        }
    }
    
    crop_lower = crop_name.lower()
    if crop_lower in explanations:
        exp = explanations[crop_lower]
        return f"ENGLISH: {exp['english']}\nHINDI: {exp['hindi']}"
    else:
        return f"ENGLISH: {crop_name} is recommended for your soil and weather conditions. Follow standard agricultural practices for best results.\nHINDI: आपकी मिट्टी और मौसम की स्थितियों के लिए {crop_name} की सिफारिश की जाती है। सर्वोत्तम परिणामों के लिए मानक कृषि प्रथाओं का पालन करें।"


def generate_fertilizer_explanation(crop_name, deficiency, recommendation):
    """
    Generate explanation for fertilizer recommendation using Gemini API
    """
    if not model:
        return recommendation
    
    try:
        prompt = f"""
        For {crop_name} crop, the soil has {deficiency} deficiency.
        
        Please provide a brief, practical explanation (2-3 sentences) in Hindi and English about:
        1. Why this deficiency is important
        2. How to address it
        3. Expected benefits
        
        Format the response as:
        ENGLISH: [explanation]
        HINDI: [explanation]
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating fertilizer explanation: {e}")
        return recommendation
