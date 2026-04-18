import PyPDF2
import re
from typing import Dict, Optional

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_soil_parameters(text: str) -> Dict[str, Optional[float]]:
    """
    Extract soil parameters from PDF text using regex patterns
    Looks for: Nitrogen (N), Phosphorus (P), Potassium (K), pH, etc.
    """
    parameters = {
        'nitrogen': None,
        'phosphorus': None,
        'potassium': None,
        'ph': None,
        'temperature': None,
        'humidity': None,
        'rainfall': None,
        'organic_matter': None,
        'ec': None  # Electrical Conductivity
    }
    
    text_lower = text.lower()
    
    # Nitrogen patterns
    nitrogen_patterns = [
        r'nitrogen\s*\(n\)[:\s]+(\d+\.?\d*)',
        r'nitrogen[:\s]+(\d+\.?\d*)',
        r'(?:total\s+)?nitrogen[:\s]+(\d+\.?\d*)',
        r'n\s*\(mg/kg\)[:\s]+(\d+\.?\d*)',
        r'(?:^|\s)n[:\s]+(\d+\.?\d*)',
    ]
    for pattern in nitrogen_patterns:
        match = re.search(pattern, text_lower, re.MULTILINE)
        if match:
            parameters['nitrogen'] = float(match.group(1))
            break
    
    # Phosphorus patterns
    phosphorus_patterns = [
        r'phosphorus[:\s]+(\d+\.?\d*)',
        r'phosphorus\s*\(p\)[:\s]+(\d+\.?\d*)',
        r'(?:available\s+)?phosphorus[:\s]+(\d+\.?\d*)',
        r'p\s*\(mg/kg\)[:\s]+(\d+\.?\d*)',
        r'(?:^|\s)p[:\s]+(\d+\.?\d*)',
    ]
    for pattern in phosphorus_patterns:
        match = re.search(pattern, text_lower, re.MULTILINE)
        if match:
            parameters['phosphorus'] = float(match.group(1))
            break
    
    # Potassium patterns
    potassium_patterns = [
        r'potassium[:\s]+(\d+\.?\d*)',
        r'potassium\s*\(k\)[:\s]+(\d+\.?\d*)',
        r'(?:available\s+)?potassium[:\s]+(\d+\.?\d*)',
        r'k\s*\(mg/kg\)[:\s]+(\d+\.?\d*)',
        r'(?:^|\s)k[:\s]+(\d+\.?\d*)',
    ]
    for pattern in potassium_patterns:
        match = re.search(pattern, text_lower, re.MULTILINE)
        if match:
            parameters['potassium'] = float(match.group(1))
            break
    
    # pH patterns
    ph_patterns = [
        r'ph[:\s]+(\d+\.?\d*)',
        r'soil\s+ph[:\s]+(\d+\.?\d*)',
        r'ph\s+value[:\s]+(\d+\.?\d*)',
    ]
    for pattern in ph_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['ph'] = float(match.group(1))
            break
    
    # Temperature patterns
    temp_patterns = [
        r'temperature[:\s]+(\d+\.?\d*)',
        r'temp[:\s]+(\d+\.?\d*)',
        r'temperature\s*\(°?c\)[:\s]+(\d+\.?\d*)',
    ]
    for pattern in temp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['temperature'] = float(match.group(1))
            break
    
    # Humidity patterns
    humidity_patterns = [
        r'humidity[:\s]+(\d+\.?\d*)',
        r'moisture[:\s]+(\d+\.?\d*)',
        r'humidity\s*\(%\)[:\s]+(\d+\.?\d*)',
    ]
    for pattern in humidity_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['humidity'] = float(match.group(1))
            break
    
    # Rainfall patterns
    rainfall_patterns = [
        r'rainfall[:\s]+(\d+\.?\d*)',
        r'rain[:\s]+(\d+\.?\d*)',
        r'rainfall\s*\(mm\)[:\s]+(\d+\.?\d*)',
    ]
    for pattern in rainfall_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['rainfall'] = float(match.group(1))
            break
    
    # Organic Matter patterns
    om_patterns = [
        r'organic\s+matter[:\s]+(\d+\.?\d*)',
        r'o\.m[:\s]+(\d+\.?\d*)',
        r'organic\s+carbon[:\s]+(\d+\.?\d*)',
    ]
    for pattern in om_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['organic_matter'] = float(match.group(1))
            break
    
    # EC (Electrical Conductivity) patterns
    ec_patterns = [
        r'ec[:\s]+(\d+\.?\d*)',
        r'electrical\s+conductivity[:\s]+(\d+\.?\d*)',
        r'e\.c[:\s]+(\d+\.?\d*)',
    ]
    for pattern in ec_patterns:
        match = re.search(pattern, text_lower)
        if match:
            parameters['ec'] = float(match.group(1))
            break
    
    return parameters


def validate_extracted_parameters(params: Dict[str, Optional[float]]) -> Dict[str, Optional[float]]:
    """
    Validate extracted parameters and fill missing ones with defaults if needed
    """
    # Define reasonable ranges for each parameter
    ranges = {
        'nitrogen': (0, 500),
        'phosphorus': (0, 500),
        'potassium': (0, 500),
        'ph': (3, 10),
        'temperature': (-10, 50),
        'humidity': (0, 100),
        'rainfall': (0, 5000),
    }
    
    validated = {}
    for key, value in params.items():
        if value is not None and key in ranges:
            min_val, max_val = ranges[key]
            if min_val <= value <= max_val:
                validated[key] = value
            else:
                validated[key] = None
        else:
            validated[key] = value
    
    return validated
