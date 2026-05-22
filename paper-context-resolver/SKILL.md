---
name: paper-context-resolver
description: "README-first AI 仓库复现的窄辅助技能。仅在 README 和仓库文件留下窄复现关键缺口时使用，用于从原始论文来源解析数据集划分、预处理、评估协议、检查点映射或运行时假设等具体论文细节。Use when resolving paper reproduction gaps: dataset splits, preprocessing, eval protocols, checkpoint mappings from original paper sources."
---

# paper-context-resolver

## When to apply

- README and repo files leave a reproduction-critical gap.
- The gap concerns dataset version, split, preprocessing, evaluation protocol, checkpoint mapping, or runtime assumptions.
- The main skill needs a narrow evidence supplement instead of a full paper summary.
- There is already a concrete reproduction question to answer.

## When not to apply

- The README already gives enough reproduction detail.
- The user wants a general paper explanation rather than reproduction support.
- The goal is to override README instructions without documenting the conflict.
- The only available input is a paper title and there is no concrete reproduction gap yet.

## Clear boundaries

- This skill is optional.
- This skill is helper-tier and should usually be orchestrator-invoked.
- It supplements README-first reproduction.
- It does not replace the main orchestration flow.
- It does not summarize the whole paper by default.

## Input expectations

- target repo metadata
- reproduction-critical question
- existing README or repo evidence
- any already known paper links

## Output expectations

- narrowed source list
- reproduction-relevant answer only
- explicit README-paper conflict note when applicable
- clear distinction between direct evidence and inference

## Notes

Use `references/paper-assisted-reproduction.md`.
