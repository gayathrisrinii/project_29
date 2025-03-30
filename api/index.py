from flask import Flask, request, jsonify
from flask_cors import CORS
import zipfile
import os
import csv
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/api', methods=['GET', 'POST'])
def api():
        
        if request.method == 'GET':
            return jsonify({"message": "This is a GET request"})
        elif request.method == 'POST':
            question = request.form.get('question')  # Use .get() to avoid AttributeError
            file = request.files.get('file')
            if not question:
                return jsonify({"error": "The 'question' field is required"}), 400
            if not file or file.filename == '':
                return jsonify({"error": "No ZIP file provided"}), 400
            if "Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the answer column of the CSV file?" in question:
                try:
                    # Unzip the file
                    with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                        csv_filename = [f for f in z.namelist() if f.endswith('.csv')]
                        if not csv_filename:
                            return jsonify({"error": "No CSV file found in the ZIP"}), 400
                        csv_filename = csv_filename[0]
                        with z.open(csv_filename) as csv_file:
                            csv_data = csv.DictReader(io.TextIOWrapper(csv_file))
                            extracted_data = [row for row in csv_data]
                    
                    return jsonify(extracted_data), 200
                except zipfile.BadZipFile:
                    return jsonify({"error": "Invalid ZIP file"}), 400
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            else:
                return jsonify({"message": "No question found", "question": question})
        # file = request.files.get('file')
        # if not file or file.filename == '':
        #     return jsonify({"error": "No file provided"}), 400

        # # Save the uploaded file
        # upload_dir = "./uploads"
        # os.makedirs(upload_dir, exist_ok=True)
        # file_path = os.path.join(upload_dir, file.filename)
        # file.save(file_path)

        # # Check if the uploaded file is a zip file
        # if not zipfile.is_zipfile(file_path):
        #     os.remove(file_path)
        #     return jsonify({"error": "Uploaded file is not a valid zip file"}), 400

        # # Extract the zip file
        # extract_path = os.path.join(upload_dir, "extracted")
        # os.makedirs(extract_path, exist_ok=True)
        # with zipfile.ZipFile(file_path, 'r') as zip_ref:
        #     zip_ref.extractall(extract_path)

        # # Look for the CSV file inside the extracted folder
        # csv_file_path = None
        # for root, dirs, files in os.walk(extract_path):
        #     for filename in files:
        #         if filename.endswith('.csv'):
        #             csv_file_path = os.path.join(root, filename)
        #             break

        # if not csv_file_path:
        #     return jsonify({"error": "No CSV file found in the uploaded zip"}), 400

        # # Read the CSV file and find the value in the "answer" column
        # answer_value = None
        # try:
        #     with open(csv_file_path, mode='r') as csv_file:
        #         csv_reader = csv.DictReader(csv_file)
        #         for row in csv_reader:
        #             if 'answer' in row:
        #                 answer_value = row['answer']
        #                 break
        # except Exception as e:
        #     return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 500

        # if answer_value is None:
        #     return jsonify({"error": "No 'answer' column found in the CSV file"}), 400

        # # Clean up uploaded and extracted files
        # try:
        #     os.remove(file_path)
        #     for root, dirs, files in os.walk(extract_path, topdown=False):
        #         for name in files:
        #             os.remove(os.path.join(root, name))
        #         for name in dirs:
        #             os.rmdir(os.path.join(root, name))
        #     os.rmdir(extract_path)
        # except Exception as e:
        #     return jsonify({"error": f"Error during cleanup: {str(e)}"}), 500

        # return jsonify({"message": "File processed successfully", "answer": answer_value})