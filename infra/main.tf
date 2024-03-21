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

  depends_on = [
    aws_iam_role.point_query_iam_role
  ]

  environment {
    variables = {
      DB_HOST = "rdsproxy.proxy-cqivfynnpqib.us-east-2.rds.amazonaws.com",
      DB_SECRET = "mikes/db/db_credentials"
    }
  }
}
