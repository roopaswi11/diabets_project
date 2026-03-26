from utils.ocr_reader import extract_text, extract_sugar_values

# Read text from image
text = extract_text("test_report.png")

print("OCR TEXT:")
print(text)

# Extract sugar values
fasting, pp, hba1c = extract_sugar_values(text)

print("\nDetected Values:")
print("Fasting Sugar:", fasting)
print("PP Sugar:", pp)
print("HbA1c:", hba1c)