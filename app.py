from flask import Flask, request, make_response, send_file, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
from yolo import image_detect
import cv2
import base64

app = Flask(__name__)
CORS(app, supports_credentials=True)

counter = 0

UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['uploaded_images'] = UPLOAD_FOLDER

@app.route('/process_image', methods=['POST'])
def process_image():
    print("HELLOOOO")
    if 'frame' not in request.files:
        return 'No file part', 400

    file = request.files['frame']
   
    filename = secure_filename(f'{uuid.uuid4()}.jpg')
 
    save_path = os.path.join(app.config['uploaded_images'], filename)
    file.save(save_path)
    image, detected = image_detect(save_path)
    
    path = "processed_image.jpg"
    
    # response = make_response(f'File saved to {save_path}', 200)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # print(detected[0].label)
    print(detected)
    response = make_response(send_file('processed_image.jpg', mimetype='image/jpeg'))
    print(len(detected))
    if len(detected) == 0:
        response.headers['type'] = "Nothing"
    else: 
        print(detected[0])
        response.headers['type'] = detected[0]

    try:
        return send_file(path,mimetype="image/jpeg")
    finally:
        os.remove(save_path)
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
