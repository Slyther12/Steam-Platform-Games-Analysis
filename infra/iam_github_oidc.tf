# ---------------------------------------------------------
# ⬇️ PASTE THIS AT THE BOTTOM OF infra/iam_github_oidc.tf
# ---------------------------------------------------------

resource "aws_iam_role_policy" "github_actions_permissions" {
  name = "github-actions-permissions"
  role = aws_iam_role.github_actions_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowS3Access"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        # Dynamically permissions ONLY for your specific bucket
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      },
      {
        Sid    = "AllowGlueJobExecution"
        Effect = "Allow"
        Action = [
          "glue:StartJobRun",
          "glue:GetJobRun",
          "glue:GetJobRuns",
          "glue:BatchStopJobRun"
        ]
        Resource = "*"
      }
    ]
  })
}
