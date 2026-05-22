---
name: win-cli
description: Windows 环境下命令执行规范。触发词：cmd、powershell、windows 命令、shell、bash 报错、路径错误。强制要求：在 win32 平台一律优先使用 cmd /c 或 powershell -Command，禁止直接使用 Unix bash 语法（ls/cp/rm/grep 等）。
---

# Windows Native CLI Skill

## 触发条件

以下关键词或场景出现时**必须**自动激活本 skill：
- 用户输入包含：`cmd`、`powershell`、`命令行`、`shell`、`windows 命令`
- 用户抱怨 bash 报错：`command not found`、`Invalid path`、`syntax error`、`不是内部或外部命令`
- 用户要求文件/目录操作：`列出文件`、`查看目录`、`复制`、`移动`、`删除`、`搜索文件内容`
- 用户输入包含 Unix 命令：`ls`、`grep`、`cp`、`rm`、`mv`、`cat`、`tail`、`wc`、`find`
- 执行涉及 Windows 绝对路径（`E:\\...`、`C:\\...`）的命令
- 平台为 `win32` 且意图执行任何 `Bash` 工具调用时

## 核心原则

| 场景 | ❌ 禁止（Bash） | ✅ 优先（Windows 原生） |
|------|----------------|------------------------|
| 文件列表 | `ls -la` | `cmd /c "dir /s /b"` |
| 目录切换确认 | `pwd` | `cmd /c "cd"` |
| 搜索文件内容 | `grep -r` | `powershell -Command "Select-String"` |
| 复制文件 | `cp` | `cmd /c "copy"` |
| 移动/重命名 | `mv` | `cmd /c "move"` |
| 删除文件 | `rm` | `cmd /c "del"` |
| 删除目录 | `rm -rf` | `cmd /c "rmdir /s /q"` |
| 创建目录 | `mkdir -p` | `cmd /c "mkdir"`（自动递归） |
| 查看文件尾部 | `tail` | `powershell -Command "Get-Content -Tail"` |
| 统计行数 | `wc -l` | `powershell -Command "(Get-Content).Count"` |

## 命令映射详解

### 1. CMD（`cmd /c`）—— 简单命令首选

适用于单条、无管道、无复杂对象的命令。

```bash
cmd /c "dir E:\Project_IEEE39\a2c\core\ /s /b"
cmd /c "type README.md"
cmd /c "copy a.py b.py"
cmd /c "move old.txt new.txt"
cmd /c "del /q *.tmp"
cmd /c "mkdir sub\\dir\\nested"
cmd /c "rmdir /s /q build"
```

**注意**：
- 路径中的 `\\` 在 JSON 和命令行中需视情况转义。向 `Bash` 工具传参时，推荐用 **正斜杠 `/`**：`E:/Project_IEEE39/a2c/core/`
- `cmd /c` 后面必须用 **双引号** 包裹整条命令
- 若命令内部本身需要双引号，改用 `powershell` 或进行 `"` 转义

### 2. PowerShell —— 复杂管道与对象操作

适用于过滤、排序、JSON 处理、多命令管道。

```bash
# 递归列出 .py 文件
powershell -Command "Get-ChildItem -Recurse -Filter *.py | Select-Object FullName, Length"

# 搜索文件内容（替代 grep）
powershell -Command "Select-String -Path '*.py' -Pattern 'def train'"

# 查看尾部 20 行（替代 tail -n 20）
powershell -Command "Get-Content logs.txt -Tail 20"

# 统计代码行数（替代 wc -l）
powershell -Command "(Get-Content utils.py).Count"

# 路径存在性检查
powershell -Command "Test-Path E:/Project_IEEE39/data"
```

## 路径规范

在 Windows 上向 `Bash` 工具传路径时，**一律使用正斜杠 `/`**：

```bash
# ✅ 正确
cmd /c "dir E:/Project_IEEE39/a2c/core/"

# ❌ 错误（容易在 bash 转义层出问题）
cmd /c "dir E:\\Project_IEEE39\\a2c\\core\\"
```

如果必须从 Windows 风格路径转换：
```bash
powershell -Command "'E:\\Project_IEEE39'.Replace('\\','/')"
```

## 引号与转义规则

| 场景 | 正确写法 |
|------|----------|
| 简单命令 | `cmd /c "dir /s /b"` |
| 路径无空格 | `cmd /c "type E:/file.txt"` |
| 路径含空格 | `cmd /c "type \"E:/my file.txt\""` |
| PowerShell 字符串 | `powershell -Command "Get-Content 'E:/file.txt'"` |
| PowerShell 变量 | `powershell -Command "$env:COMPUTERNAME"` |

**铁律**：
- `cmd /c` 外层用双引号 `"`
- 内部若需引号，用单引号 `'` 或转义双引号 `\"`
- 尽量避免在 `cmd /c` 中嵌套多层引号，直接上 `powershell`

## 权限配置模板

当用户抱怨命令被拒绝时，引导用户将以下条目加入 `.claude/settings.local.json` 的 `permissions.allow` 数组：

```json
"Bash(cmd /c *)",
"Bash(powershell -Command *)",
"Bash(powershell -c *)",
"Bash(cmd //c *)"
```

## 常见任务工作流

### 浏览代码目录结构
```bash
cmd /c "dir E:/Project_IEEE39 /s /b | findstr /i /r \"\\.py$\""
```

### 快速查看文件内容（替代 cat/head）
```bash
cmd /c "type README.md"
powershell -Command "Get-Content README.md -Head 20"
```

### 批量删除编译缓存（替代 rm -rf）
```bash
cmd /c "rmdir /s /q __pycache__"
cmd /c "del /s /q *.pyc"
```

### 跨文件搜索符号（替代 grep -r）
```bash
powershell -Command "Select-String -Path '*.py' -Pattern 'class IEEE39Env'"
```

### 检查磁盘/目录大小
```bash
powershell -Command "Get-ChildItem -Recurse | Measure-Object -Property Length -Sum"
```

## 与 Git Bash / WSL 的区别

| 特性 | Git Bash (Bash 工具默认) | cmd /c | PowerShell |
|------|--------------------------|--------|------------|
| 路径格式 | `/c/Users/...` | `C:\Users\...` | `C:\Users\...` 或 `C:/Users/...` |
| 大小写敏感 | 是 | 否 | 否 |
| 管道输出 | 纯文本 | 纯文本 | 对象流 |
| 环境变量 | `$HOME` | `%USERPROFILE%` | `$env:USERPROFILE` |
| 通配符 | `*` `?` | `*` `?` | `*` `?` + `-Filter` |

## 故障排查速查表

| 报错 | 原因 | 修复 |
|------|------|------|
| `bash: command not found` | 使用了 Unix 命令 | 改用 `cmd /c` 对应命令 |
| `Invalid switch` | `dir` 用了 `-l` 这类 bash 风格参数 | 改用 `/s /b /a` 等 CMD 风格参数 |
| `The system cannot find the path` | 反斜杠被转义消失 | 改用正斜杠 `/` 或 `\\` |
| `was unexpected at this time` | cmd 中特殊字符未转义 | 改用 powershell |
| `Access is denied` | 权限不足或文件被占用 | 检查是否被 VSCode/conda 占用 |

## 安全约束（危险操作必须确认）

以下操作属于**危险操作**，在执行前**必须使用 AskUserQuestion 工具向用户确认**，不得直接执行：

| 危险等级 | 操作类型 | 示例命令 | 确认方式 |
|----------|----------|----------|----------|
| 🔴 高危 | 删除文件 | `del /q *.py`、`del /f important.txt` | AskUserQuestion：确认文件列表 + 是否备份 |
| 🔴 高危 | 删除目录 | `rmdir /s /q results`、`rmdir /s /q checkpoints` | AskUserQuestion：确认目录路径 + 内容影响 |
| 🔴 高危 | 覆盖已有文件 | `copy new.csv old.csv`（目标存在）、`move a.py b.py`（覆盖） | AskUserQuestion：确认覆盖 + 是否需要备份 |
| 🟡 中危 | 批量删除（通配符） | `del /s *.tmp`、`rmdir /s *.log` | AskUserQuestion：确认匹配范围 + 预览列表 |
| 🟡 中危 | 修改系统环境变量 | `setx PATH ...`、`powershell [Environment]::SetEnvironmentVariable` | AskUserQuestion：确认影响范围 + 是否仅当前会话 |
| 🟡 中危 | 网络下载/上传 | `curl -O`、`Invoke-WebRequest`、`ftp` | AskUserQuestion：确认 URL 安全性 + 保存路径 |
| 🟡 中危 | 修改注册表 | `reg add`、`powershell Set-ItemProperty` | AskUserQuestion：确认注册表路径 + 修改值 |
| 🟢 低危 | 创建目录 | `mkdir`、New-Item -ItemType Directory | 无需确认 |
| 🟢 低危 | 查看文件内容 | `type`、`Get-Content` | 无需确认 |
| 🟢 低危 | 列出文件 | `dir`、`Get-ChildItem` | 无需确认 |

### 确认对话框模板

执行高危操作前，向用户展示以下信息：

1. **操作意图**：我要删除/覆盖/修改什么？
2. **影响范围**：涉及哪些文件/目录？（列出具体路径）
3. **备份建议**：是否需要先备份？
4. **选项**：
   - 确认执行
   - 先备份再执行
   - 取消操作

**示例**：
```
操作：删除 results/train/ 目录下的所有内容（共 15 个文件，3 个子目录）
影响：该目录包含 A2C 算法的训练日志，删除后不可恢复
建议：是否先备份到 results/train_backup/？
选项：① 直接删除 ② 先备份再删除 ③ 取消
```

### 禁止直接执行的操作（即使白名单已授权）

以下操作**永远禁止自动执行**，无论白名单中是否有 `Bash(cmd /c *)`：
- 格式化磁盘或分区（`format`、`diskpart`）
- 删除项目根目录（`rmdir /s /q E:/Project_IEEE39`）
- 删除用户主目录内容（`del /q C:/Users/...`）
- 修改系统关键文件（`C:/Windows/`、`C:/Program Files/`）
- 执行未知来源的 `.bat`、`.ps1`、`.exe` 文件

## 规则

- **Windows 上不用 `ls`/`grep`/`rm`**，即使它们在某些环境下存在（Git Bash），也不要用，避免跨 session 不一致。
- **简单任务用 `cmd /c`**，复杂任务用 `powershell -Command`**，不要混用。
- **路径统一正斜杠** `/`，只在必要时用 `\\`。
- **权限预申请**：在执行批量操作前，检查 `settings.local.json` 是否已包含 `Bash(cmd /c *)` 和 `Bash(powershell -Command *)`，若未包含，提示用户添加。
- **危险操作必确认**：任何涉及删除、覆盖、批量修改的命令，必须先 AskUserQuestion，不得直接调用 Bash 工具。
