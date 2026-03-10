#!/usr/bin/env python3
"""
VPC Endpoint Latency Comparison Script
Lab 03: VPC Endpoints — Cloud Architecture Course

Run this script at three points during the lab:
  1. Baseline      — no endpoints, traffic goes through internet
  2. After S3      — after creating the S3 Gateway endpoint
  3. After SQS     — after creating the SQS Interface endpoint

Usage:
  python3 latency_test.py
"""

import boto3
import time
import statistics
from botocore.exceptions import ClientError, BotoCoreError, NoCredentialsError

REGION = "us-east-1"
ITERATIONS = 30


def measure(func, label):
    """Run func ITERATIONS times and return latency statistics (in ms)."""
    samples = []
    errors = 0

    print(f"\n  Testing: {label}")
    print(f"  {'.' * ITERATIONS}", end="\r  ", flush=True)

    for _ in range(ITERATIONS):
        try:
            t0 = time.perf_counter()
            func()
            samples.append((time.perf_counter() - t0) * 1000)
            print(".", end="", flush=True)
        except NoCredentialsError:
            print("!")
            print("  ERROR: No AWS credentials found — check instance profile or environment")
            return None
        except (ClientError, BotoCoreError):
            errors += 1
            print("x", end="", flush=True)
        except Exception:
            errors += 1
            print("x", end="", flush=True)

    print()

    if not samples:
        print("  ERROR: All requests failed — is the service reachable?")
        return None

    sorted_samples = sorted(samples)
    p95_index = int(len(sorted_samples) * 0.95)

    return {
        "label": label,
        "count": len(samples),
        "errors": errors,
        "avg": statistics.mean(samples),
        "min": sorted_samples[0],
        "median": statistics.median(samples),
        "p95": sorted_samples[p95_index],
        "max": sorted_samples[-1],
    }


def print_result(r):
    if not r:
        return
    print(f"\n  Service : {r['label']}")
    print(f"  Samples : {r['count']}  |  Errors: {r['errors']}")
    print(f"  {'-' * 36}")
    print(f"  {'Average':<10} {r['avg']:>8.2f} ms")
    print(f"  {'Min':<10} {r['min']:>8.2f} ms")
    print(f"  {'Median':<10} {r['median']:>8.2f} ms")
    print(f"  {'P95':<10} {r['p95']:>8.2f} ms")
    print(f"  {'Max':<10} {r['max']:>8.2f} ms")


def print_comparison(label_a, result_a, label_b, result_b):
    """Print a side-by-side comparison of two result sets."""
    if not result_a or not result_b:
        return
    diff_avg = result_a["avg"] - result_b["avg"]
    diff_p95 = result_a["p95"] - result_b["p95"]
    print(f"\n  {'Metric':<10} {label_a:>14} {label_b:>14} {'Diff':>10}")
    print(f"  {'-' * 52}")
    print(f"  {'Average':<10} {result_a['avg']:>13.2f}ms {result_b['avg']:>13.2f}ms {diff_avg:>+10.2f}ms")
    print(f"  {'P95':<10} {result_a['p95']:>13.2f}ms {result_b['p95']:>13.2f}ms {diff_p95:>+10.2f}ms")


def main():
    print()
    print("=" * 52)
    print("  VPC Endpoint Latency Test — Lab 03")
    print("  Cloud Architecture Course — ITESO")
    print("=" * 52)
    print(f"\n  Region     : {REGION}")
    print(f"  Iterations : {ITERATIONS} per service")
    print(f"\n  Initializing boto3 clients...")

    try:
        s3 = boto3.client("s3", region_name=REGION)
        sqs = boto3.client("sqs", region_name=REGION)
    except NoCredentialsError:
        print("  ERROR: No AWS credentials found — check instance profile or environment")
        return
    except BotoCoreError as e:
        print(f"  ERROR: Failed to initialize AWS clients — {e}")
        return

    print("  OK — credentials loaded from instance profile")

    print("\n" + "-" * 52)
    print("  Running tests...")
    print("-" * 52)

    s3_result = measure(lambda: s3.list_buckets(), "S3  (list_buckets)")
    sqs_result = measure(lambda: sqs.list_queues(), "SQS (list_queues)")

    print("\n" + "=" * 52)
    print("  RESULTS")
    print("=" * 52)

    print_result(s3_result)
    print_result(sqs_result)

    print("\n" + "=" * 52)
    print("  Record these values in the comparison table")
    print("  in your lab README before moving to the")
    print("  next task.")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()
