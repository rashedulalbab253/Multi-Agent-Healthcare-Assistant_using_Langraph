import os

class Config:
    MODEL_ID = os.getenv("OLLAMA_MODEL", "medgemma")  # Ollama model name
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MAX_NEW_TOKENS = 1024

config = Config()