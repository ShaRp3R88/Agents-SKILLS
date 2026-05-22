---
name: skill-chinese-desc
description: "将已有 skill 的 description 转为中文+英文双语格式，以提升中文用户理解度和英文触发匹配率。扫描所有用户级 skill，检测缺失中文或缺失英文的描述，逐一补充为双语格式。跳过 gstack/ 和 plugin/ 目录。Use when converting skill descriptions to bilingual CN+EN format. Scans all skills, detects missing Chinese or English, adds bilingual descriptions."
---

# Skill Description 双语化

将 description 转为 `"中文简短描述。English trigger description."` 双语格式。

## 步骤

### 1. 运行检测

```bash
python ~/.agents/skills/skill-chinese-desc/detect.py
```

脚本扫描 `~/.agents/skills/` 下所有 SKILL.md（跳过 gstack/、plugin/），分类为：
- **仅中文**（需添加英文触发描述）
- **仅英文**（需添加中文前缀）
- **已双语**（跳过）

### 2. 逐个转换

对每个待处理文件：
- `Read` 该 SKILL.md 前 10 行，定位 `description:` 行
- 判断当前是仅中文还是仅英文
- 构造双语描述，格式：
  - 原仅英文：`"中文简要说明。原有英文描述保持不动。"`
  - 原仅中文：`"原有中文描述。English trigger description for harness matching."`
- 用 `Edit` 精确替换该行（仅替换 description 值，不动 YAML 结构和其他字段）

### 3. 翻译风格

- 中文部分：简洁，概括 skill 的核心用途
- 英文部分：保留原有详细触发描述；如原无英文，添加以触发词为导向的英文说明
- 英文描述末尾可加 NOT 排除（如 `NOT for data analysis (use data-analysis)`）以减少兄弟 skill 冲突
