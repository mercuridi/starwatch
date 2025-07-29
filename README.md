# StarWatch
## Project introduction
StarWatch is a complete dashboarding service for the amateur astronomer.

Quickly get insights to your favourite constellations and information on the best evenings to stargaze, all automatically adapted to your choice of location.

## File structures
- .github
    - Contains github-related utilities including CI/CD instructions.
- assets
    - Contains useful utility files for other parts of the project.
    - eg. architecture diagrams
- data
    - Contains data dumps for project scripts.
- src
    - Contains source code for the different pipelines of the project.
- test
    - Contains various tests for the different scripts in the project.
- Top level
    - Contains utility files for the project.

## Data sources
- [Meteo Weather API](https://open-meteo.com/en/docs)
    - No verification required
- [Astronomy API](https://astronomyapi.com/)
    - Requires API keys in a `.env` file to work. API keys must be obtained from Astronomy API directly.

## How to run
Ensure you have Python 3 installed. Recommended version minimum 3.10 (matches CI/CD Pytest harness)
In your terminal at the top level of the project:
1. Install requirements: `pip3 install -r requirements.txt`
2. Run pytest: `python3 -m pytest test/`
3. Run pytest coverage checks: `python3 -m pytest --cov=src test/`
4. Run pylint: `python3 -m pylint *.py`

### Terraform
This folder contains two files: `main.tf` and `variables.tf`

#### `main.tf`
Setups the necessary security groups, subnet group and a database instance to provision an RDS instance on AWS.

#### `variables.tf`
Defines the variables needed (including the db credentials) to provision the RDS instance.

**Prerequisites:**

`terraform.tfvars` file containing:

```
aws_region        = your_aws_region

private_subnet_ids = [your_list_of_public_subnet_ids]

db_identifier      = your_sql_server_host
db_name        = your_database_name
db_username    = your_database_username
db_password    = your_database_password

```
