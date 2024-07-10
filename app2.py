from flask import Flask, request, jsonify
import pdf2image
import io
import google.generativeai as genai
import tempfile
import os
import json
import dataclasses
import typing_extensions as typing
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv() 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY is None:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")
genai.configure(api_key=GOOGLE_API_KEY)

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if request.method == "POST":
        pdf_file = request.files["pdf_file"]
        temp_file_path = os.path.join(os.getcwd(), pdf_file.filename)
        pdf_file.save(temp_file_path)
        
        images = pdf2image.convert_from_path(temp_file_path, dpi=200)[:2]
        image_files = []
        num_pages=len(images)
        model = genai.GenerativeModel("gemini-1.5-flash-latest",
                              generation_config={"response_mime_type": "application/json"},
                              system_instruction="You are a resume parser agent you will be provided a image of a resume and just give the details from the resume.")
        prompt = """Provide the name skills and languages and suggestions how this resume can be improved from the image  the 1st image is 1st page and 2nd image is second page of resume:

                    response = {'name': str,
                    'skills':list[skills],
                    'languages':list[languages],}
                    Return:response"""
        for i, image in enumerate(images):
            image_file = f"page_{i+1}.jpg"
            image.save(image_file, "JPEG")
            image_files.append(os.path.join(os.getcwd(), image_file))
        try:
            if num_pages == 2:
                img_page1 = genai.upload_file(path=image_files[0], display_name=f"Page 1")
                img_page2 = genai.upload_file(path=image_files[1], display_name=f"Page 2")
                raw_response = model.generate_content([prompt , img_page1 , img_page2])
            else:
                img_page1 = genai.upload_file(path=image_files[0], display_name=f"Page 1")
                raw_response = model.generate_content([prompt , img_page1])
            print(img_page1)
            response = json.loads(raw_response.text)
        finally:
            # Delete temporary files
            os.remove(temp_file_path)
            for image_file in image_files:
                os.remove(image_file)  
            
        return response
    return jsonify({"message": "Invalid request"})

if __name__ == "__main__":
    app.run(debug=True)
