# ADR-001: Repository Structure and Module Naming

## Status

Accepted

## Context

The Cloud Architecture course covers multiple topics including AWS API interaction,
Infrastructure as Code, VPC networking, and cloud service architecture. The repository
needs a consistent structure that maps to the course syllabus while remaining navigable
for students.

## Decision

- Each module is a top-level directory named `NN-topic-name` where `NN` is the two-digit
  module number matching the syllabus order.
- Directory names use lowercase kebab-case with no spaces.
- Topic names in directories reflect the primary subject of the lab
  (e.g., `01-aws-api-interaction`, `02-infrastructure-as-code`).
- Every module directory contains a `README.md` with lab instructions.
- Shared documentation lives under `docs/` (e.g., ADRs, lab template).
- GitHub configuration lives under `.github/` (workflows, templates, dependabot).

### Module mapping

| Module | Topic | Directory |
| --- | --- | --- |
| 01 | AWS API Interaction | `01-aws-api-interaction` |
| 02 | Infrastructure as Code | `02-infrastructure-as-code` |
| 03 | VPC Endpoints | `03-vpc-endpoints` |

## Consequences

- Students can navigate the repository in syllabus order.
- New modules are added by creating a directory with the next available number.
- The numbered prefix ensures correct sort order in file explorers and GitHub.
- Renaming a module requires updating the README, PR template, and this ADR.
