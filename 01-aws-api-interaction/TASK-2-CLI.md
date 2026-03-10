# Task 2: AWS CLI (Command Line Interface)

![AWS CLI](https://img.shields.io/badge/AWS_CLI-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)

## Overview

The AWS CLI provides a powerful command-line tool for managing AWS services. It's ideal for scripting and automation.

## Step 1: Install AWS CLI

### macOS

```bash
brew install awscli
```

### Windows (PowerShell)

Download and run the installer:

- [AWS CLI MSI Installer for Windows](https://awscli.amazonaws.com/AWSCLIV2.msi)

Or using PowerShell:

```powershell
# Download and install AWS CLI
$installerPath = "$env:TEMP\AWSCLIV2.msi"
Invoke-WebRequest -Uri https://awscli.amazonaws.com/AWSCLIV2.msi -OutFile $installerPath
Start-Process msiexec.exe -ArgumentList "/i $installerPath /quiet" -Wait
```

### Linux

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Verify Installation

```bash
aws --version
```

**Download Link**: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

## Step 2: Configure AWS Credentials

### Understanding AWS Credentials

AWS uses credentials to authenticate your API requests. Two main methods exist:

#### Method A: Environment Variables (Temporary - Recommended for Learner Lab)

**What is AWS STS?**

- **STS (Security Token Service)** provides temporary security credentials
- Used by AWS Academy Learner Lab for time-limited access
- Credentials expire after a few hours (typically 3-4 hours)
- More secure than long-term credentials

**Why use environment variables?**

- Temporary credentials that expire automatically
- No need to update credential files
- Easy to refresh when lab session restarts
- Isolated per terminal session

**macOS/Linux (Bash/Zsh):**

In AWS Academy Learner Lab:

1. Click **AWS Details** button
2. Click **Show** next to AWS CLI credentials
3. Copy the credentials and paste in terminal:

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

**Characteristics:**

- ✅ The terminal clears environment variables when it closes
- ✅ STS tokens expire by their AWS-issued timestamp (15 min to 12 hours)
- ✅ Secure (no files to manage)
- ✅ Easy to refresh
- ❌ Must re-export for each new terminal
- ❌ The terminal discards environment variables when it closes

#### Method B: Credentials File (Persistent)

**When to use:**

- Long-term AWS accounts (not Learner Lab)
- Want credentials to persist across sessions
- Using IAM user credentials (not STS)

**macOS/Linux:**

Create/edit `~/.aws/credentials`:

```bash
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

> **Note:** If you are using temporary STS credentials (e.g., from AWS Academy),
> add `aws_session_token = YOUR_SESSION_TOKEN` to this file as well.

Create/edit `~/.aws/config`:

```bash
[default]
region = us-east-1
output = json
```

**Windows:**

Create/edit `C:\Users\USERNAME\.aws\credentials`:

```text
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

> **Note:** If you are using temporary STS credentials (e.g., from AWS Academy),
> add `aws_session_token = YOUR_SESSION_TOKEN` to this file as well.

Create/edit `C:\Users\USERNAME\.aws\config`:

```text
[default]
region = us-east-1
output = json
```

**Characteristics:**

- ✅ Persistent across terminal sessions
- ✅ No need to re-configure
- ❌ Must manually update when credentials expire
- ❌ Security risk if not properly managed

### Comparison: Environment Variables vs Credentials File

| Aspect | Environment Variables | Credentials File |
| --- | --- | --- |
| **Persistence** | Terminal session only | Across all sessions |
| **Security** | More secure (temporary) | Less secure (persistent) |
| **Use Case** | Learner Lab, temporary access | Long-term AWS accounts |
| **Expiration** | STS timestamp + env vars cleared on terminal close | Manual update needed |
| **Setup** | Copy-paste each session | One-time setup |
| **Best For** | AWS Academy, STS tokens | IAM users, production |

### Verify Configuration

Test your credentials with STS:

**macOS/Linux:**

```bash
aws sts get-caller-identity
```

**Windows (PowerShell):**

```powershell
aws sts get-caller-identity
```

**What is this command doing?**

- `aws sts get-caller-identity` calls AWS Security Token Service
- Returns your AWS account ID, user ID, and ARN
- Confirms your credentials are valid
- Does not create or modify any resources

Expected output (Learner Lab with assumed-role credentials):

```json
{
    "UserId": "AROA...:lab-session",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/LabRole/lab-session"
}
```

> **Note:** If you are using long-lived IAM user credentials instead of
> Learner Lab, the ARN format is `arn:aws:iam::123456789012:user/username`.

## Step 3: Create S3 Bucket with CLI

**macOS/Linux:**

```bash
aws s3 mb s3://an-2026-cli-[your-initials]
```

**Windows (PowerShell):**

```powershell
aws s3 mb s3://an-2026-cli-[your-initials]
```

Verify bucket creation:

```bash
aws s3 ls
```

## Step 4: Enable Versioning

**macOS/Linux:**

```bash
aws s3api put-bucket-versioning \
    --bucket an-2026-cli-[your-initials] \
    --versioning-configuration Status=Enabled
```

**Windows (PowerShell):**

```powershell
aws s3api put-bucket-versioning `
    --bucket an-2026-cli-[your-initials] `
    --versioning-configuration Status=Enabled
```

## Step 5: Enable Encryption

**macOS/Linux:**

```bash
aws s3api put-bucket-encryption \
    --bucket an-2026-cli-[your-initials] \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

**Windows (PowerShell):**

```powershell
aws s3api put-bucket-encryption `
    --bucket an-2026-cli-[your-initials] `
    --server-side-encryption-configuration '{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\": {\"SSEAlgorithm\": \"AES256\"}}]}'
```

## Step 6: Block Public Access

**macOS/Linux:**

```bash
aws s3api put-public-access-block \
    --bucket an-2026-cli-[your-initials] \
    --public-access-block-configuration \
        BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

**Windows (PowerShell):**

```powershell
aws s3api put-public-access-block `
    --bucket an-2026-cli-[your-initials] `
    --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

## Step 7: Upload Files

Create a test file:

**macOS/Linux:**

```bash
echo "Hello from AWS CLI" > test-cli.txt
```

**Windows (PowerShell):**

```powershell
"Hello from AWS CLI" | Out-File -FilePath test-cli.txt
```

Upload to S3:

```bash
aws s3 cp test-cli.txt s3://an-2026-cli-[your-initials]/
```

List bucket contents:

```bash
aws s3 ls s3://an-2026-cli-[your-initials]/
```

## Step 8: Download Files

```bash
aws s3 cp s3://an-2026-cli-[your-initials]/test-cli.txt downloaded-cli.txt
```

## Step 9: Sync Directories

Create a local directory with files:

**macOS/Linux:**

```bash
mkdir local-folder
echo "File 1" > local-folder/file1.txt
echo "File 2" > local-folder/file2.txt
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Path local-folder
"File 1" | Out-File -FilePath local-folder/file1.txt
"File 2" | Out-File -FilePath local-folder/file2.txt
```

Sync to S3:

```bash
aws s3 sync ./local-folder s3://an-2026-cli-[your-initials]/folder/
```

## Summary

**Method**: AWS CLI

**Bucket Details:**

```text
Bucket Name: an-2026-cli-[your-initials]
Region: us-east-1
Access: Private (public access blocked)
Versioning: Enabled
Encryption: AES256
```

## Comparison

| Aspect | Rating | Notes |
| --- | --- | --- |
| **Ease of Use** | ⭐⭐⭐ | Requires command-line knowledge |
| **Automation** | ⭐⭐⭐⭐ | Scriptable, repeatable |
| **Speed** | ⭐⭐⭐⭐ | Fast for repetitive tasks |
| **Flexibility** | ⭐⭐⭐ | Access to most AWS features |
| **Learning Curve** | Medium | Need to learn commands |
| **Best For** | Scripts | CI/CD, automation |

**Advantages:**

- Fast and efficient for repetitive tasks
- Scriptable and automatable
- Works in CI/CD pipelines
- Consistent across platforms
- Version control friendly

**Disadvantages:**

- Requires command-line knowledge
- Steeper learning curve
- Less visual feedback
- Requires credential management
- Must remember command syntax

## Cleanup

Delete all objects:

```bash
aws s3 rm s3://an-2026-cli-[your-initials] --recursive
```

Delete bucket:

```bash
aws s3 rb s3://an-2026-cli-[your-initials]
```

## Next Step

Continue to [Task 3: Python Boto3](./TASK-3-BOTO3.md)
