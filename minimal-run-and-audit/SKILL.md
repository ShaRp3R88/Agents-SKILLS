---
name: minimal-run-and-audit
description: "README-first AI 仓库复现的可信执行和报告技能。用于从选定的冒烟测试或文档推理/评估命令中捕获或规范化证据，并写入标准化 repro_outputs/ 文件。Use for trusted execution and reporting in AI reproduction: capture and normalize evidence from smoke tests or eval commands."
---

# minimal-run-and-audit

Use the shared operating principles in
`../../references/agent-operating-principles.md`; this skill should make run
evidence auditable without turning every command into a rigid protocol.

## When to apply

- After a reproduction target and setup plan exist.
- When the main skill needs execution evidence and normalized outputs.
- When a smoke test, documented inference run, documented evaluation run, or other short non-training verification is appropriate.
- When the user already knows what command should be attempted and wants execution plus reporting only.

## When not to apply

- During initial repo scanning.
- When environment or assets are still undefined enough to make execution meaningless.
- When the task is a literature lookup rather than repository execution.
- When the user is still deciding which reproduction target should count as the main run.

## Clear boundaries

- This skill owns normalized reporting for an attempted command.
- It may receive execution evidence from the main skill or a thin helper.
- It does not choose the overall target on its own.
- It does not perform broad paper analysis.
- It does not own training startup, resume, or long-running training state.
- It should not normalize risky code edits into acceptable practice.

## Input expectations

- selected reproduction goal
- runnable commands or smoke commands
- environment and asset assumptions
- optional patch metadata

## Output expectations

- execution result summary
- standardized `repro_outputs/` files
- clear distinction between verified, partial, and blocked states
- `PATCHES.md` when repo files changed

## Notes

Use `references/reporting-policy.md`, `scripts/run_command.py`, and `scripts/write_outputs.py`.
