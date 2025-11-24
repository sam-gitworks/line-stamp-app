import streamlit as st
from PIL import Image
import imageio
import re
import io
import base64

st.title("LINEスタンプ自動変換（結合処理＋画面アニメ表示）")

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

    # PNGアニメーション生成（APNG）
    output_name = "output.png"
    image_bytes = io.BytesIO()
    imageio.mimsave(image_bytes, images, format='PNG', duration=0.2)

    st.success("保存しました：output.png")

    # ダウンロード
    st.download_button(
        label="ダウンロード",
        data=image_bytes.getvalue(),
        file_name="output.png",
        mime="image/png"
    )

    # --- ★ 画面でアニメーション再生（APNGをHTMLで埋め込み） ---
    encoded = base64.b64encode(image_bytes.getvalue()).decode()

    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{encoded}" />
        </div>
        """,
        unsafe_allow_html=True
    )
