"""扫描 ~/.agents/skills/ 下所有 SKILL.md，检测 description 是否为双语格式"""
import re
from pathlib import Path

SKILL_ROOT = Path.home() / ".agents" / "skills"
CJK_RE = re.compile(r'[一-鿿㐀-䶿]')
# Stricter English detection: look for English trigger sentences,
# not just embedded terms like "docx" or "Word"
EN_TRIGGER_RE = re.compile(
    r'(Use when|NOT for|Trigger|use when|not for|trigger|'
    r'Use before|use before|Use for|use for|'
    r'Does NOT|does not|Do NOT|do not|'
    r'Provides|provides|Must|must)'
)
SKIP_PREFIXES = ['gstack/', 'plugin/']


def extract_desc(filepath):
    text = filepath.read_text(encoding='utf-8')
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None
    for line in m.group(1).split('\n'):
        dm = re.match(r'^description:\s*(.+)', line)
        if dm:
            return dm.group(1).strip()
    return None


def has_chinese(text):
    return bool(CJK_RE.search(text))


def has_english_trigger(text):
    """Detect proper English trigger sentences, not just embedded terms."""
    return bool(EN_TRIGGER_RE.search(text))


def main():
    ok = []      # bilingual (both CN and EN)
    cn_only = [] # Chinese only, needs English
    en_only = [] # English only, needs Chinese
    skipped = []

    for md in sorted(SKILL_ROOT.rglob("SKILL.md")):
        rel = str(md.relative_to(SKILL_ROOT)).replace('\\', '/')
        if any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        desc = extract_desc(md)
        if desc is None:
            skipped.append((rel, "no description found"))
            continue

        cn = has_chinese(desc)
        en = has_english_trigger(desc)

        if cn and en:
            ok.append(rel)
        elif cn and not en:
            cn_only.append((rel, desc))
        elif en and not cn:
            en_only.append((rel, desc))
        else:
            skipped.append((rel, desc))

    print(f"[OK] 双语: {len(ok)}")
    print(f"[TODO] 仅中文（需加英文）: {len(cn_only)}")
    print(f"[TODO] 仅英文（需加中文）: {len(en_only)}")
    if skipped:
        print(f"[SKIP] 跳过: {len(skipped)}")
    print()

    if cn_only:
        print("=== 仅中文 → 需添加英文 ===")
        for rel, desc in cn_only:
            print(f"\n{rel}")
            print(f"  CN: {desc[:120]}")

    if en_only:
        print("\n=== 仅英文 → 需添加中文 ===")
        for rel, desc in en_only:
            print(f"\n{rel}")
            print(f"  EN: {desc[:120]}")


if __name__ == '__main__':
    main()
