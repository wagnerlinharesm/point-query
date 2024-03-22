provider "aws" {
  region = var.region
}
# -- lambda

resource "aws_iam_role" "point_query_iam_role" {
  name               = "point_query_iam_role"
  assume_role_policy = file("iam/policy/assume_role_policy.json")
}

resource "aws_iam_role_policy" "point_query_policy" {
  name = "point_query_policy"
  role = aws_iam_role.point_query_iam_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "secretsmanager:GetSecretValue",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "point_query_lambda_function" {
  function_name = "point_query"
  handler       = "app/lambda_function.handler"
  runtime       = "python3.11"
  role          = aws_iam_role.point_query_iam_role.arn

  filename = "lambda_function.zip"

  source_code_hash = filebase64sha256("lambda_function.zip")

  vpc_config {
    subnet_ids         = ["subnet-0ff65a2cef8cdbbdb", "subnet-0c9e1d22c842d362b", "subnet-08e43d2d7fa2c463e"]
    security_group_ids = ["sg-01f81ec455ea45da9"]
  }

  depends_on = [
    aws_iam_role.point_query_iam_role
  ]

  environment {
    variables = {
      DB_HOST = "rdsproxy.proxy-cqivfynnpqib.us-east-2.rds.amazonaws.com",
      POINT_DB_USERNAME           = local.point_db_credentials["username"]
      POINT_DB_PASSWORD           = local.point_db_credentials["password"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "point_report_ec2_iam_role_policy_attachment" {
  role       = aws_iam_role.point_query_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

data "aws_secretsmanager_secret" "point_db_secretsmanager_secret" {
  name = var.point_db_secretsmanager_secret_name
}

data "aws_secretsmanager_secret_version" "point_db_secretsmanager_secret_version" {
  secret_id = data.aws_secretsmanager_secret.point_db_secretsmanager_secret.id
}

locals {
  point_db_credentials  = jsondecode(data.aws_secretsmanager_secret_version.point_db_secretsmanager_secret_version.secret_string)
}

variable "point_db_secretsmanager_secret_name" {
  type    = string
  default = "mikes/db/db_credentials"
}
