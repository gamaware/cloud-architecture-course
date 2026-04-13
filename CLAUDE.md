# CLAUDE.md — Project Instructions for Claude Code

This file is automatically loaded into context when Claude Code starts a conversation
in this repository. It defines the conventions, rules, and structure that must be followed.

## Repository Overview

Hands-on labs for Cloud Architecture at ITESO. Contains numbered modules mapped to the
course syllabus, each in a directory with lab instructions, Python scripts, and
configuration examples.

## Repository Structure

```text
NN-topic-name/          # Module directories (kebab-case)
  README.md             # Lab instructions
  TASK-*.md             # Task-specific instructions (when applicable)
  scripts/              # Python scripts
  python-scripts/       # Python scripts (alternative location)
  screenshots/          # Visual guides
docs/
  adr/                  # Architecture Decision Records (dateless)
  lab-template.md       # Standard 13-section lab README template
.claude/
  settings.json         # Project-level Claude Code settings (hooks, permissions)
  hooks/                # Automation hooks (post-edit formatters)
  skills/               # Reusable skills (e.g., /new-lab to scaffold modules)
.github/
  workflows/            # CI/CD pipelines
  actions/              # Composite actions
  ISSUE_TEMPLATE/       # Issue templates
  PULL_REQUEST_TEMPLATE.md
  copilot-instructions.md  # Copilot code review custom instructions
```

### Module Naming

Directories follow `NN-topic-name` format where NN is two-digit syllabus order.
Topic names use lowercase kebab-case reflecting the primary subject
(e.g., `01-aws-api-interaction`, `02-infrastructure-as-code`, `03-vpc-endpoints`).

## Git Workflow

### Commits

- **Conventional commits required** — enforced by `conventional-pre-commit` hook.
- Format: `type: description` (e.g., `fix:`, `feat:`, `docs:`, `chore:`, `ci:`).
- Never commit directly to `main` — enforced by `no-commit-to-branch` hook.
- Always work on a feature branch and create a PR.
- Do NOT add `Co-Authored-By` watermarks or any Claude/AI attribution to commits, code, or content. Ever.

### Pull Requests

- All changes go through PRs — no direct pushes to `main`.
- Squash merge only (merge commits and rebase disabled).
- CodeRabbit and GitHub Copilot auto-review all PRs — address their comments before merging.
- All required status checks must pass before merge.
- At least 1 approving review required (CODEOWNERS enforced).
- All review conversations must be resolved before merge.
- Use `--admin` flag to bypass branch protection when necessary.

### Branch Protection (main)

- Required status checks: Markdown Linting, YAML Validation,
  Validate Repository Structure, Security Scan.
- Additional CI checks (not required but run on PRs): Check Links, README Quality Check.
- Strict status checks — branch must be up to date with main.
- Stale reviews dismissed on new pushes.
- Required linear history (squash only).

## Pre-commit Hooks

All hooks must pass before committing. Install with `pre-commit install`.

### Hooks in use

- **General**: trailing-whitespace, end-of-file-fixer, check-yaml, check-json,
  check-added-large-files (1MB), check-merge-conflict, detect-private-key,
  check-executables-have-shebangs, check-shebang-scripts-are-executable,
  check-symlinks, check-case-conflict, no-commit-to-branch (main).
- **Secrets**: detect-secrets (with `.secrets.baseline`), gitleaks.
- **Markdown**: markdownlint with `--fix`.
- **Prose**: Vale with write-good (passive voice, weasel words) and proselint (grammar, usage).
- **Shell**: shellcheck (severity: warning), shellharden.
- **GitHub Actions**: actionlint, zizmor (security analysis).
- **Commits**: conventional-pre-commit (commit-msg stage).

## Claude Code Hooks

Hooks in `.claude/settings.json` automate deterministic actions:

- **Post-edit** (`post-edit.sh`): Runs `shellharden --replace` on `.sh` files
  and `markdownlint --fix` on `.md` files after every Edit/Write (when the tools
  are installed).

## Claude Code Skills

Skills in `.claude/skills/` provide reusable workflows:

- **`/new-lab [NN-topic-name]`** — Scaffolds a new lab module with README template.
  See `docs/lab-template.md` for the 13-section structure.
- **`/ship-it [PR-number]`** — End-to-end PR lifecycle: updates docs (CLAUDE.md, README,
  ADRs, MEMORY.md), commits, creates PR, monitors CI, addresses CodeRabbit and Copilot
  review comments, merges with `--admin`, and cleans up stale local branches.
  Pass a PR number to resume monitoring. Uses global skill.

## Linting Policy

### Absolute rule: NO suppressions on our own code

- All default linting rules are enforced. Fix violations, never suppress them.
- Do not create `.markdownlintignore`, custom rule overrides, or inline disable comments.
- Markdownlint config: MD013 line length at 120 characters, tables exempt.
  That is the ONLY customization in `.markdownlint.yaml`.

## Shell Scripts

- Must pass shellcheck (severity: warning) and shellharden.
- Quote all variables. Prefer `"$VAR"` over `"${VAR}"` — only use braces when needed
  (e.g., `"${VAR}_suffix"`).
- Use arrays for word splitting.
- Scripts must have shebangs and executable permissions.

## Python Scripts

- Follow PEP 8 style guidelines.
- Use specific exception handling (not bare `except Exception`).
- Use `botocore.exceptions.ClientError`, `BotoCoreError`, `NoCredentialsError` for AWS calls.
- Handle credentials securely — never hardcode access keys or secrets.

## Markdown

- Line length limit: 120 characters (MD013).
- Tables are exempt from line length.
- Every directory must have a `README.md`.
- Table separator lines must have spaces around pipes: `| --- | --- |` not `|---|---|`.
- Use ATX headings (`#`), not bold text as headings.
- Fenced code blocks must specify a language.

## CI/CD Pipelines

### quality-checks.yml

Markdown linting, link checking, YAML linting, repository structure validation,
README quality checks, zizmor (Actions security), Vale (prose linting).

### security.yml

Semgrep static analysis and Trivy vulnerability scanning.

### update-pre-commit-hooks.yml

Weekly auto-update of pre-commit hook versions via PR.

### Dependabot

Monitors GitHub Actions dependencies weekly.

## Code Review

- **CodeRabbit** — Auto-reviews via `.coderabbit.yaml`. Detailed suggestions with path-specific instructions.
- **GitHub Copilot** — Auto-reviews via ruleset. Custom instructions in `.github/copilot-instructions.md`.
- Both reviewers run on every PR. Address comments from both before merging.
- Reviewers may comment on issues already fixed in subsequent commits.
  Verify current file state before acting — stale comments can be dismissed.

## GitHub Actions Security

- All `actions/checkout` steps must include `persist-credentials: false`.
- Action references use tag pins (e.g., `@v6`); configured via `zizmor.yml` with `ref-pin` policy.
- zizmor runs in CI and as a pre-commit hook to catch security issues in workflows.

## Security

- GitHub secret scanning and push protection enabled at the repository level.
- Never commit secrets, credentials, private keys, or `.env` files.
- `.gitignore` excludes: `.env`, `.env.local`, `*.pem`, `*.key`, `credentials.json`.
- `detect-secrets` baseline must be updated for false positives:
  `detect-secrets scan --update .secrets.baseline`.
- Lab instructions use placeholder values (`YOUR_CLIENT_SECRET`, `<your-instance-ip>`,
  `YOUR_AWS_ACCOUNT_ID`).

## Lab Content Rules

- **Dateless** — No semester names, specific dates, or Canvas course links. Content must
  be reusable across semesters.
- **English only** — All lab content, code comments, and HTML output in English.
- **Placeholders** — Never hardcode AWS account IDs, credentials, or instance IPs.
- **Cross-references** — Directory paths in instructions must match actual directory names.

## ADRs

Architecture Decision Records live in `docs/adr/`. They are dateless since the course
structure persists across semesters. Reference `docs/adr/README.md` for the full index.

## Repo Configuration

- **Visibility**: Public
- **Topics**: cloud-architecture, aws, terraform, cloudformation, python, boto3, vpc,
  iac, labs, cloud-computing
- **Merge strategy**: Squash only, PR title used as commit title
- **Auto merge**: Enabled (useful for Dependabot PRs)
- **Delete branch on merge**: Enabled
- **Wiki**: Disabled (content lives in repo)
- **Projects**: Disabled (not in use)
