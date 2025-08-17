import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.title("📝 OCR App (English & Vietnamese)")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

lang = st.selectbox("Select language", ["eng", "vie"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    text = pytesseract.image_to_string(Image.fromarray(bw), lang=lang)
    st.text_area("OCR Result", text, height=300)
