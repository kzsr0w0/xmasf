#############################
# メリークリスマス！
#
#   2023.12.18
##########################

# --- 事前設定 --- #

# モジュールのインポート
from fastapi import FastAPI, File, UploadFile, Response
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import io

# FastAPIのインスタンス化
app = FastAPI()

# 学習済みモデルをロード スタイル転送モデル
model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

# --- スタイル画像の設定 --- #
#絶対パス
#style_image_path = 'C:\\folder\\make\\Python\\xmasf\\path_to_christmas_style_image.jpg'
#
style_image_path='.\\path_to_christmas_style_image.jpg'
style_image = Image.open(style_image_path).convert('RGB')
style_image = style_image.resize((256, 256))
style_image = tf.keras.preprocessing.image.img_to_array(style_image)
style_image = np.expand_dims(style_image, axis=0)

def load_img(image_file):
    # 画像を読み込み、適切な形式に変換
    img = Image.open(image_file).convert('RGB')
    img = img.resize((256, 256))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

# --- アプリの設定 --- #

# エンドポイントの定義
@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Style Transfer API"}

@app.post("/transfer-style/")
async def transfer_style(content_file: UploadFile = File(...)):
    # コンテンツ画像を読み込み
    content_image = load_img(io.BytesIO(await content_file.read()))

    # スタイル転送を実行
    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]

    # 出力画像をPIL形式に変換し、バイト列に変換
    stylized_image = tf.keras.preprocessing.image.array_to_img(stylized_image[0])
    img_byte_arr = io.BytesIO()
    stylized_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    return Response(content=img_byte_arr, media_type="image/jpeg")