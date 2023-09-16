from flask import Flask, request, render_template
from get_ocr import get_ocr
import json
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

endpoints = os.environ.get("ENDPOINTS")

if endpoints is None:
    raise EnvironmentError("The ENDPOINTS environment variable is not set.")
else:
    endpoints = endpoints.split(',')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', endpoints=endpoints)

def fetch_content(image_base64, endpoint):
    if endpoint == "http://127.0.0.1:5000/get_ocr":
        return json.loads(get_ocr(type('FakeRequest', (), {'args': {'image_base64': image_base64}})).get_data(as_text=True))['text']
    else:
        return "Unsupported endpoint"

@app.route('/show_result', methods=['POST'])
def show_result():
    image_base64 = request.form['image_base64']
    endpoint = request.form['endpoint']
    content = fetch_content(image_base64, endpoint)
    return render_template('index.html', content=content, endpoints=endpoints)

@app.route('/get_ocr', methods=['GET'])
def get_ocr_route():
    return get_ocr(request)

if __name__ == "__main__":
    app.run(debug=True)
