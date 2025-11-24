import streamlit as st
from PIL import Image
import imageio
import re
import io

st.title("LINEスタンプ自動変換（結合処理付き）")

uploaded_files = st.file_uploader(
    "画像をアップロードしてください（複数可）",
    type=["png"],
    accept_multiple_files=True
)

# 数字抽出関数
def extract_number(filename):
    match = re.search(r"(\d+)", filename)
    return int(match.group(1)) if match else 0

if uploaded_files:
    # ファイル名順に並び替え
    uploaded_files = sorted(uploaded_files, key=lambda f: extract_number(f.name))
    st.write("読み込み順:", [f.name for f in uploaded_files])

    # 画像読み込み
    images = []
    for file in uploaded_files:
        img = Image.open(file).convert("RGBA")
        images.append(img)

    # PNGアニメーション生成
    output_name = "output.png"
    image_bytes = io.BytesIO()
    imageio.mimsave(image_bytes, images, format='PNG', duration=0.2)

    st.success("保存しました：output.png")

    st.download_button(
        label="ダウンロード",
        data=image_bytes.getvalue(),
        file_name="output.png",
        mime="image/png"
    )
