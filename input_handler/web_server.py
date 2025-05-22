import os
import base64
import requests
import logging # Added
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.logger.setLevel(logging.INFO) # Added

# Configuration
PROCESSING_SERVICE_URL = os.getenv("WEBHOOK_URL", "http://processing-service:8000/process")
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/upload')
def upload_form():
    return render_template('upload_form.html')

@app.route('/web_submit', methods=['POST'])
def web_submit():
    app.logger.info("Processing /web_submit request...") # Changed to app.logger.info
    description = request.form.get('description')
    uploaded_files = request.files.getlist('images')

    app.logger.info(f"Description: {description}") # Changed to app.logger.info

    app.logger.info(f"Number of images received: {len(uploaded_files)}") # Changed to app.logger.info
    for image in uploaded_files:
        app.logger.info(f"Image filename: {image.filename}") # Changed to app.logger.info

    if not description or not uploaded_files:
        app.logger.error("Error: Description and images are required.") # Changed to app.logger.error
        return "Description and images are required.", 400

    base64_images = []
    for file in uploaded_files:
        if file.filename == '':
            continue 
        try:
            file_bytes = file.read()
            encoded_string = base64.b64encode(file_bytes).decode('utf-8')
            content_type = file.content_type
            data_uri = f"data:{content_type};base64,{encoded_string}"
            base64_images.append(data_uri)
        except Exception as e:
            app.logger.error(f"Error processing file {file.filename}: {e}") # Changed to app.logger.error
            return f"Error processing file {file.filename}.", 500

    if not base64_images:
        app.logger.error("Error: No valid images were processed.") # Changed to app.logger.error
        return "No valid images were processed.", 400

    payload = {
        "source": "web_form",
        "user_id": "web_user", 
        "text": description,
        "images": base64_images 
    }
    
    # Log payload summary
    logged_payload_summary = {
        "source": payload.get("source"),
        "user_id": payload.get("user_id"),
        "text_length": len(payload.get("text", "")),
        "num_images": len(payload.get("images", []))
    }
    app.logger.info(f"Payload for processing service: {logged_payload_summary}") # Changed to app.logger.info

    try:
        response = requests.post(PROCESSING_SERVICE_URL, json=payload)
        response.raise_for_status() 
        app.logger.info(f"Response from processing service: {response.status_code}, {response.text}") # Changed to app.logger.info
        return f"Successfully submitted to processing service. Response: {response.json()}", 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error sending data to processing service: {e}") # Changed to app.logger.error
        return f"Error sending data to processing service: {e}", 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}") # Changed to app.logger.error
        return f"An unexpected error occurred: {e}", 500

if __name__ == '__main__':
    # For direct execution, set up basic logging to see app.logger output
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)
