# starwatch

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

