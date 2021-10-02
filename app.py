import pytesseract
from PIL import Image
import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, support_credentials=True)

ROOT_DIR = os.path.abspath(os.curdir)


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        files = request.files
        file = files.get('image')
        file.save(secure_filename(file.filename))
        im = Image.open(f'./{file.filename}').convert('RGB')
        im.save(f'./{file.filename}.webp', 'webp')

        @app.after_request
        def delete(response):
            if os.path.exists(f'{file.filename}.webp'):
                os.remove(f'./{file.filename}.webp')
                os.remove(f'./{file.filename}')
            return response

        return send_file(f'./{file.filename}.webp', mimetype='image/webp')


@app.route('/text', methods=['POST'])
def get_text():
    if request.method == 'POST':
        files = request.files
        file = files.get('image')
        file.save(secure_filename(file.filename))
        text = pytesseract.image_to_string(Image.open(f'{file.filename}'))

        @app.after_request
        def delete(response):
            if os.path.exists(f'{file.filename}.webp'):
                os.remove(f'./{file.filename}.webp')
                os.remove(f'./{file.filename}')
            return response
        return jsonify(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)