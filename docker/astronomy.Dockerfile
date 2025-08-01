# Use AWS Lambda Python base image
ARG ARCHITECTURE="arm64"
FROM public.ecr.aws/lambda/python:3.8-${ARCHITECTURE}

# Install OS deps and Python requirements in one layer
WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./

# we specifically need libpq v10+ as it supports SCRAM authentication
# AWS linux links against an older PGSQL version that only supports MD5 auth
# SCRAM auth is used by our Python drivers, so it's easier to do this and just update libpq
# the line below enables postgresql10 specifically as the default postgresql package is too old
RUN yum install -y gcc \
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