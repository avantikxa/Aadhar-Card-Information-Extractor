import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
import re
import streamlit as st
from PIL import Image

# For local hosting, uncomment the below line and set your local Tesseract OCR engine path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'   #comment this line while hosting locally


def image_processing(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return threshold


def scan_detection(image):

    global document_contour

    document_contour = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


def extractText(ocr_text):
    ad_no = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', ocr_text)
    dob = re.search(r'\b\d{2}/\d{2}/\d{4}\b', ocr_text)
    gender = re.search(r'(Male|Female|MALE|FEMALE)', ocr_text)
    name = re.search(r'\b[A-Z][a-z]*(?:\s+[A-Z][a-z]*){1,3}\b', ocr_text)

    if name:
        st.write("Name:", name.group(0))
    else:
        st.write("Name not detected.")
    if ad_no:
        st.write("Aadhaar Number:", ad_no.group(0))
    else:
        st.write("Aadhaar number not detected.")
    if dob:
        dob = str(dob.group(0))
        dob = dob[:2] + "/" + dob[3:5] + "/" + dob[6:]
        st.write("DOB:", dob)
    else:
        st.write("DOB not detected.")
    if gender:
        st.write("Gender:", gender.group(0))
    else:
        st.write("Gender not detected.")


st.set_page_config(
page_title = 'Aadhaar Information Extractor',
layout = 'centered',
)
 
st.markdown("<h1 style='text-align: center; color: white;'>Aadhaar Card Information Extractor</h1>", unsafe_allow_html=True)
    
scale = 0.5

font = cv2.FONT_HERSHEY_SIMPLEX

input_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if input_image is not None:

    img = Image.open(input_image)
    img_array = np.array(img)

    cv2.imwrite('test_img.jpg',cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
    
    frame = cv2.imread('test_img.jpg')
    HEIGHT, WIDTH, _ = frame.shape

    frame_copy = frame.copy()

    scan_detection(frame_copy)
    # st.image(frame_copy)

    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
    # st.image(warped)

    processed = image_processing(warped)
    processed = processed[10:processed.shape[0] - 10, 10:processed.shape[1] - 10]
    # st.image(processed)

    ocr_text = pytesseract.image_to_string(processed)

    extractText(ocr_text)

