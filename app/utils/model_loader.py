import requests
from app.config.config import config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def check_ollama_connection():
    """
    Check if Ollama is running and the model is available.
    Pulls the model if not already downloaded.
    """
    try:
        # Check if Ollama server is running
        response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        logger.info("[INFO] Ollama server is running.")

        # Check if the model is already downloaded
        models = response.json().get("models", [])
        model_names = [m.get("name", "") for m in models]
        
        if not any(config.MODEL_ID in name for name in model_names):
            logger.info(f"[INFO] Model '{config.MODEL_ID}' not found locally. Pulling...")
            pull_response = requests.post(
                f"{config.OLLAMA_BASE_URL}/api/pull",
                json={"name": config.MODEL_ID},
                stream=True,
                timeout=600
            )
            pull_response.raise_for_status()
            # Stream through the response to wait for completion
            for line in pull_response.iter_lines():
                if line:
                    logger.info(f"[PULL] {line.decode('utf-8')}")
            logger.info(f"[INFO] Model '{config.MODEL_ID}' pulled successfully.")
        else:
            logger.info(f"[INFO] Model '{config.MODEL_ID}' is already available.")

        return True

    except requests.exceptions.ConnectionError:
        logger.error(
            "[ERROR] Cannot connect to Ollama. "
            "Please make sure Ollama is installed and running. "
            "Download from https://ollama.com and run 'ollama serve'."
        )
        raise RuntimeError(
            "Ollama is not running. Please start Ollama first. "
            "Download from https://ollama.com and run 'ollama serve'."
        )
    except Exception as e:
        logger.error(f"[ERROR] Failed to verify Ollama setup: {e}")
        raise
