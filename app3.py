from flask import Flask, request, jsonify
import json
import genai

app = Flask(__name__)

@app.route('/upload_json', methods=['POST'])
def upload_json_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.json'):
        data = file.read()
        try:
            json_data = json.loads(data.decode('utf-8'))
            print(json_data)
            # Process the JSON data
            md_file = genai.upload_file(path="test.json", display_name="Starred Repos Content", mime_type="text/markdown")
            PROMPT="""you are a helper you will be provided a need and you have to search through the data of the starred repos of users and you have to provide the best solution they can use
using this JSON schema:
Repositories = [
  {
    repositoryname: string,
    description: string,
    url: string,
    stars: int
  },
  {
    repositoryname: string,
    description: string,
    url: string,
    stars: int
  },.....
]
"""
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash" , system_instruction=PROMPT, generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(
                [
                    "These are my starred repos tell me something i can use in state management",
                    md_file,
                ]
            )
            return jsonify({'response': response.text})
        except json.JSONDecodeError:
            return 'Invalid JSON file'
    return 'Only JSON files are allowed'

if __name__ == '__main__':
    app.run(debug=True)
