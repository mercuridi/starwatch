<img width="1060" height="204" alt="image" src="https://github.com/user-attachments/assets/16495107-028c-407a-8a8f-3b1c23630f15" />

# StarWatch
## Project introduction
StarWatch is a complete dashboarding service for the amateur astronomer.

Quickly get insights to your favourite constellations and information on the best evenings to stargaze, all automatically adapted to your choice of location.

## File structures
- .github
    - Contains github-related utilities including CI/CD instructions.
- assets
    - Contains useful utility files for other parts of the project.
- dashboard
    - Contains the source code for *only* the user-facing dashboard.
- data
    - Contains data dumps for project scripts.
- docker
    - Contains dockerfiles and deploy scripts for containerisation of the project.
- src
    - Contains source code for the different pipelines of the project.
- terraform
    - Contains various terraform files for different provisioned AWS resources
- test
    - Contains various tests for the different scripts in the project.
- Top level
    - Contains utility files for the project.

## Data sources
- [Meteo Weather API](https://open-meteo.com/en/docs)
    - No verification required
- [Astronomy API](https://astronomyapi.com/)
    - Requires API keys in a `.env` file to work. API keys must be obtained from Astronomy API directly.
- [AuroraWatchUK](https://aurorawatch.lancs.ac.uk/api-info/0.2/)
    - No verification required
- [NASA](https://api.nasa.gov/)
    - Requires API keys in a `.env` file to work. API keys must be obtained from NASA directly.
- [Open Notify ISS Current Location](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)
    - No verification required
- [Ariss](https://live.ariss.org/iss.txt)
    - No verification required

## How to run
Ensure you have Python 3 installed. Recommended version minimum 3.10 (matches CI/CD Pytest harness)
In your terminal at the top level of the project:
1. Install requirements: `pip3 install -r requirements.txt`

There are many things you may wish to do with the project:
- Run pytest: `python3 -m pytest test/`
- Run pytest coverage checks: `python3 -m pytest --cov=src --cov-report term-missing test/`
- Run pylint: `python3 -m pylint *.py`

- Build the docker image for the astronomy pipeline:
```
docker buildx build . --provenance=false --platform=linux/arm64 --no-cache --tag astronomy_pipeline:latest --file docker/astronomy.Dockerfile
```
- Build the docker image for the dashboard:
```
docker buildx build . --provenance=false --platform=linux/arm64 --no-cache --tag astronomy_pipeline:latest --file docker/dashboard.Dockerfile
```
- Directly deploy the astronomy pipeline to AWS (build and push): `docker/deploy_astronomy.sh`
    - Warning!!! Pushing the image to ECR will *not* update any linked Lambdas. You need to make sure the Lambda is using the updated image yourself. **Terraform will not do this for you!!!**

## Terraform
This folder contains the sub-folders: `rds_tf`, `lambda_tf`, `ecs_tf`, and `ecr_tf`.

All sub-folders contain contains two files: `main.tf` and `variables.tf`

#### `main.tf`
Set ups the necessary terraform resources.

#### `variables.tf`
Defines the variables associated with each resource.

**Prerequisites:**

A `terraform.tfvars` file must be created within each folder. 

The variables to define for each resource are found in the `variables.tf` files in each folder.

