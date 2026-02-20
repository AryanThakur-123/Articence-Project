# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_health():
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json()["status"] == "ok"


# def test_crm_data():
#     response = client.get("/data/crm?limit=2")
#     assert response.status_code == 200
#     body = response.json()
#     assert "data" in body
#     assert "metadata" in body


# def test_llm_execute():
#     response = client.post(
#         "/llm/execute",
#         json={
#             "name": "get_data",
#             "arguments": {
#                 "source": "crm",
#                 "limit": 2
#             }
#         }
#     )
#     assert response.status_code == 200
#     body = response.json()
#     assert "data" in body
#     assert "metadata" in body
