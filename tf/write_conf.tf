resource "local_file" "resource_out" {
    content  = jsonencode({
      "role": aws_iam_role.role.arn,
      "bucket": aws_s3_bucket.bucket.id,
    })
    filename = "${path.module}/../aws_resources.json"
}
