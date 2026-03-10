#!/usr/bin/env python3
"""
Connectivity Test Script
Lab 03: VPC Endpoints — Cloud Architecture Course

Run this script AFTER removing the 0.0.0.0/0 → IGW route from the route table.
It tests three things:
  1. General internet access  — expected to FAIL without the IGW route
  2. Amazon S3 access         — expected to PASS via the Gateway endpoint
  3. Amazon SQS access        — expected to PASS via the Interface endpoint

This proves that VPC endpoints provide connectivity to AWS services
independently of the internet gateway.

Usage:
  python3 connectivity_test.py
"""

import urllib.error
import urllib.request
import boto3
from botocore.exceptions import ClientError, BotoCoreError, NoCredentialsError

REGION = "us-east-1"
TIMEOUT = 6  # seconds — short enough to fail quickly if internet is down


def test_internet():
    """Try to reach a public HTTPS endpoint outside AWS."""
    try:
        url = "https://checkip.amazonaws.com"
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            public_ip = response.read().decode().strip()
            return True, f"Public IP: {public_ip}"
    except urllib.error.URLError as e:
        return False, f"Network error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def test_s3():
    """Try to list S3 buckets via boto3 (routes through Gateway endpoint if configured)."""
    try:
        client = boto3.client("s3", region_name=REGION)
        response = client.list_buckets()
        bucket_count = len(response.get("Buckets", []))
        return True, f"{bucket_count} bucket(s) listed"
    except NoCredentialsError:
        return False, "No AWS credentials found — check instance profile or environment"
    except (ClientError, BotoCoreError) as e:
        return False, f"AWS error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def test_sqs():
    """Try to list SQS queues via boto3 (routes through Interface endpoint if configured)."""
    try:
        client = boto3.client("sqs", region_name=REGION)
        response = client.list_queues()
        queue_count = len(response.get("QueueUrls", []))
        return True, f"{queue_count} queue(s) listed"
    except NoCredentialsError:
        return False, "No AWS credentials found — check instance profile or environment"
    except (ClientError, BotoCoreError) as e:
        return False, f"AWS error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def fmt(success, detail):
    status = "PASS" if success else "FAIL"
    return status, detail


def main():
    print()
    print("=" * 65)
    print("  Connectivity Test — Lab 03")
    print("  Cloud Architecture Course — ITESO")
    print("=" * 65)
    print()
    print("  Remove the 0.0.0.0/0 → IGW route from your route table")
    print("  BEFORE running this script, then run it to see which")
    print("  services still work without internet access.")
    print()
    print("  Testing... (internet test may take a few seconds to time out)")
    print()

    tests = [
        ("Internet (checkip.amazonaws.com)", test_internet,
         "FAIL expected — no internet route"),
        ("Amazon S3  (list_buckets)", test_s3,
         "PASS expected — Gateway endpoint bypasses internet"),
        ("Amazon SQS (list_queues)", test_sqs,
         "PASS expected — Interface endpoint bypasses internet"),
    ]

    print(f"  {'Test':<40} {'Result':<6}  {'Detail'}")
    print(f"  {'-' * 90}")

    for label, func, expectation in tests:
        success, detail = func()
        status, _ = fmt(success, detail)
        indicator = "OK" if success else "!!"
        print(f"  {label:<40} [{indicator}] {status:<4}  {detail}")
        print(f"  {'':<40}        {expectation}")
        print()

    print("=" * 65)
    print("  IMPORTANT: Re-add the 0.0.0.0/0 → IGW route in the")
    print("  route table before continuing the lab.")
    print("=" * 65)
    print()


if __name__ == "__main__":
    main()
