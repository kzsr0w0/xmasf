import streamlit as st
import requests

st.title('Style Transfer App')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg"])

if uploaded_file is not None:
    # FastAPIエンドポイントに画像を送信
    response = requests.post("http://127.0.0.1:8000/transfer-style/", files={"content_file": uploaded_file})
    #response = requests.post("https://xmasf.onrender.com/transfer-style/", files={"content_file": uploaded_file})
    
    # 結果を表示
    if response.ok:
        st.image(response.content, caption='Styled Image', use_column_width=True)
    else:
        print('error!')