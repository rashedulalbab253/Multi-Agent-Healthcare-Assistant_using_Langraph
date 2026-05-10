import requests
import base64
from io import BytesIO
from PIL import Image
from typing import Optional, List
from app.config.config import config
from app.utils.logger import get_logger

logger = get_logger(__name__)


def generate_response(prompt: str, images: Optional[List[Image.Image]] = None) -> str:
    """
    Generate response using the MedGemma model via Ollama API.
    
    Args:
        prompt: The text prompt to send to the model.
        images: Optional list of PIL Images for multimodal input.
    
    Returns:
        str: The generated response text.
    """
    logger.info("Generating response via Ollama with prompt: %s", prompt[:200])

    payload = {
        "model": config.MODEL_ID,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": config.MAX_NEW_TOKENS,
        }
    }

    # If images are provided, encode them as base64 for Ollama's multimodal API
    if images:
        encoded_images = []
        for img in images:
            if img is not None:
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                encoded_images.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))
        if encoded_images:
            payload["images"] = encoded_images

    try:
        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=300  # 5 min timeout for generation
        )
        response.raise_for_status()
        result = response.json()
        output_text = result.get("response", "")
        logger.info("Model output: %s", output_text[:200])
        return output_text

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. Please make sure Ollama is running. "
            "Run 'ollama serve' in a terminal."
        )
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise
