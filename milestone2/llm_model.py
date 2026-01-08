from llama_index.llms.gemini import Gemini
from config import GEMINI_MODEL
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Now you can access the environment variable just like before
#api_key = os.environ.get('GEMINI_API_KEY')

def get_llm():
    return Gemini(model=GEMINI_MODEL,api_key=os.environ.get('GEMINI_API_KEY'),temperature=0.2)
