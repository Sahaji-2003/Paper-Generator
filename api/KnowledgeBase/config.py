import os
from dotenv import load_dotenv

# load_dotenv()
# Load environment variables from a specific file, such as .env.local
load_dotenv(dotenv_path=".env.local")


ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
