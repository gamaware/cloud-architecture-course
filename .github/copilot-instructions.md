# Copilot Code Review Instructions

This is a university course repository for Cloud Architecture at ITESO.
It contains hands-on labs with Python scripts, markdown documentation,
CloudFormation templates, and Terraform configurations.

## Review priorities

1. **Reproducibility** — Lab instructions must work from a clean AWS Academy
   Learner Lab environment. Flag hardcoded paths, missing prerequisites, or
   steps that assume prior state.

2. **Technical accuracy** — Verify AWS CLI commands, CloudFormation templates,
   Terraform configurations, Python Boto3 code, and VPC networking concepts
   are correct and follow current best practices.

3. **Security** — Flag any committed credentials, hardcoded secrets, private keys,
   or AWS account IDs. Lab instructions should use placeholders.

4. **Python quality** — Scripts should follow PEP 8 style, use specific exception
   handling (not bare except), and handle credentials securely.

5. **Dateless content** — No semester-specific dates, Canvas course links, or
   time-bound references. Content must be reusable across semesters.

6. **Markdown quality** — Line length max 120 characters (tables exempt).
   Fenced code blocks must specify a language. No bold text as headings.

7. **Cross-references** — Directory paths in instructions must match actual
   directory names (kebab-case with NN- prefix, e.g., `02-infrastructure-as-code`).

## What NOT to flag

- Placeholder READMEs in future modules (content under development).
- Simplified configurations intentional for educational purposes.
