from flask import escape, request, jsonify
import pytesseract
from PIL import Image
import base64
import io

def get_ocr(request):
    image_base64 = request.args.get('image_base64')
    
    # Check if image_base64 is provided
    if not image_base64:
        return "Please provide a valid image in base64 encoding."

    # Convert base64 to image
    try:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        return f"An error occurred while decoding the image: {e}"

    # Perform OCR using pytesseract
    try:
        extracted_text = pytesseract.image_to_string(image, lang='jpn')
        formatted_text = extracted_text.replace('\n', '').replace('。', '。\n')
    except Exception as e:
        return f"An error occurred while performing OCR: {e}"

    # Return the OCR result
    response = jsonify({'text': formatted_text})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
