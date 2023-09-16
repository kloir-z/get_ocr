from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pytesseract
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app, resources={r"/get_ocr": {"origins": ["http://localhost:3000", "https://my-pj-20230703.firebaseapp.com"]}})

@app.route('/get_ocr', methods=['POST'])
def get_ocr():
    try:
        data = request.json
        image_base64 = data.get('image_base64')
        
        if not image_base64:
            return make_response("Please provide a valid image in base64 encoding.", 400)

        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
        
        extracted_text = pytesseract.image_to_string(image, lang='jpn')
        formatted_text = extracted_text.replace('\n', '').replace('。', '。\n')

        response = jsonify({'text': formatted_text})
        return response

    except Exception as e:
        return make_response(f"An error occurred: {e}", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)