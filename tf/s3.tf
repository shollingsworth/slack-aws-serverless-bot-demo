resource "aws_s3_bucket" "bucket" {
  bucket_prefix = local.prefix
}

resource "aws_s3_bucket_server_side_encryption_configuration" "enc" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
resource "aws_s3_bucket_acl" "acl" {
  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}

# uncomment for versioning
# resource "aws_s3_bucket_versioning" "versioning" {
#   bucket = aws_s3_bucket.bucket.id
#   versioning_configuration {
#     status = "Disabled"
#   }
# }

resource "aws_s3_bucket_public_access_block" "pubaccess" {
  bucket                  = aws_s3_bucket.bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket" {
  value = aws_s3_bucket.bucket.id
}
