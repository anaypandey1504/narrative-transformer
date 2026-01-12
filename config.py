import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 8192

def validate_config():
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set. Get your FREE API key at:\n"
            "  https://console.groq.com/keys\n\n"
            "Then set it via:\n"
            "  - Environment variable: $env:GROQ_API_KEY = 'your-key'\n"
            "  - Or create a .env file with: GROQ_API_KEY=your-key"
        )
    return True
