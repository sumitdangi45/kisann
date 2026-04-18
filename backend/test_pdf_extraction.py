"""
Test script to verify PDF extraction functionality
"""
from utils.pdf_extractor import extract_soil_parameters

# Sample text that would be extracted from a soil report PDF
sample_pdf_text = """
SOIL TEST REPORT
================

Farmer Name: John Doe
Location: Maharashtra

SOIL PARAMETERS:
Nitrogen (N): 90 mg/kg
Phosphorus (P): 42 mg/kg
Potassium (K): 43 mg/kg
pH: 6.5
Temperature: 20°C
Humidity: 82%
Rainfall: 202 mm

Organic Matter: 2.5%
EC: 0.45 dS/m

RECOMMENDATIONS:
Based on the soil analysis, the following crops are recommended...
"""

# Test extraction
params = extract_soil_parameters(sample_pdf_text)
print("Extracted Parameters:")
for key, value in params.items():
    if value is not None:
        print(f"  {key}: {value}")
    else:
        print(f"  {key}: NOT FOUND")
