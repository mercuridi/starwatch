provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "c18-starwatch-s3" {
    bucket = var.s3_bucket_name

  tags = {
    Name        = "c18-starwatch-s3"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.c18-starwatch-s3.id
  # keeps bucket secure by disabling public access
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}