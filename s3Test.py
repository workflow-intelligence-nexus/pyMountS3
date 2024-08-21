import boto3
import os
from botocore.exceptions import ClientError

# AWS S3 configuration
bucket_name = 'runpodbkups'
file_name = 'test_file_10kb.txt'
local_file_path = '/tmp/' + file_name
downloaded_file_path = '/tmp/downloaded_' + file_name

# Create an S3 client
s3 = boto3.client('s3')

def create_test_file():
    """Create a 10KB test file"""
    with open(local_file_path, 'w') as f:
        f.write('0' * 10240)  # Write 10KB of data

def upload_file():
    """Upload the file to S3"""
    try:
        s3.upload_file(local_file_path, bucket_name, file_name)
        print(f"File uploaded successfully to {bucket_name}/{file_name}")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def download_file():
    """Download the file from S3"""
    try:
        s3.download_file(bucket_name, file_name, downloaded_file_path)
        print(f"File downloaded successfully to {downloaded_file_path}")
    except ClientError as e:
        print(f"Error downloading file: {e}")

def verify_file():
    """Verify the downloaded file"""
    original_size = os.path.getsize(local_file_path)
    downloaded_size = os.path.getsize(downloaded_file_path)
    
    if original_size == downloaded_size == 10240:
        print("File size verified: 10KB")
    else:
        print(f"File size mismatch. Original: {original_size}, Downloaded: {downloaded_size}")

def cleanup():
    """Remove local files"""
    os.remove(local_file_path)
    os.remove(downloaded_file_path)
    print("Local files cleaned up")

def main():
    create_test_file()
    upload_file()
    download_file()
    verify_file()
    cleanup()

if __name__ == "__main__":
    main()