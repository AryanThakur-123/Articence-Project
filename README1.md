# Universal Data Connector

A modular, LLM-integrated data access layer that unifies CRM, Support, and Analytics systems into a standardized API interface.

## 🚀 Features

Modular connector architecture

Business rules engine

Voice optimization layer

LLM function-calling integration

Structured logging

Full test coverage

Dockerized deployment

## 🏗 Architecture Overview
Client → FastAPI Router → LLM Handler → Connector
                                   ↓
                        Business Rules Engine
                                   ↓
                         Voice Optimization
                                   ↓
                              Response
## 📁 Project Structure
app/
 ├── connectors/        # CRM, Support, Analytics connectors
 ├── services/          # Business logic + optimization
 ├── models/            # Pydantic models
 ├── routers/           # API endpoints
 ├── utils/             # Logging + mock data
 └── main.py            # Application entry point
⚙️ Setup (Local Development)
1️⃣ Create virtual environment
python -m venv .venv
2️⃣ Activate

Windows:

.venv\Scripts\activate

Mac/Linux:

source .venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run server
uvicorn app.main:app --reload

Visit:

http://localhost:8000/docs
## 🐳 Docker Setup
Build Image
docker build -t universal-data-connector .
Run Container
docker run -p 8000:8000 universal-data-connector
## 🧪 Running Tests
pytest

All tests should pass.

## 🔍 Available Endpoints

GET /health

GET /data/crm

GET /data/support

GET /data/analytics

POST /chat (LLM-powered)

## 🧠 Business Logic

Automatic data type identification

Filtering & pagination

Business rule application

Voice-context summarization

Metadata enrichment

## 🛠 Tech Stack

FastAPI

Pydantic

OpenAI / Claude (function calling)

Pytest

Docker
