from flask import Flask, request, jsonify
import pdf2image
import io
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY ='AIzaSyAKoOr-E5A5YA6n78UMyXcytwKVV3Yf5_s'
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        images = pdf2image.convert_from_bytes(file.read(), dpi=300)
        uploaded_images = []
        for idx, image in enumerate(images):
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            uploaded_image = genai.upload_file(file=img_buffer, display_name=f"Page {idx}")
            uploaded_images.append(uploaded_image)
        prompt = """Provide the name skills and languages from the image:

response = {'name': str,
             'skills':list[skills],
             'languages':list[languages] }
Return:response"""
        model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                      generation_config={"response_mime_type": "application/json"},
                                      system_instruction="You are a resume parser agent you will be provided a image of a resume and just give the details from the resume.")
        raw_response = model.generate_content([prompt] + uploaded_images)
        response = json.loads(raw_response.text)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
