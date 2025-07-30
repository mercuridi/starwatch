variable "aws_region" {
  description = "The AWS region to use"  
  type = string
}

variable "public_subnet_ids" {
  description = "The public subnets to use"
  type = list(string)
}

variable "db_identifier" {
  description = "The database identifier"  
  type = string
}

variable "db_name" {
  description = "The database name"
  type = string
}

variable "db_username" {
  description = "The database username"
  type = string
}

variable "db_password" {
  description = "The database password"
  type = string
  sensitive = true
}

variable "db_port" {
  description = "The database port"
}