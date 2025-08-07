# Facebook Post Scraper + OCR Viewer (Streamlit) — LIVE SCRAPER ENABLED
# Version 2 - Pulls live posts from 4 selected public Facebook pages

import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import requests
from io import BytesIO
from facebook_scraper import get_posts

st.set_page_config(layout="wide")
st.title("📦 Facebook Post Price Tracker (Point)")

# Pages to Track
facebook_pages = [
    ("Aalam AlQalaa", "Aalam.AlQalaa"),
    ("Trendmiq", "Trendmiq"),
    ("Burj Al Arab Zayona", "BurjAlArabzayona"),
    ("Estore Iraq", "estoreiraq")
]

# Collect recent posts (limit to 1 page each for performance)
data = []
with st.spinner("⏳ Fetching latest posts..."):
    for name, page in facebook_pages:
        try:
            for post in get_posts(page, pages=1):
                if post.get("text") or post.get("images"):
                    data.append({
                        "Page": name,
                        "Post Text": post.get("text", "").strip(),
                        "Image URL": post.get("images", [None])[0],
                        "Post Date": post.get("time")
                    })
        except:
            st.warning(f"⚠️ Failed to load posts from: {name}")

# Convert to DataFrame
df = pd.DataFrame(data)

# Search Bar
query = st.text_input("🔍 ابحث عن منتج أو سعر (مثال: ايفون، 299000)", "")

# Filtered results
if query:
    results = df[df.apply(lambda row: query in str(row['Post Text']), axis=1)]
else:
    results = df

# Show results
for i, row in results.iterrows():
    st.subheader(f"📌 {row['Page']} — {row['Post Date'].strftime('%Y-%m-%d') if row['Post Date'] else ''}")
    st.write(row['Post Text'])

    if row['Image URL']:
        try:
            image = Image.open(BytesIO(requests.get(row['Image URL']).content))
            st.image(image, caption="📸 الصورة المرفقة", use_column_width=True)
            ocr_text = pytesseract.image_to_string(image, lang='ara')
            st.markdown(f"**🧠 OCR (نص مستخرج من الصورة):**")
            st.code(ocr_text)
        except:
            st.warning("لم يتم تحميل الصورة أو تحليل النص.")
    else:
        st.info("لا توجد صورة مرفقة في هذا المنشور.")

    st.markdown("---")
