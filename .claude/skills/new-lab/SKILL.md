---
name: new-lab
description: >-
  Scaffold a new lab module with the standard 13-section README
  and directory structure. Use this skill whenever the user wants to
  create a new lab, add a module, scaffold a lesson, or says something
  like "create lab 04" or "add a new module for serverless".
disable-model-invocation: true
user-invocable: true
argument-hint: "[NN-topic-name]"
---

# Scaffold a New Lab Module

Create a new lab module directory following the course conventions.

Argument: `$ARGUMENTS` is the module directory name in `NN-topic-name` format
(e.g., `04-serverless-lambda`).

## Steps

1. Read `docs/lab-template.md` to understand the 13-section structure.
2. Create the module directory: `$ARGUMENTS/`
3. Generate `$ARGUMENTS/README.md` with:
   - Title derived from the topic name (convert kebab-case to title case)
   - All 13 sections from the lab template as scaffolded placeholders
   - Appropriate technology badges
   - Author and license sections
4. Update the root `README.md` to add the new module entry
   (use existing modules as examples for the format)

## Conventions

- Directory names: `NN-topic-name` (two-digit number, kebab-case)
- Files stay flat at the lab root until 5+ files of the same type warrant a subdirectory
- All content in English, dateless, no hardcoded credentials
- Use placeholder values for AWS resources (`YOUR_INSTANCE_IP`, `YOUR_AWS_ACCOUNT_ID`, etc.)
- Follow the hint pattern from docs/lab-template.md for questions
