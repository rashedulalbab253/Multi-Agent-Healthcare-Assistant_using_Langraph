# app/agents/router_agent.py
from PIL import Image
from app.utils.logger import get_logger
from app.graph.types import State
from app.utils.prompt_builder import build_router_prompt
from langsmith.run_helpers import traceable
from app.agents.base_agent import BaseAgent
from app.utils.predictor import generate_response


logger = get_logger(__name__)

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RouterAgent")

    @traceable
    def respond(self, state: dict) -> str:
        image = state.payload.get("image", None)
        note = state.payload.get("note", None)
        has_image = image is not None
        logger.info(f"Identifying next agent for has_image: {has_image} with note: {note}")
        prompt = build_router_prompt(note, has_image)
        logger.info(f"RouterAgent prompt: {prompt}")
        
        # Pass images list if image exists
        images = [image] if image else None
        return generate_response(prompt, images)
    
    
    def run(self, state: State) -> State:
        """
        Run the agent with the provided image.
        """
        logger.info(f"Running {self.name} with state: {state}")
        
        response = self.respond(state).lower().strip()
        logger.info("RouterAgent response: %s", response)

        if "icd10" in response:
            state.payload["clinical_note"] = state.payload.get("note", "")
            state.type = "icd10"
        elif "soap" in response:
            state.payload["transcript"] = state.payload.get("note", "")
            state.type = "soap"
        elif "image_analysis" in response:
            state.type = "image_analysis"
            state.payload["image"] = state.payload.get("image", None)
            state.payload["clinical_note"] = state.payload.get("note", "")
        else:
            logger.error(f"Unknown response from RouterAgent: {response}")
            state.error = f"Unknown response from RouterAgent: {response}"
            return state
        return State(
            type=state.type,
            payload=state.payload,  # preserve existing payload
            result=response,            # add this line (or appropriate value)
            error=None              # no error
        )

    

