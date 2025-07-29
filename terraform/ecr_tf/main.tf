provider "aws" {
  region  = var.aws_region
}

resource "aws_ecr_repository" "c18-starwatch-ecr" {
  name                 = var.ecr_name
  image_tag_mutability = "MUTABLE"
}