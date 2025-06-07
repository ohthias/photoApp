from flask import Flask, request, render_template, send_file
import os
import uuid
import cv2
import qrcode
from PIL import Image
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'fotos'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data_urls = request.json['photos']
    codigo = str(uuid.uuid4())[:8].upper()
    caminho = os.path.join(UPLOAD_FOLDER, codigo)
    os.makedirs(caminho, exist_ok=True)

    for i, data_url in enumerate(data_urls):
        header, encoded = data_url.split(',', 1)
        img_data = base64.b64decode(encoded)
        with open(os.path.join(caminho, f'foto_{i+1}.jpg'), 'wb') as f:
            f.write(img_data)

    # Gerar QR Code
    qr = qrcode.make(codigo)
    qr_path = os.path.join(caminho, 'qrcode.png')
    qr.save(qr_path)

    return {'codigo': codigo}

@app.route('/qrcode/<codigo>')
def get_qrcode(codigo):
    path = os.path.join(UPLOAD_FOLDER, codigo, 'qrcode.png')
    return send_file(path, mimetype='image/png')
