#!/usr/bin/env python3
"""
DNS Resolution Test Script
Lab 03: VPC Endpoints — Cloud Architecture Course

Run this script at three points during the lab:
  1. Baseline      — no endpoints, both services resolve to public IPs
  2. After S3      — after creating the S3 Gateway endpoint (S3 DNS unchanged)
  3. After SQS     — after creating the SQS Interface endpoint (SQS DNS flips to private)

The key observation:
  - Gateway endpoint (S3):    DNS does NOT change — routing table intercepts traffic silently
  - Interface endpoint (SQS): DNS DOES change    — service name resolves to a private VPC IP

Usage:
  python3 dns_test.py
"""

import socket


SERVICES = {
    "S3  (Gateway endpoint)": "s3.amazonaws.com",
    "SQS (Interface endpoint)": "sqs.us-east-1.amazonaws.com",
}

PRIVATE_PREFIXES = ("10.", "172.16.", "172.17.", "172.18.", "172.19.",
                    "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                    "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                    "172.30.", "172.31.", "192.168.")


def classify(ip):
    """Return 'PRIVATE' if the IP is in an RFC-1918 range, else 'PUBLIC'."""
    if any(ip.startswith(prefix) for prefix in PRIVATE_PREFIXES):
        return "PRIVATE"
    return "PUBLIC"


def resolve(hostname):
    """Resolve a hostname to its first IP address."""
    try:
        ip = socket.gethostbyname(hostname)
        return ip, classify(ip), None
    except socket.gaierror as e:
        return None, None, str(e)


def main():
    print()
    print("=" * 60)
    print("  DNS Resolution Test — Lab 03")
    print("  Cloud Architecture Course — ITESO")
    print("=" * 60)
    print()
    print("  What to look for:")
    print("  - PUBLIC  → traffic will route through the internet")
    print("  - PRIVATE → traffic will route through a VPC Interface endpoint")
    print()
    print("  Note: S3 Gateway endpoint does NOT change DNS.")
    print("  S3 will always resolve to a public IP — the route table")
    print("  intercepts that traffic silently before it leaves the VPC.")
    print()

    results = []
    for label, hostname in SERVICES.items():
        ip, scope, error = resolve(hostname)
        results.append((label, hostname, ip, scope, error))

    print(f"  {'Service':<30} {'Hostname':<40} {'Resolved IP':<18} {'Scope'}")
    print(f"  {'-' * 100}")

    for label, hostname, ip, scope, error in results:
        if error:
            print(f"  {label:<30} {hostname:<40} {'ERROR':<18} {error}")
        else:
            marker = "  <-- traffic stays inside VPC!" if scope == "PRIVATE" else ""
            print(f"  {label:<30} {hostname:<40} {ip:<18} {scope}{marker}")

    print()
    print("  Run this script again after creating each endpoint to observe")
    print("  how DNS resolution changes (or doesn't).")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
