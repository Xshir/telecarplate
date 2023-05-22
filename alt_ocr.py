import requests
import base64
import cv2
from constants import ALT_OCR_API_KEY
api_endpoint = 'https://api.ocr.space/parse/image'

def encode_image(image):
    # img to base64
    _, img_encoded = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    return img_base64

def ocr(opencv_frame):
    img_base64 = encode_image(opencv_frame)
    payload = {'base64Image': 'data:image/jpeg;base64,' + img_base64}
    response = requests.post(
                            'https://api.ocr.space/parse/image',
                            data=payload, 
                            headers={'apikey': ALT_OCR_API_KEY}
                            )
    json_response = response.json()
    parsed_text = json_response["ParsedResults"][0]["ParsedText"]
    if parsed_text != "":
        return parsed_text
    else: 
        return False


