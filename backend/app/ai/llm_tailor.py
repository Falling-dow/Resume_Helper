from typing import Literal
from config import get_client
from utils import detect_lang

def tailor_resume_text(
    jd_text: str,
    resume_text: str,
    out_fmt: Literal["markdown","plain"]="markdown"
) -> str:
    """
    用 DeepSeek-R1 改写简历，强制分节顺序：
    1) 教育经历 / Education
    2) 实习/工作经历（其后可接科研经历/Research）/ Experience (+ Research)
    3) 技能 / Skills
    （可选：项目经历 / Projects，荣誉/证书 / Awards & Certificates）
    """
    client = get_client()
    lang = detect_lang(resume_text)

    # 语言与分节规范
    lang_rule = (
        "The output language MUST strictly match the original resume language. "
        "If the resume is Chinese, output in Chinese; if it is English, output in English. "
    )
    zh_extra = (
        "When the output is Chinese, DO NOT include a Summary/摘要 section. "
        "Use the following section order and titles exactly (omit empty ones):\n"
        "1) 教育背景\n"
        "2) 实习经历（若有全职可合并命名为 工作/实习经历）\n"
        "3) 科研经历（可选；如条目较少，也可并入上一节末尾）\n"
        "4) 项目经历（可选）\n"
        "5) 技能\n"
        "6) 荣誉/证书（可选）\n"
        "Each position/education headline MUST be a single Markdown line in the form:\n"
        "### 机构或公司 | 岗位或学位(可选) | 起止日期 | 地点(可选)\n"
        "For bullets: concise, data-backed when available, no fabrication."
    )
    en_extra = (
        "Do NOT include a Summary section. "
        "Use the following section order and titles exactly (omit empty ones):\n"
        "1) Education\n"
        "2) Experience\n"
        "3) Research Experience (optional; if short, may be appended after Experience)\n"
        "4) Projects (optional)\n"
        "5) Skills\n"
        "6) Awards & Certificates (optional)\n"
        "Each headline MUST be a single Markdown line in the form:\n"
        "### Organization | Title or Degree (optional) | Dates | Location (optional)\n"
        "Bullets must be concise and factual (no fabrication)."
    )

    system_msg = (
        "You are a senior resume editor. "
        "Task: rewrite the entire resume TEXT to best match the JD while preserving factual information. "
        "Do NOT fabricate or invent facts, dates, employers, degrees, or metrics. "
        "Use concise bullets, strong action verbs, and JD keywords naturally. "
        "Reorder sections if needed. Keep length reasonable. "
        + lang_rule +
        (zh_extra if lang == "zh" else en_extra) +
        " The final document MUST follow the section order above. "
        "Avoid duplicate content across sections; merge overlapping items sensibly. "
        f"Output format: {out_fmt}. Return ONLY the content between <OUTPUT> and </OUTPUT>."
    )

    user_msg = f"""
[JD]
{jd_text}

[ORIGINAL_RESUME_TEXT]
{resume_text}

[REWRITE_REQUIREMENTS]
- No fabrication. If a point lacks numbers, improve wording but do not invent metrics.
- Prioritize JD-relevant skills/experience; de-emphasize or remove irrelevant content.
- Prefer short, scannable bullets (1–2 lines each).
- Keep names, dates, institutions factual.
- If conflicting info appears, choose the safer/less specific variant without creating new facts.
- Ensure the section ORDER matches the spec in the system message.

Return:
<OUTPUT>
(the full rewritten resume here in {out_fmt})
</OUTPUT>
"""

    resp = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=8000,
    )
    txt = resp.choices[0].message.content
    start = txt.find("<OUTPUT>")
    end = txt.find("</OUTPUT>")
    return txt[start+8:end].strip() if start != -1 and end != -1 else txt.strip()
