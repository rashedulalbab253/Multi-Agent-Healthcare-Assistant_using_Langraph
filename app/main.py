from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.analyze import router as analyze_router
import os
from dotenv import load_dotenv
from app.utils.model_loader import check_ollama_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# LangSmith env vars (optional - set to empty if not configured)
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "")

app = FastAPI()

# Check Ollama connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        check_ollama_connection()
        logger.info("✅ Ollama connection verified. Model is ready.")
    except Exception as e:
        logger.error(f"⚠️ Ollama check failed: {e}")
        logger.error("The app will start, but model inference will fail until Ollama is running.")

app.include_router(analyze_router, prefix="/api")

# Serve static HTML
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join("app/static", "index.html"))
