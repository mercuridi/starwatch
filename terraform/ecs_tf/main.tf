# Specify region
provider "aws" {
  region = "eu-west-2"
}

# Reference existing VPC
data "aws_vpc" "c18-vpc" {
 id = "vpc-0adcb6a62ca552c01"
}

# Reference existing subnet 1
data "aws_subnet" "subnet_1" {
  id = "subnet-0aed07ac008a10da9"
}

# Reference existing subnet 2
data "aws_subnet" "subnet_2" {
  id = "subnet-0f10662561eade8c3"
}

# Security group for ECR
resource "aws_security_group" "c18-starwatch-dashboard-ecr-sg" {
  name        = "c18-starwatch-dashboard-ecr-sg"
  description = "Allow inbound access to dashboard"
  vpc_id      = data.aws_vpc.c18-vpc.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create ECR repo for dashboard container image
resource "aws_ecr_repository" "c18-starwatch-dashboard-ecr" {
  name                 = "c18-starwatch-dashboard-ecr"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name = "c18-starwatch-dashboard"
  }
}

# Reference existing c18 ECS cluster for dashboard task
data "aws_ecs_cluster" "c18-cluster" {
  cluster_name = "c18-ecs-cluster"
}

# Creates service to run container
resource "aws_ecs_service" "c18-starwatch-dashboard-service" {
  name            = "c18-starwatch-dashboard-service"
  cluster         = data.aws_ecs_cluster.c18-cluster.arn
  task_definition = aws_ecs_task_definition.c18-starwatch-td.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets         = [data.aws_subnet.subnet_1.id, data.aws_subnet.subnet_2.id]
    assign_public_ip = true
    security_groups = [aws_security_group.c18-starwatch-dashboard-ecr-sg.id]
  }
}

# Allow ECS to pull image and run tasks
resource "aws_iam_role" "c18-starwatch-ecs-task-exec-role" {
  name = "c18-starwatch-ecs-task-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "c18-starwatch-ecs_task_exec-policy" {
  role       = aws_iam_role.c18-starwatch-ecs-task-exec-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


resource "aws_ecs_task_definition" "c18-starwatch-td" {
  family                   = "c18-starwatch-da-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn = aws_iam_role.c18-starwatch-ecs-task-exec-role.arn

  container_definitions = jsonencode([
    {
      name      = "c18-starwatch-dashboard-container"
      image = "${aws_ecr_repository.c18-starwatch-dashboard-ecr.repository_url}:latest"
      essential = true
      portMappings = [{
        containerPort = 8501
        protocol      = "tcp"
      }]
    }
  ])
}
