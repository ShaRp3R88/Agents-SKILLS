---
name: repo-intake-and-plan
description: "README-first AI 仓库复现的窄辅助技能。用于扫描仓库、读取 README 和常见项目文件、提取文档命令、分类推理/评估/训练候选方案，并向主编排器返回最小可信复现计划。Use when scanning a repo for AI reproduction: read README, extract doc commands, classify candidates, return minimal reproduction plan."
---

# repo-intake-and-plan

## When to apply

- At the beginning of README-first reproduction work.
- When the main skill needs a fast map of repo structure and documented commands.
- When inference, evaluation, and training candidates must be classified conservatively.
- When the user explicitly wants to inspect the repo first and not run anything yet.

## When not to apply

- When execution has already started and the task is now about running commands or writing outputs.
- When the target is not a repository-backed reproduction task.
- When the user only wants paper interpretation without repo inspection.
- When the user already has a selected documented command and only needs setup or execution.

## Clear boundaries

- This skill scans and plans.
- This skill is helper-tier and should usually be orchestrator-invoked.
- It does not install environments.
- It does not prepare large assets.
- It does not execute substantive reproduction commands.
- It does not decide high-risk patching.

## Input expectations

- Target repository path.
- Access to README and common project files if present.
- Optional user hints about desired priority, such as inference-first.

## Output expectations

- concise repo structure summary
- documented command inventory
- inferred candidate categories: inference, evaluation, training, other
- minimum trustworthy reproduction recommendation
- notable ambiguity or risk list

## Notes

Use `references/repo-scan-rules.md` and helper scripts under `scripts/`.
