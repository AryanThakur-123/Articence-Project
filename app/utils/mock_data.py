import json
import random
from datetime import datetime, timedelta,UTC
from pathlib import Path
from typing import List, Dict
import uuid


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# -------------------------
# CRM MOCK DATA
# -------------------------

def generate_customers(n: int = 50) -> List[Dict]:
    statuses = ["active", "inactive", "churned"]
    companies = ["Acme Corp", "Globex", "Initech", "Umbrella", "Wayne Enterprises"]

    customers = []

    for _ in range(n):
        created_at = datetime.now(UTC) - timedelta(days=random.randint(30, 1000))

        customers.append({
            "id": str(uuid.uuid4()),
            "name": f"Customer_{random.randint(1000, 9999)}",
            "email": f"user{random.randint(100,999)}@example.com",
            "company": random.choice(companies),
            "status": random.choice(statuses),
            "lifetime_value": round(random.uniform(100, 20000), 2),
            "created_at": created_at.isoformat(),
            "last_activity_at": (
                created_at + timedelta(days=random.randint(1, 365))
            ).isoformat()
        })

    return customers


# -------------------------
# SUPPORT MOCK DATA
# -------------------------

def generate_support_tickets(n: int = 100) -> List[Dict]:
    priorities = ["low", "medium", "high", "critical"]
    statuses = ["open", "in_progress", "resolved", "closed"]

    tickets = []

    for _ in range(n):
        created_at = datetime.now(UTC) - timedelta(days=random.randint(0, 90))

        tickets.append({
            "id": str(uuid.uuid4()),
            "customer_id": str(uuid.uuid4()),
            "subject": f"Issue_{random.randint(1000,9999)}",
            "description": "Auto-generated support ticket.",
            "priority": random.choice(priorities),
            "status": random.choice(statuses),
            "created_at": created_at.isoformat(),
            "resolved_at": (
                created_at + timedelta(days=random.randint(1, 10))
            ).isoformat() if random.random() > 0.5 else None
        })

    return tickets


# -------------------------
# ANALYTICS MOCK DATA
# -------------------------

def generate_analytics(days: int = 30) -> List[Dict]:
    metrics = ["daily_active_users", "revenue", "new_signups"]

    analytics = []
    today = datetime.now(UTC)

    for metric in metrics:
        for i in range(days):
            date = today - timedelta(days=i)

            analytics.append({
                "metric_name": metric,
                "timestamp": date.isoformat(),
                "value": round(random.uniform(100, 10000), 2)
            })

    return analytics


# -------------------------
# WRITE TO FILES
# -------------------------

def write_mock_data():
    customers = generate_customers()
    tickets = generate_support_tickets()
    analytics = generate_analytics()

    with open(DATA_DIR / "customers.json", "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2)

    with open(DATA_DIR / "support_tickets.json", "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)

    with open(DATA_DIR / "analytics.json", "w", encoding="utf-8") as f:
        json.dump(analytics, f, indent=2)

    print("Mock data generated successfully.")


if __name__ == "__main__":
    write_mock_data()
