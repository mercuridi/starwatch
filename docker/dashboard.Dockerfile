FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src/
COPY dashboard/ dashboard/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python3", "-m", "streamlit", "run", "dashboard/dashboard.py", "--server.port=8501"]
