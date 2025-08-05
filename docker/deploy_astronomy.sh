# 1) Authenticate Docker to ECR registry
aws ecr get-login-password \
  --region eu-west-2 \
| docker login \
  --username AWS \
  --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
echo "AWS authenticated"

# 2) Build ARM64 image
docker buildx build . \
  --provenance=false \
  --platform linux/arm64 \
  --file docker/astronomy.Dockerfile \
  --tag 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline
echo "Building new image"

# 3) Push it up to ECR
docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline
echo "Image pushed to AWS"

# 4) Update the lambda function code with the new image
aws lambda update-function-code \
  --function-name c18-starwatch-etl-lambda \
  --image-uri 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline \
  --region eu-west-2
echo "Lambda function code updated"