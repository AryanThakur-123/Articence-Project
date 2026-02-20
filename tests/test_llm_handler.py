from unittest.mock import patch, MagicMock
from app.llm.handler import LLMHandler


@patch("app.llm.handler.client")
def test_process_message_without_function(mock_client):

    # Mock message object
    mock_message = MagicMock()
    mock_message.content = "Simple reply"
    mock_message.tool_calls = None  # Prevent function branch

    # Mock choice object
    mock_choice = MagicMock()
    mock_choice.message = mock_message

    # Mock response object
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    # Mock Groq client call
    mock_client.chat.completions.create.return_value = mock_response

    response = LLMHandler.process_user_message("Hello")

    assert response == "Simple reply"