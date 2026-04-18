"""
Test PDF upload and extraction
"""
from utils.pdf_extractor import extract_text_from_pdf, extract_soil_parameters, validate_extracted_parameters

# Test with the sample PDF
pdf_path = "sample_soil_report.pdf"

print("Testing PDF extraction...")
print("=" * 50)

# Extract text
text = extract_text_from_pdf(pdf_path)
print(f"Extracted text length: {len(text)} characters")
print(f"First 200 chars: {text[:200]}")
print()

# Extract parameters
params = extract_soil_parameters(text)
validated = validate_extracted_parameters(params)

print("Extracted Parameters:")
for key, value in validated.items():
    if value is not None:
        print(f"  {key}: {value}")
    else:
        print(f"  {key}: NOT FOUND")

print()
print("=" * 50)

# Check if we have all required parameters
required = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
missing = [p for p in required if validated.get(p) is None]

if missing:
    print(f"❌ Missing parameters: {missing}")
else:
    print("✅ All required parameters found!")
