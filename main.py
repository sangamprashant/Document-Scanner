from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from scan import DocScanner

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Create the 'uploads' directory if it does not exist
UPLOADS_DIR = 'uploads'
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

@app.route('/scan', methods=['POST'])
def scan_image():
    # Check if the POST request has the file part
    print("hello")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file to the 'uploads' directory
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        file.save(file_path)

        # Initialize the document scanner
        scanner = DocScanner()

        # Scan the uploaded image
        try:
            scanner.scan(file_path)
            result_path = os.path.join('output', os.path.basename(file_path))
            return jsonify({'success': True, 'result_path': result_path})
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)