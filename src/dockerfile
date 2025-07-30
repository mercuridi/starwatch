# Dockerfile for the astronomy script
# Must be run from top-level

# Get base image from AWS
FROM public.ecr.aws/lambda/python:3.13

# Move to the lambda task root directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Copy source code
COPY src/extract_astronomy_data.py .
COPY src/transform_astronomy_data.py .
COPY src/load_astronomy_data.py .
COPY src/pipeline_astronomy_data.py .

# Expects a function called `handler` in `pipeline_astronomy_data.py`
# Required function signature:
# `def handler(event, context):`
CMD ["pipeline_astronomy_data.handler"]