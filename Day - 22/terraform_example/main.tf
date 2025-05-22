provider "aws" {
  region = "us-east-1"  # Change to your desired region
  # You can also set the region using environment variables
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "my-unique-example-bucket-name-1234567890"
  acl    = "private"

  tags = {
    Name        = "MyExampleBucket"
    Environment = "Dev"
  }
}
