FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ipnet_demo ./ipnet_demo
EXPOSE 8000

CMD ["uvicorn", "ipnet_demo.api:app", "--host", "0.0.0.0", "--port", "8000"]
