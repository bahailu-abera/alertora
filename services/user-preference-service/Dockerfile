FROM python:3.11-slim

# Set work directory
WORKDIR /user-preference-service

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Run the service
CMD ["python",  "-u", "run.py"]
