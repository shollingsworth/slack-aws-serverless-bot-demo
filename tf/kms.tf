resource "aws_kms_key" "crypt_key" {
  description = local.prefix
  is_enabled = true
}

resource "aws_kms_alias" "crypt_alias" {
  name = "alias/${local.prefix}"
  target_key_id = aws_kms_key.crypt_key.id
}
