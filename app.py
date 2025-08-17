import pytesseract
import streamlit as st
import cv2
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ==============================
# 1) Tiêu đề
# ==============================
st.title("📝 OCR App (English & Vietnamese)")

uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "png", "jpeg"])
lang = st.selectbox("🌐 Select language", ["eng", "vie", "eng+vie"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # ==============================
    # 2) Xử lý ảnh
    # ==============================
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ==============================
    # 3) OCR
    # ==============================
    text = pytesseract.image_to_string(Image.fromarray(bw), lang=lang)

    if not text.strip():
        st.warning("⚠️ Không nhận diện được văn bản trong ảnh.")
    else:
        st.text_area("📖 OCR Result", text, height=300)

        # ==============================
        # 4) Nút Copy & Download
        # ==============================
        # Copy vào Clipboard bằng JavaScript (render nút thật sự)
        copy_code = f"""
            <textarea id="ocr_text" style="display:none;">{text}</textarea>
            <button style="padding:8px 16px; font-size:16px; border:none; border-radius:6px; background-color:#4CAF50; color:white; cursor:pointer;"
                onclick="navigator.clipboard.writeText(document.getElementById('ocr_text').value); alert('✅ OCR result copied!');">
                📋 Copy to Clipboard
            </button>
        """
        st.markdown(copy_code, unsafe_allow_html=True)


        # Download file .txt
        st.download_button(
            label="💾 Download OCR Result",
            data=text,
            file_name="ocr_result.txt",
            mime="text/plain"
        )

# ==============================
# 5) Footer
# ==============================
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray; font-size:14px;">
        Developed by <b>Hồ Tăng Nhật Hiếu</b>
    </div>
    """,
    unsafe_allow_html=True
)
