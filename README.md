# Aadhaar Card Information Extractor
This project is an implementation of OCR (Optical Character Recognition) to extract relevant information from an Aadhaar card.

Deployed App: [here](https://cvaproject-aadhaarcardin-aadhar-info-extractor-streamlit-0gi7up.streamlit.app/)

## Setup
1. Install the required packages by running pip install -r requirements.txt.
2. Download and install Tesseract OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki).
3. Set the Tesseract OCR engine path in the code.

## Usage
1. Run the code `python aadhaar_info_extractor.py image_name.jpg`, replace `image_name.jpg` with the filepath to your image.
2. The input image, warped image, and processed image will be displayed.
3. The extracted text (Aadhaar number, name, DOB, and gender) will be printed in the console.

OR

`pip install acie`<br>
Then, just type acie followed by the filename argument, for example:
`acie filename.jpg`
<hr>
# Aadhaar Card Information Extractor - Streamlit

## Follow same setup steps

## Usage: 
### For Self-hosting the application:
1. Run the code `streamlit run aadhar_info_extractor_streamlit.py`.
2. Open localhost link as display on the terminal.
3. Upload images via the file uploader.
4. The extracted text (Aadhaar number, name, DOB, and gender) will be printed on the page.

### Alternatively, deployed website available [here](https://cvaproject-aadhaarcardin-aadhar-info-extractor-streamlit-0gi7up.streamlit.app/)
<hr>
PyPi Repository: https://pypi.org/project/acie/
