from flask import Flask, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for the whole app

UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process_image', methods=['POST'])
def process_image():
    print("HELLOOOO")
    if 'frame' not in request.files:
        return 'No file part', 400

    file = request.files['frame']
    print(file)
    filename = secure_filename(f'{uuid.uuid4()}.png')
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    response = make_response(f'File saved to {save_path}', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    

if __name__ == '__main__':
    app.run(debug=True)
