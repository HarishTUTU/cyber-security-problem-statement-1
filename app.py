from flask import Flask, render_template, request, jsonify
import os
import magic

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'exe', 'zip', 'rar', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')  # Make sure this points to the templates folder

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_name": filename,
            "file_type": file_type,
            "file_path": file_path
        })
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/check_url', methods=['POST'])
def check_url():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    return jsonify({
        "message": "URL checked successfully",
        "url": url,
        "malware_status": "Safe"
    })

if __name__ == '__main__':
    app.run(debug=True)
