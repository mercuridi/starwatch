variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to use"  
  type = string
}

variable "ecr_name" {
  description = "ECR repository name"
  type        = string
}

variable "vpc_id" {
    description = "ID for the VPC to use"
    type = string
}

variable "private_subnet_id" {
  description = "Private subnet ID to host Lambda"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID for NAT Gateway"
  type        = string
}

variable "DB_HOST" {
  description = "IP to access the RDS"
  type        = string
}
variable "DB_PORT" {
  description = "Port for MS SQLServer"
  type        = string
}
variable "DB_USER" {
  description = "Group-specific username for RDS"
  type        = string
}
variable "DB_PASSWORD" {
  description = "Group-specific password for RDS"
  type        = string
}
variable "DB_NAME" {
  description = "Database name for RDS"
  type        = string
}
variable "DB_SCHEMA" {
  description = "Group-specific schema for RDS"
  type        = string
}

variable "APPLICATION_ID" {
    description = "Application ID secret for Astronomy API"
    type = string
}

variable "APPLICATION_SECRET" {
    description = "Application Secret secret for Astronomy API"
    type = string
}