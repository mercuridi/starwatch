# Dockerfile for the dashboard ECS service
# Must be run from top-level

# Start from lambda Python3.8 image
FROM python:3.11

# Copy requirements
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Make file structure
RUN mkdir src
RUN mkdir dashboard

# Copy source code
COPY src/extract_weather.py src/
COPY src/transform_weather.py src/
COPY dashboard/dashboard.py dashboard

# Open streamlit port
EXPOSE 8501 

# Check it's working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run dashboard
#ßß ENTRYPOINT configures an executable container
ENTRYPOINT ["python3", "-m", "streamlit", "run", "dashboard/dashboard.py", "--server.port=8501"]
