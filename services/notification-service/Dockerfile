FROM python:3.11-slim

WORKDIR /notification-service

RUN apt-get update && apt-get install -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY run.py .

# Run the app
CMD ["python", "run.py"]
