import google.generativeai as genai
from dotenv import load_dotenv

from security_config import get_google_api_key


load_dotenv()
genai.configure(api_key=get_google_api_key())

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
