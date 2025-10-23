from datetime import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

import time
import json
import os

app = FastAPI(title="Real-Time Analytics API")

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch:9200")

# Initialize Kafka and Elasticsearch
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
es = Elasticsearch([ELASTICSEARCH_HOST])

TOPIC = "raw-data"


# Pydantic schema
class Event(BaseModel):
    user_id: int
    event_type: str
    amount: float


@app.get("/")
def root():
    time.sleep(30)
    return {"message": "Real-Time Analytics API is running 🚀"}


@app.post("/events")
def publish_event(event: Event):
    """Publish an event to Kafka."""
    try:
        event_data = event.dict()
        producer.send(TOPIC, event_data)
        producer.flush()
        return {"status": "success", "data": event_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats():
    """Retrieve aggregated data from Elasticsearch."""
    try:
        body = {
            "size": 0,
            "aggs": {
                "by_event_type": {
                    "terms": {"field": "event_type.keyword"}
                },
                "total_amount": {
                    "sum": {"field": "amount"}
                }
            }
        }
        res = es.search(index="kafka-data-*", body=body)
        return {
            "event_counts": res["aggregations"]["by_event_type"]["buckets"],
            "total_amount": res["aggregations"]["total_amount"]["value"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
