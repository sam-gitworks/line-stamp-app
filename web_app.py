import streamlit as st
from PIL import Image
import io

st.title("LINEスタンプ自動変換（最小版）")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGBA")

    # スタンプ推奨サイズ
    resized = img.resize((270, 270), Image.LANCZOS)

    st.image(resized, caption="変換後の画像", width=200)

    buf = io.BytesIO()
    resized.save(buf, format="PNG")

    st.download_button(
        "変換画像をダウンロード",
        buf.getvalue(),
        file_name="stamp.png",
        mime="image/png"
    )
