# 🚀 Real-Time Analytics Platform with FastAPI, Kafka, and AWS Integration

This project demonstrates a **cloud-ready, event-driven analytics pipeline** of my docker-demo built with **FastAPI**, **Kafka**, and the **ELK Stack (Elasticsearch, Logstash, Kibana)** — that was deployed and integrated with **Amazon Web Services (AWS)**.

It showcases my ability to design, deploy, and manage scalable data systems in both **containerized** and **cloud-native** environments using **AWS S3**, **EC2**, and **SageMaker**.


## ⚡ TL;DR — Portfolio Projects Overview

1. **Elasticsearch + Kibana (Docker Compose)** – Containerized stack for real-time data monitoring, search, and interactive dashboards.  
2. **Kafka + Logstash + Data Generator (Docker Compose)** – End-to-end streaming pipeline that ingests, processes, and prepares data for analytics or ML workflows.  
3. **FastAPI + Docker + AWS Cloud** – Cloud-ready API for real-time data ingestion, integrated with S3 storage, EC2 deployment, and SageMaker ML model training.


---

📍 **In short:**  
> I design and deploy **cloud-native, data-driven applications** that combine **APIs, streaming systems, and machine learning**, using **AWS + Docker + FastAPI**.

---

## 🧭 Architecture Overview

```bash
[ FastAPI Service (EC2) ]
│
▼
[ Kafka Topic ]
│
▼
[ Logstash Consumer ]
│
▼
[ Elasticsearch / Kibana (AWS OpenSearch) ]
│
└──► [ S3 Data Backup + SageMaker ML Training ]
```


---

## ☁️ Cloud Experience: AWS Integration

This project leverages multiple AWS services to demonstrate cloud proficiency and scalability.

| AWS | Purpose | What I do                                                                          |
|-------------|----------|------------------------------------------------------------------------------------|
| **Amazon EC2** | Hosts Dockerized FastAPI, Kafka, and Logstash services | Configured Ubuntu EC2 instances, managed Docker & Compose deployments              |
| **Amazon S3** | Centralized data lake for raw events and processed data | Automated data export from Elasticsearch to S3 using Logstash output plugin        |
| **Amazon SageMaker** | Machine learning model training and inference on ingested data | Used S3 data snapshots to train predictive models and deployed inference endpoints |
| **AWS IAM** | Managed access between EC2, S3, and SageMaker securely | Created roles and policies for least-privilege permissions                         |
| **AWS CloudWatch** | Monitored metrics and logs across EC2 and containers | Configured log shipping and performance alerts                                     |
| **AWS CLI / SDK (boto3)** | Automated interactions with AWS resources | Used in FastAPI and SageMaker scripts for data handling                            |

---

## 💡 Key Highlights

- Designed an **end-to-end data streaming architecture** using Kafka and Logstash  
- Integrated **AWS S3** for persistent and scalable data storage  
- Deployed the entire application stack on **AWS EC2** with my demo license 
- Leveraged **SageMaker** for ML model training and batch inference using S3 data exports  
- Built **REST APIs with FastAPI** for event ingestion and analytics queries  
- Implemented **Elasticsearch dashboards in Kibana** for real-time monitoring and insights  

---

## 🧰 Tech Stack

| Layer | Technology |
|--------|-------------|
| **API** | FastAPI (Python 3.11) |
| **Streaming** | Apache Kafka |
| **Data Processing** | Logstash |
| **Data Storage** | Elasticsearch (on AWS OpenSearch) |
| **Visualization** | Kibana |
| **Cloud Platform** | AWS EC2, S3, SageMaker |
| **Containerization** | Docker, Docker Compose |
| **Monitoring** | AWS CloudWatch |
| **Infrastructure** | Terraform / AWS CLI  |

---

## ⚙️ FastAPI Features

- `/events` → Publish real-time user events (purchases, views, clicks) to Kafka  
- `/stats` → Query aggregated analytics from Elasticsearch  
- `/train-model` *(optional)* → Trigger SageMaker model training from S3 data  
- `/predict` *(optional)* → Get ML predictions from deployed SageMaker endpoint  

### Example Request (POST /events)

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"user_id": 101, "event_type": "purchase", "amount": 59.99}'
```

### Example Response

```bash
{
  "status": "success",
  "data": {
    "user_id": 101,
    "event_type": "purchase",
    "amount": 59.99
  }
}
```
---

## ☁️ AWS Deployment Workflow
### 1️⃣ EC2 Deployment

- Created and configured Ubuntu EC2 instance
- Installed Docker, Docker Compose, and AWS CLI
- Pulled application source from GitHub
- Launched all services
    ```bash
    docker-compose up -d
    ```
- Configured security groups for ports 8000, 9092, 9200, 5601

### 2️⃣ S3 Data Lake Integration

Configured Logstash output to export Elasticsearch indices to Amazon S3

Example Logstash output snippet:

```bash
output {
  s3 {
    access_key_id => "${AWS_ACCESS_KEY_ID}"
    secret_access_key => "${AWS_SECRET_ACCESS_KEY}"
    region => "us-east-1"
    bucket => "my-analytics-data"
    prefix => "events/"
  }
}
```

Data automatically lands in S3 for analytics or ML training

### 3️⃣ SageMaker Integration

- Imported S3 dataset into SageMaker notebook instance
- Trained regression/classification model on user behavior data
- Deployed model as a real-time inference endpoint

Example (Python using boto3):

```bash
import boto3

sagemaker = boto3.client("sagemaker-runtime", region_name="us-east-1")

response = sagemaker.invoke_endpoint(
    EndpointName="event-predictor",
    ContentType="application/json",
    Body=json.dumps({"amount": 59.99, "event_type": "purchase"})
)

print(response["Body"].read().decode())
```

---

## 🧹 Cleanup
To stop services and clean resources:
```bash
docker-compose down -v
aws s3 rm s3://my-analytics-data --recursive
aws sagemaker delete-endpoint --endpoint-name event-predictor
```

---

## 📜 License

Created for educational and development purposes.

---

## ✨ Author

Hashaam Ahsan
hashaamahsan@gmail.com