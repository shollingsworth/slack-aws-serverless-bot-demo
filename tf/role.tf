data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "inline_role_policy" {
  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = ["arn:aws:lambda:${local.region}:${data.aws_caller_identity.current.account_id}:function:${local.prefix}*"]
  }

  statement {
    effect    = "Allow"
    actions   = [
      "ssm:GetParameters",
      "ssm:GetParameter",
    ]
    resources = ["arn:aws:ssm:${local.region}:${data.aws_caller_identity.current.account_id}:parameter/${local.prefix}*"]
  }

  statement {
    effect    = "Allow"
    actions   = [
      "kms:Decrypt",
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:${local.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.prefix}*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:*",
    ]
    resources = [
      aws_s3_bucket.bucket.arn,
      "${aws_s3_bucket.bucket.arn}/*",
    ]
  }
}

resource "aws_iam_role" "role" {
  name               = "${local.prefix}-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
  inline_policy {
    name   = "inline-policy"
    policy = data.aws_iam_policy_document.inline_role_policy.json
  }
}

output "role" {
  value = aws_iam_role.role.arn
}
