import pytesseract
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Path to Tesseract (Linux/Streamlit Cloud)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ==============================
# 1) Title
# ==============================
st.title("📝 OCR App")

uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "png", "jpeg"])
lang = st.selectbox("🌐 Select language", ["-- Select language --", "eng", "vie", "eng+vie"])

if uploaded_file is not None and lang != "-- Select language --":
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # ==============================
    # 2) Image Preprocessing
    # ==============================
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ==============================
    # 3) OCR
    # ==============================
    text = pytesseract.image_to_string(Image.fromarray(bw), lang=lang)

    if not text.strip():
        st.warning("⚠️ No text detected in the image.")
    else:
        st.text_area("📖 OCR Result", text, height=300)

        # ==============================
        # 4) Buttons (Copy & Download)
        # ==============================
        # Fake "Copy" button (same style as Download)
        st.download_button(
            label="📋 Copy to Clipboard",
            data=text,
            file_name="copy.txt",   # user can open/copy
            mime="text/plain"
        )

        # Real Download button
        st.download_button(
            label="💾 Download OCR Result",
            data=text,
            file_name="ocr_result.txt",
            mime="text/plain"
        )

elif uploaded_file is not None and lang == "-- Select language --":
    st.info("👉 Please select a language before running OCR.")

# ==============================
# 5) Footer
# ==============================
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:14px;">
        Developed by <b>Ho Tang Nhat Hieu</b>
    </div>
    """,
    unsafe_allow_html=True
)
