# Terraform configuration for AWS resources

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "optimizer_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = "optimizer-agent"
  }
}

resource "aws_security_group" "optimizer_sg" {
  name        = "optimizer-sg"
  description = "Allow HTTP and SSH access"
  ingress = [
    {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
  egress = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}

resource "aws_s3_bucket" "cost_reports" {
  bucket = var.cost_report_bucket
  acl    = "private"
}
