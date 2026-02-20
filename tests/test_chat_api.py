from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


@patch("app.llm.handler.LLMHandler.process_user_message")
def test_chat_endpoint(mock_llm):
    mock_llm.return_value = "Mocked response"

    response = client.post(
        "/chat/",
        json={"message": "Show me revenue"}
    )

    assert response.status_code == 200
    assert response.json()["response"] == "Mocked response"