from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client()
def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text