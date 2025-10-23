import json
import time
import random
from kafka import KafkaProducer

KAFKA_BROKER = "kafka:9092"
TOPIC = "raw-data"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def generate_event():
    return {
        "user_id": random.randint(1000, 9999),
        "event_type": random.choice(["click", "view", "purchase"]),
        "amount": round(random.uniform(5.0, 500.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }


if __name__ == "__main__":
    time.sleep(30)
    print(f"🚀 Sending data to Kafka topic '{TOPIC}'...")
    while True:
        event = generate_event()
        producer.send(TOPIC, event)
        print(f"Sent: {event}")
        time.sleep(1)
