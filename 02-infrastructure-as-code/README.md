# Infrastructure as Code Lab

![AWS CloudFormation](https://img.shields.io/badge/CloudFormation-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![IaC](https://img.shields.io/badge/IaC-%23326CE5.svg?style=for-the-badge&logoColor=white)

## Overview

This hands-on lab teaches Infrastructure as Code (IaC) fundamentals using AWS CloudFormation and Terraform.
Students will learn to define, deploy, and manage cloud infrastructure using declarative configuration files.
This lab demonstrates how IaC enables version control, repeatability, and automation of infrastructure
provisioning.

## Learning Objectives

- Understand Infrastructure as Code principles and benefits
- Write CloudFormation templates in YAML
- Deploy and manage CloudFormation stacks
- Create Terraform configurations in HCL
- Use Terraform CLI for infrastructure lifecycle management
- Compare CloudFormation vs Terraform approaches
- Implement version control for infrastructure
- Apply IaC best practices

## Prerequisites

- Completion of Lab 01: AWS API Interaction
- AWS Academy Learner Lab [155046] access
- Basic understanding of YAML and JSON
- Text editor or IDE (VS Code recommended)
- Terminal/command line familiarity
- AWS CLI configured (from Lab 01)

## What is Infrastructure as Code?

**Infrastructure as Code (IaC)** is the practice of managing infrastructure through code rather than manual processes:

- Define infrastructure in configuration files
- Version control your infrastructure
- Automate provisioning and updates
- Ensure consistency across environments
- Enable collaboration and code review
- Reduce human error and configuration drift

---

## Task 1: AWS CloudFormation

CloudFormation is AWS's native IaC service that uses templates to provision and manage AWS resources.

### Step 1: Understanding CloudFormation

**Key Concepts:**

- **Template**: JSON or YAML file defining resources
- **Stack**: Collection of AWS resources managed as a single unit
- **Resource**: AWS service component (e.g., S3 bucket, EC2 instance)
- **Parameters**: Input values for templates
- **Outputs**: Values returned after stack creation

### Step 2: Create CloudFormation Template

Create a directory for your CloudFormation files:

```bash
mkdir cloudformation-lab
cd cloudformation-lab
```

Create a file named `s3-bucket-template.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFormation template to create an S3 bucket with versioning and encryption'

Parameters:
  BucketNameSuffix:
    Type: String
    Description: Suffix for the bucket name (e.g., your initials)
    Default: 'demo'
    AllowedPattern: '[a-z0-9-]+'
    ConstraintDescription: Must contain only lowercase letters, numbers, and hyphens

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub 'an-2026-cfn-${BucketNameSuffix}'
      AccessControl: Private
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      Tags:
        - Key: Environment
          Value: Lab
        - Key: ManagedBy
          Value: CloudFormation

Outputs:
  BucketName:
    Description: 'Name of the S3 bucket'
    Value: !Ref MyS3Bucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'

  BucketARN:
    Description: 'ARN of the S3 bucket'
    Value: !GetAtt MyS3Bucket.Arn
    Export:
      Name: !Sub '${AWS::StackName}-BucketARN'

  BucketDomainName:
    Description: 'Domain name of the S3 bucket'
    Value: !GetAtt MyS3Bucket.DomainName
```

### Step 3: Validate the Template

Before deploying, validate the template syntax:

```bash
aws cloudformation validate-template \
    --template-body file://s3-bucket-template.yaml
```

Expected output shows template parameters and description.

### Step 4: Deploy the Stack

Deploy using AWS CLI:

```bash
aws cloudformation create-stack \
    --stack-name s3-bucket-stack \
    --template-body file://s3-bucket-template.yaml \
    --parameters ParameterKey=BucketNameSuffix,ParameterValue=[your-initials]
```

Replace `[your-initials]` with your actual initials (e.g., `jag`).

### Step 5: Monitor Stack Creation

Check stack status:

```bash
aws cloudformation describe-stacks \
    --stack-name s3-bucket-stack \
    --query 'Stacks[0].StackStatus'
```

Watch stack events in real-time:

```bash
aws cloudformation describe-stack-events \
    --stack-name s3-bucket-stack \
    --max-items 10
```

Wait for status: `CREATE_COMPLETE`

### Step 6: View Stack Outputs

```bash
aws cloudformation describe-stacks \
    --stack-name s3-bucket-stack \
    --query 'Stacks[0].Outputs'
```

### Step 7: Verify in Console

1. Go to AWS Console → CloudFormation
2. Find your stack `s3-bucket-stack`
3. Click on the stack name
4. Explore tabs:
   - **Stack info**: Overview and status
   - **Events**: Creation timeline
   - **Resources**: Created AWS resources
   - **Outputs**: Exported values
   - **Parameters**: Input values
   - **Template**: View the YAML template

### Step 8: Update the Stack

Let's add a lifecycle policy. Update `s3-bucket-template.yaml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFormation template to create an S3 bucket with versioning and encryption'

Parameters:
  BucketNameSuffix:
    Type: String
    Description: Suffix for the bucket name (e.g., your initials)
    Default: 'demo'
    AllowedPattern: '[a-z0-9-]+'
    ConstraintDescription: Must contain only lowercase letters, numbers, and hyphens

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub 'an-2026-cfn-${BucketNameSuffix}'
      AccessControl: Private
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldVersions
            Status: Enabled
            NoncurrentVersionExpirationInDays: 30
      Tags:
        - Key: Environment
          Value: Lab
        - Key: ManagedBy
          Value: CloudFormation

Outputs:
  BucketName:
    Description: 'Name of the S3 bucket'
    Value: !Ref MyS3Bucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'

  BucketARN:
    Description: 'ARN of the S3 bucket'
    Value: !GetAtt MyS3Bucket.Arn
    Export:
      Name: !Sub '${AWS::StackName}-BucketARN'

  BucketDomainName:
    Description: 'Domain name of the S3 bucket'
    Value: !GetAtt MyS3Bucket.DomainName
```

Update the stack:

```bash
aws cloudformation update-stack \
    --stack-name s3-bucket-stack \
    --template-body file://s3-bucket-template.yaml \
    --parameters ParameterKey=BucketNameSuffix,ParameterValue=[your-initials]
```

Monitor the update:

```bash
aws cloudformation describe-stacks \
    --stack-name s3-bucket-stack \
    --query 'Stacks[0].StackStatus'
```

### Step 9: Delete the Stack

When done, delete all resources:

```bash
# First, empty the bucket (CloudFormation can't delete non-empty buckets)
aws s3 rm s3://an-2026-cfn-[your-initials] --recursive

# Then delete the stack
aws cloudformation delete-stack --stack-name s3-bucket-stack
```

Verify deletion:

```bash
aws cloudformation describe-stacks --stack-name s3-bucket-stack
```

### Task 1 Summary

**Method**: AWS CloudFormation

**Key Features:**

- Native AWS service (no additional tools)
- YAML or JSON templates
- Automatic rollback on errors
- Change sets for preview
- Stack policies for protection
- Drift detection

**Advantages:**

- Deep AWS integration
- No cost (only for resources)
- Automatic dependency resolution
- Built-in rollback
- AWS support

**Disadvantages:**

- AWS-only (vendor lock-in)
- Verbose syntax
- Limited to AWS services
- Slower than Terraform

---

## Task 2: Terraform

Terraform is a cloud-agnostic IaC tool that supports multiple cloud providers using HashiCorp Configuration Language (HCL).

### Step 1: Install Terraform

**macOS:**

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

**Windows:**
Download from: <https://www.terraform.io/downloads>

**Linux:**

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

Verify installation:

```bash
terraform version
```

### Step 2: Understanding Terraform

**Key Concepts:**

- **Configuration**: HCL files defining infrastructure
- **Provider**: Plugin for cloud platform (AWS, Azure, GCP)
- **Resource**: Infrastructure component
- **State**: Current infrastructure state tracking
- **Plan**: Preview of changes before applying
- **Apply**: Execute the planned changes

### Step 3: Create Terraform Configuration

Create a directory for Terraform files:

```bash
mkdir terraform-lab
cd terraform-lab
```

Create `main.tf`:

```hcl
# Configure Terraform
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

# Create S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = "an-2026-tf-${var.bucket_suffix}"

  tags = {
    Name        = "an-2026-tf-${var.bucket_suffix}"
    Environment = "Lab"
    ManagedBy   = "Terraform"
  }
}

# Enable Versioning
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block Public Access
resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle Policy
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "delete-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
```

Create `variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "bucket_suffix" {
  description = "Suffix for bucket name (e.g., your initials)"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.bucket_suffix))
    error_message = "Bucket suffix must contain only lowercase letters, numbers, and hyphens."
  }
}
```

Create `outputs.tf`:

```hcl
output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.main.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.main.arn
}

output "bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = aws_s3_bucket.main.bucket_domain_name
}

output "bucket_region" {
  description = "Region of the S3 bucket"
  value       = aws_s3_bucket.main.region
}
```

Create `terraform.tfvars`:

```hcl
bucket_suffix = "jag"  # Change to your initials
aws_region    = "us-east-1"
```

### Step 4: Initialize Terraform

Initialize the working directory and download providers:

```bash
terraform init
```

This creates:

- `.terraform/` directory with provider plugins
- `.terraform.lock.hcl` file with dependency versions

### Step 5: Format and Validate

Format code to canonical style:

```bash
terraform fmt
```

Validate configuration:

```bash
terraform validate
```

### Step 6: Plan Infrastructure Changes

Preview what Terraform will create:

```bash
terraform plan
```

Review the output:

- Resources to be created (green `+`)
- Resources to be modified (yellow `~`)
- Resources to be destroyed (red `-`)

### Step 7: Apply Configuration

Create the infrastructure:

```bash
terraform apply
```

Type `yes` when prompted to confirm.

Terraform will:

1. Create the S3 bucket
2. Enable versioning
3. Configure encryption
4. Block public access
5. Set lifecycle policy
6. Display outputs

### Step 8: View State

Terraform tracks infrastructure in a state file:

```bash
# List resources in state
terraform state list

# Show details of a resource
terraform state show aws_s3_bucket.main
```

View outputs:

```bash
terraform output
```

Get specific output:

```bash
terraform output bucket_name
```

### Step 9: Verify in Console

1. Go to AWS Console → S3
2. Find your bucket `an-2026-tf-[your-initials]`
3. Verify all configurations match your Terraform code

### Step 10: Modify Infrastructure

Let's add a tag. Update `main.tf`:

```hcl
resource "aws_s3_bucket" "main" {
  bucket = "an-2026-tf-${var.bucket_suffix}"

  tags = {
    Name        = "an-2026-tf-${var.bucket_suffix}"
    Environment = "Lab"
    ManagedBy   = "Terraform"
    Course      = "Cloud Architecture"  # New tag
  }
}
```

Plan the change:

```bash
terraform plan
```

Apply the change:

```bash
terraform apply
```

### Step 11: Destroy Infrastructure

When done, destroy all resources:

```bash
terraform destroy
```

Type `yes` to confirm.

Terraform will:

1. Remove lifecycle policy
2. Remove public access block
3. Remove encryption configuration
4. Remove versioning
5. Delete the bucket

### Task 2 Summary

**Method**: Terraform

**Key Features:**

- Cloud-agnostic (AWS, Azure, GCP, etc.)
- HCL (HashiCorp Configuration Language)
- State management
- Plan before apply
- Module system for reusability
- Large provider ecosystem

**Advantages:**

- Multi-cloud support
- Cleaner, more readable syntax
- Strong community and modules
- Faster execution
- Better state management

**Disadvantages:**

- Requires separate tool installation
- State file management complexity
- Learning curve for HCL
- No automatic rollback

---

## Comparison: CloudFormation vs Terraform

| Aspect | CloudFormation | Terraform |
| --- | --- | --- |
| **Provider** | AWS | HashiCorp |
| **Cloud Support** | AWS only | Multi-cloud |
| **Language** | YAML/JSON | HCL |
| **State Management** | AWS-managed | Local/Remote |
| **Cost** | Free | Free (Enterprise paid) |
| **Rollback** | Automatic | Manual |
| **Preview Changes** | Change Sets | Plan |
| **Learning Curve** | Medium | Medium-High |
| **Community** | AWS-focused | Large, multi-cloud |
| **Best For** | AWS-only projects | Multi-cloud, flexibility |

---

## Best Practices

### General IaC Best Practices

1. **Version Control**: Store all IaC code in Git
2. **Modularization**: Break large configurations into reusable modules
3. **Documentation**: Comment complex logic and decisions
4. **Naming Conventions**: Use consistent, descriptive names
5. **Secrets Management**: Never hardcode credentials
6. **Testing**: Validate before applying to production
7. **State Management**: Secure and backup state files
8. **Code Review**: Peer review infrastructure changes

### CloudFormation Best Practices

1. Use parameters for reusability
2. Leverage intrinsic functions (!Ref, !Sub, !GetAtt)
3. Export outputs for cross-stack references
4. Use nested stacks for complex architectures
5. Enable termination protection for production
6. Use change sets to preview updates

### Terraform Best Practices

1. Use remote state (S3 + DynamoDB)
2. Organize code with modules
3. Use workspaces for environments
4. Lock state during operations
5. Use variables and locals effectively
6. Implement consistent tagging strategy
7. Use data sources for existing resources

---

## Advanced Exercise (Optional)

Create a more complex infrastructure with both tools:

**Requirements:**

- S3 bucket for static website hosting
- CloudFront distribution
- Route53 DNS record
- ACM certificate

Try implementing this with both CloudFormation and Terraform to compare the experience.

---

## Cleanup

Ensure all resources are deleted:

### CloudFormation

```bash
aws cloudformation delete-stack --stack-name s3-bucket-stack
```

### Terraform

```bash
cd terraform-lab
terraform destroy
```

Verify in AWS Console that all resources are removed.

---

## Key Takeaways

1. **IaC enables infrastructure automation** - Define infrastructure as code
2. **Version control your infrastructure** - Track changes like application code
3. **CloudFormation is AWS-native** - Deep integration but AWS-only
4. **Terraform is cloud-agnostic** - Flexibility across multiple providers
5. **Both tools have strengths** - Choose based on requirements
6. **State management is critical** - Understand how each tool tracks resources
7. **Plan before apply** - Always preview changes before execution
8. **IaC is essential for DevOps** - Foundation for CI/CD and automation

---

## Additional Resources

### CloudFormation Resources

- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [CloudFormation Template Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)
- [CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

### Terraform Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terraform Registry](https://registry.terraform.io/)

### General IaC

- [Infrastructure as Code Book by Kief Morris](https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

## Troubleshooting

### CloudFormation Issues

**Issue**: Stack creation fails
**Solution**: Check Events tab for error details. Common issues:

- Bucket name already exists (must be globally unique)
- Insufficient permissions
- Invalid template syntax

**Issue**: Stack stuck in DELETE_FAILED
**Solution**: Manually delete resources blocking deletion (e.g., non-empty S3 bucket), then retry.

### Terraform Issues

**Issue**: "Error: configuring Terraform AWS Provider"
**Solution**: Verify AWS credentials are configured correctly. Check `~/.aws/credentials`.

**Issue**: "Error acquiring the state lock"
**Solution**: Another Terraform process is running. Wait or force-unlock (use carefully):

```bash
terraform force-unlock <lock-id>
```

**Issue**: State file conflicts
**Solution**: Use remote state with locking (S3 + DynamoDB) for team environments.

---

## Next Steps

After completing this lab, you should:

1. Understand Infrastructure as Code principles
2. Be able to write CloudFormation templates
3. Be comfortable with Terraform configurations
4. Know when to use each tool
5. Apply IaC best practices

You're now ready to build more complex cloud architectures using IaC!
