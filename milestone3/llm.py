#from llama_index.llms.gemini import Gemini
#from llama_index.llms.google_genai import GoogleGenAI
from config import GEMINI_MODEL, TEMPERATURE
import os
from dotenv import load_dotenv
import llama_index.llms.google_genai
#import google.generativeai as genai
from llama_index.llms.google_genai import GoogleGenAI

# Load the environment variables from .env file
load_dotenv()

# Now you can access the environment variable just like before
#api_key = os.environ.get('GEMINI_API_KEY')

# Initialize with the new class

#llm = GoogleGenAI(
    #model="gemini-1.5-flash",  # Note: The 'models/' prefix is often handled automatically now
    #api_key="YOUR_API_KEY"
#)

# Test the connection
#response = llm.complete("Hello, how are you?")
#print(response)

def get_llm():
    return GoogleGenAI(model=GEMINI_MODEL,api_key=os.environ.get('GEMINI_API_KEY'),temperature=TEMPERATURE)