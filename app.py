import pytesseract
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import streamlit.components.v1 as components
import uuid
from streamlit_cropper import st_cropper
import platform  # 👈 thêm

# Path to Tesseract (Windows / Linux / Streamlit Cloud)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# ==============================
# 1) Title
# ==============================
st.title("📝 OCR App (English & Vietnamese)")

uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # ==============================
    # 2) Crop Option
    # ==============================
    crop_option = st.radio("Do you want to crop the image?", ["No", "Yes"])

    if crop_option == "Yes":
        st.subheader("✂️ Crop Image")
        cropped_img = st_cropper(img, realtime_update=True, box_color='#FF0000', aspect_ratio=None)
        st.image(cropped_img, caption="Cropped Image", use_container_width=True)
        final_img = cropped_img
    else:
        final_img = img

    # ==============================
    # 3) Language Selection
    # ==============================
    lang = st.selectbox("🌐 Select language", ["-- Select language --", "eng", "vie", "eng+vie"])

    if lang != "-- Select language --":
        # ==============================
        # 4) Image Preprocessing
        # ==============================
        img_cv = cv2.cvtColor(np.array(final_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # ==============================
        # 5) OCR
        # ==============================
        text = pytesseract.image_to_string(Image.fromarray(bw), lang=lang)

        if not text.strip():
            st.warning("⚠️ No text detected in the image.")
        else:
            st.text_area("📖 OCR Result", text, height=300)

            # ==============================
            # 6) Buttons (Copy & Download)
            # ==============================
            msg_id = f"msg-{uuid.uuid4()}"
            copy_btn = f"""
                <button onclick="navigator.clipboard.writeText(`{text}`);
                                 var el = document.getElementById('{msg_id}');
                                 el.style.display='block';"
                        style="padding:8px 16px; font-size:16px; border:none;
                               border-radius:6px; background-color:#4CAF50;
                               color:white; cursor:pointer;">
                    📋 Copy to Clipboard
                </button>
                <p id="{msg_id}" style="display:none; color:green; margin-top:10px;">
                    ✅ Copied to clipboard!
                </p>
            """
            components.html(copy_btn, height=80)

            st.download_button(
                label="💾 Download OCR Result",
                data=text,
                file_name="ocr_result.txt",
                mime="text/plain"
            )
    else:
        st.info("👉 Please select a language before running OCR.")

# ==============================
# 7) Footer
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
