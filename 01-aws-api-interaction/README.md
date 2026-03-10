# AWS API Interaction Lab

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![CLI](https://img.shields.io/badge/CLI-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)

## Overview

This hands-on lab teaches AWS API interaction fundamentals through three different methods: AWS Management Console
(GUI), AWS CLI, and Python Boto3 SDK. Students will learn how to create and manage S3 buckets using each approach,
understanding the strengths and use cases for each method. This lab provides the foundation for programmatic cloud
resource management.

## Learning Objectives

- Navigate and use the AWS Management Console effectively
- Install and configure AWS CLI
- Execute AWS operations via command line
- Write Python scripts using Boto3 SDK
- Create, configure, and manage S3 buckets programmatically
- Understand AWS authentication and credentials
- Compare different methods of AWS API interaction
- Apply best practices for cloud automation

## Prerequisites

- AWS Academy Learner Lab [155046] access
- Basic understanding of cloud computing concepts
- Terminal/command line familiarity
- Text editor or IDE (VS Code recommended)

## What is AWS API?

**AWS API (Application Programming Interface)** provides programmatic access to AWS services:

- RESTful API endpoints for all AWS services
- Multiple ways to interact: Console, CLI, SDKs
- Consistent authentication using AWS credentials
- Enables automation and infrastructure as code
- Foundation for DevOps and cloud engineering

## Lab Structure

This lab covers 3 tasks, each exploring a different method of AWS API interaction.

### Tasks

1. **[Task 1: AWS Management Console (GUI)](./TASK-1-CONSOLE.md)**
   - Visual interface for AWS services
   - Best for learning and exploration
   - No coding required

2. **[Task 2: AWS CLI (Command Line Interface)](./TASK-2-CLI.md)**
   - Command-line tool for AWS operations
   - Ideal for scripting and automation
   - Cross-platform support

3. **[Task 3: Python Boto3 SDK](./TASK-3-BOTO3.md)**
   - Programmatic access via Python
   - Full control and flexibility
   - Application integration

## Comparison of Methods

| Aspect | Console (GUI) | AWS CLI | Boto3 (Python) |
| --- | --- | --- | --- |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Automation** | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Flexibility** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | Low | Medium | High |
| **Best For** | Learning, exploration | Scripts, CI/CD | Applications, complex automation |

## Quick Start

1. Start with **Task 1** to understand AWS services visually
2. Progress to **Task 2** to learn command-line automation
3. Complete **Task 3** to master programmatic control

Each task is self-contained and you can complete them independently, but we recommend following the order for
the best learning experience.

## Key Takeaways

1. **AWS provides multiple ways to interact with services** - Choose based on your use case
2. **Console is great for learning** - Visual feedback helps understand AWS services
3. **CLI is ideal for scripting** - Fast, efficient, and works in automation pipelines
4. **Boto3 enables complex automation** - Full programmatic control for applications
5. **All methods use the same AWS API** - Understanding one helps with others
6. **Credentials are critical** - Secure management is essential for all methods

## Additional Resources

- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS S3 User Guide](https://docs.aws.amazon.com/s3/index.html)
- [AWS SDK for Python (Boto3) Getting Started](https://aws.amazon.com/sdk-for-python/)
- [AWS STS Documentation](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html)

## Troubleshooting

### Issue: "Bucket name already exists"

**Solution**: Bucket names must be globally unique. Add extra identifiers to your bucket name.

### Issue: "Access Denied" errors

**Solution**: Verify your AWS credentials are correctly configured. In Learner Lab, credentials expire after a few
hours - refresh them from AWS Details.

### Issue: AWS CLI not found

**Solution**: Confirm that you have AWS CLI in your PATH. Restart your terminal after installation.

### Issue: Boto3 import error

**Solution**: Ensure you've activated your virtual environment and installed boto3: `pip install boto3`

### Issue: Environment variables not working

**Solution**: Verify you've exported them in the current terminal session. They don't persist across terminal restarts.

## Next Steps

After completing this lab, you should:

1. Understand the three main methods of AWS API interaction
2. Be comfortable creating and managing S3 buckets
3. Know when to use each method
4. Be ready for Lab 02: Infrastructure as Code

Continue to **[Lab 02: Infrastructure as Code](../02-infrastructure-as-code)** to learn about CloudFormation
and Terraform!
