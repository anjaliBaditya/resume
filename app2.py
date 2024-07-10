import google.generativeai as genai
from IPython.display import Image



from google.colab import userdata

GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


Image(filename="res.png")

sample_file = genai.upload_file(path="res.png", display_name="Sample drawing")

print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

file = genai.get_file(name=sample_file.name)
print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

import json
import dataclasses
import typing_extensions as typing

model = genai.GenerativeModel("gemini-1.5-flash-latest",
                              generation_config={"response_mime_type": "application/json"},
                              system_instruction="You are a resume parser agent you will be provided a image of a resume and just give the details from the resume.")
prompt = """Provide the name skills and languages from the image:

response = {'name': str,
             'skills':list[skills],
             'languages':list[languages] }
Return:response"""
raw_response = model.generate_content([prompt , sample_file])

response = json.loads(raw_response.text)
print(json.dumps(response, indent=4))

genai.delete_file(sample_file.name)
print(f"Deleted {sample_file.display_name}.")




md_file = genai.upload_file(path="contrib.md", display_name="Contributors guide", mime_type="text/markdown")

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
response = model.generate_content(
    [
        "What should I do before I start writing, when following these guidelines?",
        md_file,
    ]
)
print(response.text)



cpp_file = genai.upload_file(
    path="gemma.cpp", display_name="gemma.cpp", mime_type="text/plain"
)

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
response = model.generate_content(["What does this program do?", cpp_file])
print(response.text)
