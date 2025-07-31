# Dockerfile for the dashboard ECS service
# Must be run from top-level

# Get base Python image
FROM python:3.10

# Copy requirements
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Make file structure
RUN mkdir src
RUN mkdir dashboard

# Copy source code
COPY src/extract_weather.py src
COPY src/transform_weather.py src
COPY dashboard/dashboard.py dashboard

# Run dashboard
RUN python3 dashboard.py