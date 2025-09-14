import re

CJK_RE = re.compile(r"[\u4e00-\u9fff]")

def detect_lang(text: str) -> str:
    """检测是否包含 CJK 字符，返回 'zh' 或 'en'。"""
    return "zh" if CJK_RE.search(text or "") else "en"

def sanitize_inline_md(s: str) -> str:
    """去掉行内 **/__/*/_/` 等 Markdown 标记，保留纯文本。"""
    if not s: return s
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", s)
    s = re.sub(r"__(.*?)__", r"\1", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.*?)\*(?!\*)", r"\1", s)  # 避免把列表星号删掉
    s = re.sub(r"_(.*?)_", r"\1", s)
    s = re.sub(r"`(.*?)`", r"\1", s)
    return re.sub(r"[ \t]+", " ", s).strip()
