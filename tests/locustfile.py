# tests/locustfile.py
from locustfile import HttpUser, task, between
import random

class BotUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8080"

    @task(70)
    def send_text_message(self):
        questions = [
            "Что такое Python?",
            "Объясни машинное обучение",
            "Как работает интернет?",
            "Что такое база данных?",
        ]
        self.client.post("/webhook", json={
            "update_id": random.randint(1, 999999),
            "message": {
                "message_id": random.randint(1, 999),
                "from": {"id": random.randint(1, 9999), "first_name": "Test"},
                "chat": {"id": random.randint(1, 9999), "type": "private"},
                "text": random.choice(questions)
            }
        })

    @task(20)
    def send_command(self):
        self.client.post("/webhook", json={
            "update_id": random.randint(1, 999999),
            "message": {
                "message_id": random.randint(1, 999),
                "from": {"id": random.randint(1, 9999), "first_name": "Test"},
                "chat": {"id": random.randint(1, 9999), "type": "private"},
                "text": "/start"
            }
        })

    @task(10)
    def send_search(self):
        self.client.post("/webhook", json={
            "update_id": random.randint(1, 999999),
            "message": {
                "message_id": random.randint(1, 999),
                "from": {"id": random.randint(1, 9999), "first_name": "Test"},
                "chat": {"id": random.randint(1, 9999), "type": "private"},
                "text": "/search Python tutorial"
            }
        })