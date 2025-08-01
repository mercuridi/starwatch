# 1) Authenticate Docker to ECR registry
aws ecr get-login-password \
  --region eu-west-2 \
| docker login \
  --username AWS \
  --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com

# 2) Build ARM64 image
docker buildx build . \
  --provenance=false \
  --platform linux/arm64 \
  --file docker/astronomy.Dockerfile \
  --tag 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline

# 3) Push it up to ECR
docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline