from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.handler import LLMHandler
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["LLM"])


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):

    logger.info("Received chat request")
    logger.info(f"User message: {request.message}")

    try:
        response = LLMHandler.process_user_message(request.message)

        logger.info("LLM response generated successfully")
        logger.debug(f"LLM response content: {response}")

        return {"response": response}

    except Exception as e:
        logger.exception("Error while processing chat request")
        raise e

# from app.llm.handler import LLMHandler

# response = LLMHandler.process_user_message(
#     "Show me the latest revenue"
# )

# print(response)
