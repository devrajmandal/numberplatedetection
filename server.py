from flask import Flask, request, jsonify
import cv2
import numpy as np
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/readnumberplate', methods=['POST'])
def read_numberplate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    
    results = reader.readtext(img)
    detected_plates = [res[1] for res in results]
    print(f"Detected: {detected_plates}")

    return jsonify({'number_plate': detected_plates[0] if detected_plates else 'Not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
