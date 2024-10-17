# Base image
FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy model and app script
COPY best_model.pkl .
COPY deployed_ml_app.py .

ENTRYPOINT ["python", "deployed_ml_app.py"]

