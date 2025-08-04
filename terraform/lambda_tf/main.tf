provider "aws" {
  region = var.aws_region
}

# IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec_role" {
  name = "c18-starwatch-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
resource "aws_iam_role_policy_attachment" "lambda_vpc_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Security group for Lambda
resource "aws_security_group" "lambda_sg" {
  name        = "c18-starwatch-lambda-sg"
  description = "Allow Lambda to connect to RDS SQL Server"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Lambda Function from ECR Image
resource "aws_lambda_function" "image_lambda" {
  function_name = "c18-starwatch-etl-lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"

  # change below as required
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c18-starwatch-ecr:astronomy_pipeline"
  timeout       = 120
  memory_size   = 512

  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_PORT     = var.DB_PORT
      DB_USER     = var.DB_USER
      DB_PASSWORD = var.DB_PASSWORD
      DB_NAME     = var.DB_NAME
      DB_SCHEMA   = var.DB_SCHEMA
    }
  }
  vpc_config {
    subnet_ids         = [var.private_subnet_id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
}

# IAM Role for EventBridge Scheduler
resource "aws_iam_role" "eventbridge_scheduler_role" {
  name = "c18-starwatch-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "scheduler.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "scheduler_invoke_lambda" {
  name = "c18-starwatch-scheduler-policy"
  role = aws_iam_role.eventbridge_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = aws_lambda_function.image_lambda.arn
    }]
  })
}

# EventBridge Schedule (disabled at first)
resource "aws_scheduler_schedule" "lambda_every_minute" {
  name       = "c18-starwatch-lambda-schedule"
  group_name = "default"

  # change below settings as needed
  schedule_expression = "rate(1 minute)"
  state               = "DISABLED"  # Change to ENABLED once ready

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.image_lambda.arn
    role_arn = aws_iam_role.eventbridge_scheduler_role.arn
  }
}

# Getting Lambda internet access
data "aws_internet_gateway" "existing_igw" {
  filter {
    name   = "attachment.vpc-id"
    values = [var.vpc_id]
  }
}

resource "aws_eip" "nat_eip" {}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = var.public_subnet_id
  depends_on    = [data.aws_internet_gateway.existing_igw]
}

resource "aws_route_table" "private_rt" {
  vpc_id = var.vpc_id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
}