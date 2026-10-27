import random
from locust import HttpUser, task, between

class StoreManagerUser(HttpUser):

    wait_time = between(1, 3)

    @task(1)
    def test_create_order(self):
        """Test de charge sur la creation des commandes"""

        payload = {
            "user_id": random.randint(1, 3),
            "items": [
                {
                    "product_id": random.randint(1, 4),
                    "quantity": random.randint(1, 10)
                }
            ]
        }

        with self.client.post("/orders", json=payload, catch_response=True) as response:
            if response.status_code >= 400:
                response.failure(f"HTTP {response.status_code} : {response.text[:500]}")