aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com

docker buildx build . --provenance=false --platform=linux/arm64 --tag 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline --file docker/astronomy.Dockerfile

docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline