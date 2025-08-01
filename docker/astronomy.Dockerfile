# Use AWS Lambda Python base image
ARG ARCHITECTURE="arm64"
FROM public.ecr.aws/lambda/python:3.8-${ARCHITECTURE}

# Install OS deps and Python requirements in one layer
WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./
RUN yum install -y gcc postgresql-devel \
    && pip install -r requirements.txt \
    && yum clean all

# Copy only the files you need into src/
COPY src/extract_astronomy_data.py   .
COPY src/transform_astronomy_data.py .
COPY src/load_astronomy_data.py      .
COPY src/pipeline_astronomy_data.py  .
COPY src/astronomy_utils.py .

# Tell Lambda to invoke the handler inside the src package
CMD ["pipeline_astronomy_data.handler"]