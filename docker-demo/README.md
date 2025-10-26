# 🔥 Real-Time Data Pipeline with Kafka, Logstash, Elasticsearch, and Kibana

This project demonstrates a **complete real-time data pipeline** built using **Kafka**, **Logstash**, **Elasticsearch**, and **Kibana** — powered by **Docker Compose**.  
A lightweight **Python data generator** continuously pushes simulated JSON events to Kafka, which Logstash consumes and indexes into Elasticsearch for real-time visualization in Kibana.

---

## ⚡ TL;DR — Portfolio Projects Overview

1. **Elasticsearch + Kibana (Docker Compose)** – Containerized stack for real-time data monitoring, search, and interactive dashboards.  
2. **Kafka + Logstash + Data Generator (Docker Compose)** – End-to-end streaming pipeline that ingests, processes, and prepares data for analytics or ML workflows.

---

📍 **In short:**  
> I design and deploy **data-driven applications** that combine **APIs and streaming systems**, using **Docker + FastAPI**.

## 🏗️ Architecture

```bash
Data Generator → Kafka → Logstash → Elasticsearch → Kibana
```

### Components

| Service | Description |
|----------|-------------|
| **Zookeeper** | Coordinates Kafka brokers |
| **Kafka** | Message queue that stores event streams |
| **Logstash** | Consumes Kafka messages and indexes them into Elasticsearch |
| **Elasticsearch** | Stores and indexes incoming data |
| **Kibana** | Visualization dashboard for Elasticsearch data |
| **Data Generator** | Python script that sends random JSON events to Kafka |

---

## 📂 Project Structure

```bash
docker-demo/
├── docker-compose.yml
├── logstash/
│ └── logstash.conf
├── elasticsearch/
│ └── elasticsearch.yml
├── kibana/
│ └── kibana.yml
├── data-generator/
│ └── producer.py
│ └── requirements.txt
│ └── Dockerfile
├── fastapi-app/
│ └── main.py
│ └── requirements.txt
│ └── Dockerfile
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Start the Pipeline

Run the full stack using Docker Compose:

```bash
docker-compose up -d
```

This will spin up:

- Zookeeper
- Kafka
- Logstash
- Elasticsearch
- Kibana
- data-generator
- fastapi-app

🕓 Wait about 30–60 seconds for all services to initialize.


### 2️⃣ Create the Kafka Topic
(Optional — Logstash will create it automatically on most setups)
```bash
docker exec -it kafka kafka-topics --create --topic raw-data --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1
```

### 3️⃣ View Data in Kibana

- Open http://localhost:5601 
- Navigate to Stack Management → Index Patterns
- Create a new pattern
- kafka-data-*

Explore your live data in Discover or create visualizations.

### 4️⃣ Play with FastApi

- Open http://localhost:8000/docs
- Open POST tab
- Click "Try it Out" button on the right and go crazy 

---

## 🧹 Cleanup

To stop and remove all containers:

```bash
docker-compose down
```

To remove all data volumes as well:
```bash
docker-compose down -v
```
---

## ⚠️ Troubleshooting

| Issue                                     | Solution                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Kibana can’t connect to Elasticsearch** | Ensure `xpack.security.enabled=false` in `elasticsearch.yml`                                |
| **Producer can’t connect to Kafka**       | Ensure you use `localhost:9092` for local Python scripts, `kafka:9092` inside Docker        |
| **Data not showing in Kibana**            | Wait for Logstash to consume messages or check Logstash logs with `docker logs -f logstash` |


---

## 📜 License

Created for educational and development purposes.

---

## ✨ Author

Hashaam Ahsan
hashaamahsan@gmail.com

