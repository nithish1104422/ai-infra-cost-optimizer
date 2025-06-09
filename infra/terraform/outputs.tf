# Terraform output definitions

output "optimizer_instance_id" {
  description = "The ID of the EC2 instance running the optimizer agent"
  value       = aws_instance.optimizer_ec2.id
}

output "optimizer_instance_public_ip" {
  description = "The public IP address of the optimizer EC2 instance"
  value       = aws_instance.optimizer_ec2.public_ip
}

output "cost_report_bucket_name" {
  description = "The name of the S3 bucket for storing cost reports"
  value       = aws_s3_bucket.cost_reports.id
}
