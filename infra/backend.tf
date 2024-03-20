terraform {
  backend "s3" {
    bucket = "point-terraform-state"
    key    = "point-query.tfstate"
    region = "us-east-2"
    encrypt = true
  }
}
