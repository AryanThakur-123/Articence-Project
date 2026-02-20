import json
import os
from groq import Groq
from dotenv import load_dotenv
from app.llm.function_schemas import QUERY_DATA_FUNCTION
from app.models.common import DataQuery
from app.connectors.registry import get_connector  # You should have this
from app.models.common import DataResponse
import logging
logger = logging.getLogger(__name__)

load_dotenv("settings.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class LLMHandler:

    @staticmethod
    def process_user_message(user_message: str) -> str:
        """
        Full LLM → Function Call → Backend → LLM loop
        """

        logger.info("Processing user message: %s", user_message)

        messages = [
            {"role": "system", "content": "You are a business data assistant."},
            {"role": "user", "content": user_message}
        ]

        # Step 1 — Ask model
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=[{
                "type": "function",
                "function": QUERY_DATA_FUNCTION
            }],
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Step 2 — Did model call function?
        if message.tool_calls:

            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info("Function call detected: %s", function_name)
            logger.debug("Function arguments: %s", arguments)

            # Step 3 — Execute backend
            data_query = DataQuery(**arguments)

            logger.info("Executing connector for source: %s", data_query.source)

            connector = get_connector(data_query.source)
            result: DataResponse = connector.execute(data_query)

            # Log row count safely
            if hasattr(result, "data") and isinstance(result.data, list):
                logger.info("Filtered rows count: %d", len(result.data))
            else:
                logger.info("Data returned from connector")

            # Step 4 — Send tool result back to LLM
            messages.append(message)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result.model_dump())
            })

            # Step 5 — Final response
            final_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )

            logger.info("Final response generated")

            return final_response.choices[0].message.content

        # If no function call
        logger.info("No function call detected, returning direct LLM response")
        return message.content