from flask import Flask, request, jsonify
import pdf2image
import io
import google.generativeai as genai
import json
import mimetypes

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAKoOr-E5A5YA6n78UMyXcytwKVV3Yf5_s'
genai.configure(api_key=GOOGLE_API_KEY)

def convert_pdf_to_images(file):
    try:
        images = pdf2image.convert_from_bytes(file.read(), dpi=300)
        return images, None
    except pdf2image.PDFInfoNotInstalledError:
        return None, 'PDFInfoNotInstalledError'
    except Exception as e:
        return None, str(e)

def upload_images_to_genai(images):
    try:
        uploaded_images = []
        for idx, image in enumerate(images):
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            # Assuming the function genai.upload_file exists and works as intended
            uploaded_image = genai.upload_file(file=img_buffer, display_name=f"Page {idx}").blob
            uploaded_images.append(uploaded_image)
        return uploaded_images, None
    except Exception as e:
        return None, str(e)

def extract_resume_info(uploaded_images):
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-flash-latest",
            generation_config={"response_mime_type": "application/json"},
            system_instruction="You are a resume parser agent. You will be provided with an image of a resume. Please extract details such as name, skills, languages, and provide suggestions for improvement."
        )

        # Create the prompt for the generative model
        prompt = """Provide the name, skills, languages, and suggestions on how this resume can be improved from the image. The first image is the first page, and the second image is the second page of the resume:

        response = {'name': str,
                    'skills': list[skills],
                    'languages': list[languages],
                    'pages': list[pagenocontent, pagenocontent,....]}
        Return:response"""
        
        raw_response = model.generate_content([prompt, uploaded_images])
        response = json.loads(raw_response.text)
        return response, None
    except Exception as e:
        return None, str(e)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if mimetypes.guess_type(file.filename)[0] != 'application/pdf':
            return jsonify({'error': 'Invalid file type'}), 400

        images, error = convert_pdf_to_images(file)
        if error:
            return jsonify({'error': error}), 500
        
        uploaded_images, error = upload_images_to_genai(images)
        if error:
            return jsonify({'error': error}), 500
        
        response, error = extract_resume_info(uploaded_images)
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
