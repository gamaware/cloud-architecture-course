import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region='us-east-1'):
    """
    Create an S3 bucket with versioning and encryption enabled.

    Args:
        bucket_name (str): Name of the bucket to create
        region (str): AWS region (default: us-east-1)

    Returns:
        bool: True if successful, False otherwise
    """
    s3_client = boto3.client('s3', region_name=region)

    try:
        # Create bucket
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"✓ S3 bucket '{bucket_name}' created successfully")

        # Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print("✓ Versioning enabled")

        # Enable encryption
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )
        print("✓ Encryption (AES-256) enabled")

        # Block public access
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print("✓ Public access blocked")

        return True

    except ClientError as e:
        print(f"✗ Error: {e}")
        return False

def upload_file(bucket_name, file_path, object_name=None):
    """
    Upload a file to an S3 bucket.

    Args:
        bucket_name (str): Bucket to upload to
        file_path (str): File to upload
        object_name (str): S3 object name (default: same as file_path)

    Returns:
        bool: True if successful, False otherwise
    """
    if object_name is None:
        object_name = file_path

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"✓ File '{file_path}' uploaded as '{object_name}'")
        return True
    except ClientError as e:
        print(f"✗ Error uploading file: {e}")
        return False

def list_bucket_objects(bucket_name):
    """
    List all objects in an S3 bucket.

    Args:
        bucket_name (str): Name of the bucket
    """
    s3_client = boto3.client('s3')

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            print(f"\nObjects in bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print(f"Bucket '{bucket_name}' is empty")

    except ClientError as e:
        print(f"✗ Error listing objects: {e}")

def delete_bucket(bucket_name):
    """
    Delete an S3 bucket and all its contents.

    Args:
        bucket_name (str): Name of the bucket to delete
    """
    s3_client = boto3.client('s3')

    try:
        # Delete all objects first
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"✓ Deleted object: {obj['Key']}")

        # Delete the bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"✓ Bucket '{bucket_name}' deleted successfully")

    except ClientError as e:
        print(f"✗ Error deleting bucket: {e}")

if __name__ == "__main__":
    # Configuration
    BUCKET_NAME = 'an-2026-boto3-jag'  # Change this to your initials!
    REGION = 'us-east-1'

    # Create bucket
    print("Creating S3 bucket...")
    if create_s3_bucket(BUCKET_NAME, REGION):
        print(f"\n✓ Bucket '{BUCKET_NAME}' is ready!\n")

        # Create and upload a test file
        test_file = 'test-boto3.txt'
        with open(test_file, 'w') as f:
            f.write('Hello from Boto3!')

        upload_file(BUCKET_NAME, test_file)

        # List bucket contents
        list_bucket_objects(BUCKET_NAME)

        # Cleanup (uncomment to delete)
        # print("\nCleaning up...")
        # delete_bucket(BUCKET_NAME)
