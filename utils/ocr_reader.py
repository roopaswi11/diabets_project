import pytesseract
import cv2
import numpy as np
import re
from pdf2image import convert_from_path
from docx import Document

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(path):

    img = cv2.imread(path)

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.threshold(
        blur,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    text = pytesseract.image_to_string(thresh)

    return text


def extract_text_from_pdf(path):

    images = convert_from_path(path)

    text = ""

    for img in images:

        img = np.array(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray,(5,5),0)

        thresh = cv2.threshold(
            blur,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        text += pytesseract.image_to_string(thresh)

    return text


def extract_text_from_docx(path):

    doc = Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_sugar_values(text):

    fasting = None
    pp = None
    hba1c = None

    fasting_match = re.search(r'fasting.*?(\d+)', text, re.IGNORECASE)

    if fasting_match:
        fasting = fasting_match.group(1)

    pp_match = re.search(r'(pp|postprandial).*?(\d+)', text, re.IGNORECASE)

    if pp_match:
        pp = pp_match.group(2)

    hba1c_match = re.search(r'hba1c.*?(\d+\.?\d*)', text, re.IGNORECASE)

    if hba1c_match:
        hba1c = hba1c_match.group(1)

    return fasting, pp, hba1c