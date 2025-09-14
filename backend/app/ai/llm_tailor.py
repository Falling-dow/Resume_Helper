from typing import Literal
from config import get_client
from utils import detect_lang

def tailor_resume_text(jd_text: str, resume_text: str, out_fmt: Literal["markdown","plain"]="markdown") -> str:
    """
    调 DeepSeek R1（deepseek-reasoner），把 PDF 文本与 JD 合并改写为 Markdown。
    语言：严格跟随原简历语言（中文/英文）。
    中文：不生成摘要；建议使用 教育背景/实习经历/项目经历/技能/荣誉证书 等分节。
    """
    client = get_client()
    lang = detect_lang(resume_text)
    lang_rule = (
        "The output language MUST strictly match the original resume language. "
        "If the resume is Chinese, output in Chinese; if it is English, output in English. "
    )
    zh_extra = (
        "When the output is Chinese, DO NOT include a Summary/摘要 section; "
        "use section titles: 教育背景、实习经历、项目经历（如有）、研究经历（如有）、技能、荣誉/证书。 "
        "Each position/education line should be formatted like: "
        "### 机构或公司 | 岗位或学位(可选) | 起止日期 | 地点(可选)"
    )
    en_extra = ""

    system_msg = (
        "You are a senior resume editor. "
        "Task: rewrite the entire resume TEXT to best match the JD while preserving factual information. "
        "Do NOT fabricate or invent facts, dates, employers, degrees, or metrics. "
        "Use concise bullets, strong action verbs, and JD keywords naturally. "
        "Reorder sections if needed. Keep length reasonable. "
        + lang_rule +
        (zh_extra if lang == "zh" else en_extra) +
        f" Output format: {out_fmt}. Return ONLY the content between <OUTPUT> and </OUTPUT>."
    )

    user_msg = f"""
[JD]
{jd_text}

[ORIGINAL_RESUME_TEXT]
{resume_text}

[REWRITE_REQUIREMENTS]
- No fabrication. If a point lacks numbers, improve wording but do not invent metrics.
- Prioritize JD-relevant skills/experience; de-emphasize irrelevant content.
- Prefer short sentences and scannable bullets.
- Keep names, dates, institutions factual.
- If conflicting info appears, choose the safer/less specific variant without creating new facts.
- Optimize for ATS (keywords) but keep natural language.

Return:
<OUTPUT>
(the full rewritten resume here in {out_fmt})
</OUTPUT>
"""

    resp = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role":"system","content": system_msg},
            {"role":"user","content": user_msg},
        ],
        max_tokens=8000,
    )
    txt = resp.choices[0].message.content
    start = txt.find("<OUTPUT>")
    end = txt.find("</OUTPUT>")
    return txt[start+8:end].strip() if start != -1 and end != -1 else txt.strip()
