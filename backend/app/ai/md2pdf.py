# md2pdf.py
import os
import re
import subprocess
import shutil
from typing import Optional

# -------------------- utils --------------------
def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

# 重要：不转义 { }，也不转义反斜杠 \ ，避免破坏 \textbf{...} 这类命令
_LATEX_ESCAPE_MAP = {
    # "\\": r"\textbackslash{}",   # 不转义反斜杠
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

def _latex_escape(s: str) -> str:
    if s is None:
        return ""
    for k, v in _LATEX_ESCAPE_MAP.items():
        s = s.replace(k, v)
    return s

def _md_inline_to_latex(line: str) -> str:
    """
    行内 Markdown → LaTeX（顺序很关键）：
    1) 先提取并占位 `code`
    2) 再对“非代码”的文本做转义（不会动 { } 和 \）
    3) 最后把 **...** / *...* / __...__ / _..._ 等替换成 \textbf / \emph
    4) 还原代码为 \texttt{...}
    """
    # 1) 提取代码片段
    codes: list[str] = []
    def _cap(m):
        codes.append(m.group(1))
        return f"@@CODE{len(codes)-1}@@"
    line = re.sub(r"`([^`]+)`", _cap, line)

    # 2) 先对当前字符串做转义（不会影响我们后面插入的 LaTeX 命令）
    line = _latex_escape(line)

    # 3) 行内粗斜体
    line = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", line)
    line = re.sub(r"__(.+?)__", r"\\textbf{\1}", line)
    line = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"\\emph{\1}", line)
    line = re.sub(r"_(.+?)_", r"\\emph{\1}", line)

    # 4) 还原代码片段（对代码内容做 LaTeX 转义以保证安全）
    def _restore(m):
        idx = int(m.group(1))
        return r"\texttt{" + _latex_escape(codes[idx]) + "}"
    line = re.sub(r"@@CODE(\d+)@@", _restore, line)
    return line

# -------------------- parse header --------------------
_EMAIL_PAT = re.compile(r"([\w\.-]+@[\w\.-]+\.\w+)$")

def _parse_header(md_text: str):
    """
    解析 Markdown 顶部：
    - 第1行：# 姓名
    - 第2行：联系方式（电话/邮箱/链接）
    - 第3行：若是“纯邮箱”，自动并入联系方式
    返回：name, contact, body_lines
    """
    lines = [ln.rstrip() for ln in md_text.splitlines()]
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    name = ""
    contact = ""
    if i < len(lines) and lines[i].startswith("# "):
        name = lines[i][2:].strip()
        i += 1
        if i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
            contact = lines[i].strip()
            i += 1
        # 第三行若是“单独邮箱”，并入 contact
        if i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
            maybe_email = lines[i].strip()
            if _EMAIL_PAT.search(maybe_email) and len(maybe_email.split()) == 1:
                if contact:
                    contact = f"{contact} | {maybe_email}"
                else:
                    contact = maybe_email
                i += 1

    body_lines = lines[i:]
    return name, contact, body_lines

def _contact_to_latex(contact: str) -> str:
    """
    把“电话/邮箱/链接 …”转成带图标的 LaTeX。
    - 去掉 **bold** / *italic* 等 Markdown 痕迹
    - 支持以 | · • 、中文/英文逗号、分号、两个以上空格分隔
    """
    if not contact:
        return ""

    # 清理 Markdown 强调符
    contact = re.sub(r"\*\*(.*?)\*\*", r"\1", contact)
    contact = re.sub(r"__(.*?)__", r"\1", contact)
    contact = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"\1", contact)
    contact = contact.strip()

    parts = re.split(r"\s*[|·•，,;；]\s*|\s{2,}", contact)
    out_parts = []
    for p in parts:
        p = p.strip()
        if not p:
            continue

        # 去掉“Phone: / 电话： / Email: / 邮箱：”前缀
        p_clean = re.sub(r"^(phone|tel|电话)[:：]\s*", "", p, flags=re.I)
        p_clean = re.sub(r"^(email|e-mail|邮箱)[:：]\s*", "", p_clean, flags=re.I)

        # email
        m = _EMAIL_PAT.search(p_clean)
        if m:
            addr = m.group(1)
            out_parts.append(r"\faEnvelope\ \href{mailto:%s}{%s}" % (addr, _latex_escape(addr)))
            continue

        # phone（简单匹配）
        if re.search(r"\+?\d[\d\-\s()]{5,}", p_clean):
            out_parts.append(r"\faPhone\ " + _latex_escape(p_clean))
            continue

        # url
        if re.search(r"https?://", p_clean, re.I):
            low = p_clean.lower()
            if "linkedin" in low:
                out_parts.append(r"\faLinkedin\ \href{%s}{LinkedIn}" % _latex_escape(p_clean))
            elif "github" in low:
                out_parts.append(r"\faGithub\ \href{%s}{GitHub}" % _latex_escape(p_clean))
            else:
                out_parts.append(r"\href{%s}{%s}" % (_latex_escape(p_clean), _latex_escape(p_clean)))
            continue

        # 兜底：原样文本（如“上海”）
        out_parts.append(_latex_escape(p_clean))

    return r" \quad ".join(out_parts)

# -------------------- md -> LaTeX body --------------------
def _md_to_latex_body(lines):
    """
    极简 Markdown -> LaTeX：
    - ##, ### -> \section / \subsection*
    - - / * 列表 -> itemize
    - ``` 代码块
    - 行内 **/*** 等
    - 跳过正文里独立的联系方式行
    """
    # 预过滤重复联系方式行
    filtered = []
    for raw in lines:
        if re.match(r"\s*\*{0,2}\s*(email|e-mail|phone|tel|邮箱|电话)\s*[:：]", raw, flags=re.I):
            continue
        # 单独的纯邮箱行也跳过（已并入 header）
        if _EMAIL_PAT.search(raw.strip()) and len(raw.strip().split()) == 1:
            continue
        filtered.append(raw)
    lines = filtered

    out = []
    in_code = False
    in_item = False

    def open_items():
        nonlocal in_item
        if not in_item:
            out.append(r"\begin{itemize}[leftmargin=*, topsep=0pt, itemsep=1pt]")
            in_item = True

    def close_items():
        nonlocal in_item
        if in_item:
            out.append(r"\end{itemize}")
            in_item = False

    for raw in lines:
        line = raw.rstrip("\n")

        # 代码块 fence
        if line.strip().startswith("```"):
            if not in_code:
                close_items()
                out.append(r"\begin{verbatim}")
                in_code = True
            else:
                out.append(r"\end{verbatim}")
                in_code = False
            continue
        if in_code:
            out.append(line)
            continue

        # 空行
        if not line.strip():
            close_items()
            out.append("")
            continue

        # 标题（一级标题在页眉已处理；正文从 ## 开始）
        if line.startswith("## "):
            close_items()
            title = line[3:].strip()
            out.append(r"\section{%s}" % _latex_escape(title))
            continue
        if line.startswith("### "):
            close_items()
            title = line[4:].strip()
            out.append(r"\subsection*{%s}" % _latex_escape(title))
            continue

        # 列表
        if line.lstrip().startswith(("- ", "* ")):
            open_items()
            item = line.lstrip()[2:]
            out.append(r"\item " + _md_inline_to_latex(item))
            continue

        # 段落
        close_items()
        out.append(_md_inline_to_latex(line))

    close_items()
    return "\n".join(out)

# -------------------- LaTeX 模板 --------------------
_TEMPLATE = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{fontawesome5}

\pagestyle{empty}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    urlcolor=blue!70!black,
}

\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{3pt}{7pt}

\titleformat{\subsection}[runin]{\bfseries}{}{0em}{}[]
\titlespacing{\subsection}{0pt}{0pt}{5pt}

\setlength{\parindent}{0pt}

\begin{document}

% Header
\begin{center}
    {\fontsize{26}{28}\selectfont \textbf{%(NAME)s}} \\
    \vspace{2pt}
    %(CONTACT)s
\end{center}

%(BODY)s

\end{document}
""".strip()

# -------------------- 编译 --------------------
def _compile_latex(tex_path: str, out_pdf: str):
    """
    优先 pdflatex；无则 xelatex；都没有则仅保留 .tex 并提示。
    """
    workdir = os.path.dirname(os.path.abspath(tex_path)) or "."
    base = os.path.splitext(os.path.basename(tex_path))[0]

    engine = _which("pdflatex") or _which("xelatex")
    if not engine:
        print(f"[WARN] 未找到 LaTeX 引擎（pdflatex/xelatex）。已导出 TEX：{tex_path}\n"
              f"你可以上传到 Overleaf 或安装 MacTeX/TeX Live 后本地编译。")
        return False

    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", base + ".tex"]
    subprocess.run(cmd, cwd=workdir, check=True)
    subprocess.run(cmd, cwd=workdir, check=True)

    gen_pdf = os.path.join(workdir, base + ".pdf")
    if os.path.abspath(gen_pdf) != os.path.abspath(out_pdf):
        shutil.move(gen_pdf, out_pdf)

    for ext in (".aux", ".log", ".out", ".toc"):
        p = os.path.join(workdir, base + ext)
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass
    return True

# -------------------- 公开 API --------------------
def md_to_latex_to_pdf(md_text: str, out_pdf: str):
    """
    Markdown → (模板)LaTeX → PDF
    - 自动解析 Markdown 顶部“# 姓名 / 联系方式”（第三行若是邮箱将并入）
    - 若无 LaTeX 引擎：仅导出 .tex 并提示（不抛异常）
    - 处理好 Python 与 LaTeX 的 % 冲突
    """
    name, contact, body_lines = _parse_header(md_text)
    body = _md_to_latex_body(body_lines)

    # 安全占位处理，避免 '%' 与 Python %-format 冲突
    safe_tpl = _TEMPLATE.replace("%(NAME)s", "<<NAME>>") \
                        .replace("%(CONTACT)s", "<<CONTACT>>") \
                        .replace("%(BODY)s", "<<BODY>>")
    safe_tpl = safe_tpl.replace("%", "%%")
    safe_tpl = safe_tpl.replace("<<NAME>>", "%(NAME)s") \
                       .replace("<<CONTACT>>", "%(CONTACT)s") \
                       .replace("<<BODY>>", "%(BODY)s")

    tex = safe_tpl % {
        "NAME": _latex_escape(name or "NAME"),
        "CONTACT": _contact_to_latex(contact),
        "BODY": body,
    }

    out_dir = os.path.dirname(os.path.abspath(out_pdf)) or "."
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(out_pdf))[0]
    tex_path = os.path.join(out_dir, base + ".tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    ok = _compile_latex(tex_path, out_pdf)
    if ok:
        print("[OK] 使用 LaTeX 引擎生成 PDF →", out_pdf)
    else:
        print("[OK] 仅生成 TEX（手动编译）→", tex_path)
