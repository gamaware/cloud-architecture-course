# Task 3: Python Boto3 SDK

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Boto3](https://img.shields.io/badge/Boto3-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

## Overview

Boto3 is the AWS SDK for Python, enabling programmatic access to AWS services. It's ideal for complex automation
and application integration.

## Step 1: Install Python

### macOS

Python 3 comes pre-installed on most macOS versions. Verify:

```bash
python3 --version
```

If not installed, use Homebrew:

```bash
brew install python3
```

Or download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Windows (PowerShell)

Download and install from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

**Important**: Check "Add Python to PATH" during installation

Verify installation:

```powershell
python --version
```

## Step 2: Set Up Python Environment

Create a project directory:

**macOS/Linux:**

```bash
mkdir aws-boto3-lab
cd aws-boto3-lab
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Path aws-boto3-lab
cd aws-boto3-lab
```

Create a virtual environment:

**macOS/Linux:**

```bash
python3 -m venv venv
```

**Windows (PowerShell):**

```powershell
python -m venv venv
```

Activate the virtual environment:

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error on Windows:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install Boto3:

```bash
pip install boto3
```

## Step 3: Configure AWS Credentials

Boto3 uses the same credentials as AWS CLI. Use **environment variables** (recommended for Learner Lab):

**macOS/Linux:**

```bash
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
export AWS_DEFAULT_REGION="us-east-1"
```

**Windows (PowerShell):**

```powershell
$env:AWS_ACCESS_KEY_ID="ASIA..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_SESSION_TOKEN="..."
$env:AWS_DEFAULT_REGION="us-east-1"
```

Alternatively, confirm that your `~/.aws/credentials` file has valid credentials (from Task 2).

## Step 4: Use the Python Script

Instead of copying code, we'll use the script already in this repository:

**Location**: `python-scripts/create_s3_bucket.py`

### View the Script

**macOS/Linux:**

```bash
cat ../python-scripts/create_s3_bucket.py
```

**Windows (PowerShell):**

```powershell
Get-Content ..\python-scripts\create_s3_bucket.py
```

### Customize the Script

Edit the bucket name in the script:

**macOS/Linux:**

```bash
nano ../python-scripts/create_s3_bucket.py
# Or use your preferred editor
code ../python-scripts/create_s3_bucket.py
```

**Windows (PowerShell):**

```powershell
notepad ..\python-scripts\create_s3_bucket.py
```

Change line 113:

```python
BUCKET_NAME = 'an-2026-boto3-jag'  # Change this to your initials!
```

To:

```python
BUCKET_NAME = 'an-2026-boto3-[your-initials]'  # e.g., 'an-2026-boto3-abc'
```

### Run the Script

**macOS/Linux:**

```bash
python3 ../python-scripts/create_s3_bucket.py
```

**Windows (PowerShell):**

```powershell
python ..\python-scripts\create_s3_bucket.py
```

Expected output:

```text
Creating S3 bucket...
✓ S3 bucket 'an-2026-boto3-jag' created successfully
✓ Versioning enabled
✓ Encryption (AES-256) enabled
✓ Public access blocked

✓ Bucket 'an-2026-boto3-jag' is ready!

✓ File 'test-boto3.txt' uploaded as 'test-boto3.txt'

Objects in bucket 'an-2026-boto3-jag':
  - test-boto3.txt (17 bytes)
```

## Step 5: Verify in Console

1. Go to AWS Console → S3
2. Find your bucket `an-2026-boto3-[your-initials]`
3. Verify that the file upload succeeded
4. Check Properties tab for versioning and encryption

## Understanding the Script

The script demonstrates key Boto3 concepts:

### 1. Creating a Client

```python
s3_client = boto3.client('s3', region_name=region)
```

- Creates an S3 client for API calls
- Automatically uses credentials from environment or `~/.aws/credentials`

### 2. Error Handling

```python
try:
    # AWS operations
except ClientError as e:
    print(f"Error: {e}")
```

- Catches AWS-specific errors
- Provides meaningful error messages

### 3. Bucket Operations

- `create_bucket()` - Creates the bucket
- `put_bucket_versioning()` - Enables versioning
- `put_bucket_encryption()` - Enables encryption
- `put_public_access_block()` - Blocks public access

### 4. File Operations

- `upload_file()` - Uploads files to S3
- `list_objects_v2()` - Lists bucket contents
- `delete_object()` - Deletes objects
- `delete_bucket()` - Deletes the bucket

## Step 6: Cleanup (Optional)

To delete the bucket, edit the script and uncomment the cleanup section:

```python
# Cleanup (uncomment to delete)
print("\nCleaning up...")
delete_bucket(BUCKET_NAME)
```

Then run the script again.

## Summary

**Method**: Python Boto3 SDK

**Bucket Details:**

```text
Bucket Name: an-2026-boto3-[your-initials]
Region: us-east-1
Access: Private (public access blocked)
Versioning: Enabled
Encryption: AES256
```

## Comparison

| Aspect | Rating | Notes |
| --- | --- | --- |
| **Ease of Use** | ⭐⭐ | Requires programming knowledge |
| **Automation** | ⭐⭐⭐⭐⭐ | Full programmatic control |
| **Speed** | ⭐⭐⭐⭐ | Fast once you write the code |
| **Flexibility** | ⭐⭐⭐⭐⭐ | Complete control, custom logic |
| **Learning Curve** | High | Need Python and AWS knowledge |
| **Best For** | Applications | Complex automation, integration |

**Advantages:**

- Full programmatic control
- Integration with applications
- Complex logic and error handling
- Reusable code and libraries
- Best for automation at scale
- Type hints and IDE support
- Extensive documentation

**Disadvantages:**

- Requires programming knowledge
- More code to write and maintain
- Debugging can be complex
- Dependency management
- Longer initial setup

## Cleanup

To delete the bucket using the script:

1. Uncomment the cleanup section in `create_s3_bucket.py`
2. Run the script again

Or use AWS CLI:

```bash
aws s3 rm s3://an-2026-boto3-[your-initials] --recursive
aws s3 rb s3://an-2026-boto3-[your-initials]
```

## Next Step

Return to [Main README](./README.md) for overall comparison and key takeaways.
