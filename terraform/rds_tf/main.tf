provider "aws" {
  region  = var.aws_region
}

resource "aws_db_subnet_group" "c18-starwatch-public-subnet-group" {
  name       = "c18-starwatch-public-subnet-group"
  subnet_ids = var.public_subnet_ids

  tags = {
    Name = "c18-starwatch-public-subnet-group"
  }
}

resource "aws_security_group" "c18-starwatch-security-group" {
  name        = "c18-starwatch-sg"
  description = "Allow DB access"
  vpc_id      = "vpc-0adcb6a62ca552c01"

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
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

resource "aws_db_instance" "c18-starwatch-rds" {
  identifier         = var.db_identifier
  allocated_storage  = 20 # GiB
  engine             = "postgres"
  engine_version     = "17.2"
  instance_class     = "db.t3.micro"
  username           = var.db_username
  password           = var.db_password
  port               = var.db_port
  vpc_security_group_ids = [aws_security_group.c18-starwatch-security-group.id]
  db_subnet_group_name   = aws_db_subnet_group.c18-starwatch-public-subnet-group.name
  publicly_accessible    = true
  skip_final_snapshot    = true

  tags = {
    Name = "c18-starwatch-rds"
  }
}