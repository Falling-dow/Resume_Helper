# md2pdf.py
import os
import re
import shutil
import subprocess
import tempfile
from typing import Optional

# ---------- 工具 ----------
def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

_LATEX_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}

def _latex_escape(s: str) -> str:
    s = s.replace("\\", _LATEX_ESCAPE_MAP["\\"])
    for k, v in _LATEX_ESCAPE_MAP.items():
        if k == "\\":
            continue
        s = s.replace(k, v)
    return s

def _md_inline_to_latex(line: str) -> str:
    # 保护 `code`
    code_spans = []
    def _cap(m):
        code_spans.append(m.group(1))
        return f"@@CODE{len(code_spans)-1}@@"
    line = re.sub(r"`([^`]+)`", _cap, line)

    # **bold** / __bold__
    line = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", line)
    line = re.sub(r"__(.+?)__", r"\\textbf{\1}", line)
    # *italic* / _italic_
    line = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"\\emph{\1}", line)
    line = re.sub(r"_(.+?)_", r"\\emph{\1}", line)

    # 先转义，再还原 code
    def _restore(m):
        idx = int(m.group(1))
        return r"\texttt{" + _latex_escape(code_spans[idx]) + "}"
    line = _latex_escape(line)
    line = re.sub(r"@@CODE(\d+)@@", _restore, line)
    return line

# ---------- Markdown → LaTeX（按你的导言区） ----------
PREAMBLE = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{fontawesome5}

% Remove page numbers
\pagestyle{empty}

% Configure hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    urlcolor=blue!70!black,
}

% Section formatting
\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{3pt}{7pt}

% Subsection formatting
\titleformat{\subsection}[runin]{\bfseries}{}{0em}{}[]
\titlespacing{\subsection}{0pt}{0pt}{5pt}

% Remove paragraph indentation
\setlength{\parindent}{0pt}
"""

def _parse_header(md_text: str):
    """
    从 Markdown 头两行提取：
    - 第1行：# 姓名
    - 第2行：联系方式（可选）
    返回 (name, contact, start_index_after_header)
    """
    lines = md_text.splitlines()
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
    return name, contact, i, lines

def _md_body_to_latex(lines, start_idx: int) -> str:
    """
    极简 Markdown → LaTeX：
    - # / ## / ### → \section / \subsection / \subsubsection
    - 列表：- / * 开头 → itemize
    - 支持 **bold** *italic* `code`
    - ``` 三引号代码块 → verbatim
    """
    out = []
    in_code_block = False
    in_itemize = False

    def _open_items():
        nonlocal in_itemize
        if not in_itemize:
            out.append(r"\begin{itemize}[leftmargin=*, topsep=0pt, itemsep=1pt]")
            in_itemize = True
    def _close_items():
        nonlocal in_itemize
        if in_itemize:
            out.append(r"\end{itemize}")
            in_itemize = False

    for idx in range(start_idx, len(lines)):
        raw = lines[idx]
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            if not in_code_block:
                _close_items()
                in_code_block = True
                out.append(r"\begin{verbatim}")
            else:
                in_code_block = False
                out.append(r"\end{verbatim}")
            continue

        if in_code_block:
            out.append(line)
            continue

        if not line.strip():
            _close_items()
            out.append("")
            continue

        # 标题
        if line.startswith("# "):
            _close_items()
            out.append(r"\section{" + _latex_escape(line[2:].strip()) + "}")
            continue
        if line.startswith("## "):
            _close_items()
            out.append(r"\section{" + _latex_escape(line[3:].strip()) + "}")
            continue
        if line.startswith("### "):
            _close_items()
            out.append(r"\subsection{" + _latex_escape(line[4:].strip()) + "}")
            continue

        # 列表
        if line.lstrip().startswith(("- ", "* ")):
            _open_items()
            item = line.lstrip()[2:]
            out.append(r"\item " + _md_inline_to_latex(item))
            continue

        # 普通段落
        _close_items()
        out.append(_md_inline_to_latex(line))

    _close_items()
    return "\n".join(out)

def _assemble_latex(md_text: str) -> str:
    name, contact, start_idx, lines = _parse_header(md_text)

    # Header block（使用你的风格；如果没提供 name/contact 就跳过）
    header = ""
    if name:
        header += r"\begin{center}" + "\n"
        header += r"    {\LARGE \textbf{" + _latex_escape(name) + r"}} \\" + "\n"
        if contact:
            header += r"    \vspace{2pt}" + "\n"
            header += "    " + _latex_escape(contact) + "\n"
        header += r"\end{center}" + "\n\n"

    body = _md_body_to_latex(lines, start_idx)

    return (
        PREAMBLE
        + "\n\\begin{document}\n\n"
        + header
        + body
        + "\n\n\\end{document}\n"
    ).strip()

# ---------- 编译 ----------
def _compile_latex(tex_path: str, out_pdf: str):
    out_dir = os.path.dirname(os.path.abspath(out_pdf)) or "."
    engine = _which("xelatex") or _which("pdflatex")
    if not engine:
        print(f"[WARN] 未找到 xelatex/pdflatex。已导出 LaTeX 源文件：{tex_path}")
        print("       你可以将该 .tex 上传到 Overleaf 或安装 MacTeX/TeX Live 后本地编译。")
        return

    base = os.path.splitext(os.path.basename(out_pdf))[0]
    # 调整输出目录为 out_pdf 当前目录
    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", tex_path]
    # 编译两遍以稳定目录/引用
    subprocess.run(cmd, cwd=out_dir, check=True)
    subprocess.run(cmd, cwd=out_dir, check=True)

    # 清理中间文件
    stem = os.path.splitext(os.path.basename(tex_path))[0]
    for ext in (".aux", ".log", ".out", ".toc"):
        p = os.path.join(out_dir, stem + ext)
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

def md_to_latex_to_pdf(md_text: str, out_pdf: str):
    """
    Markdown → LaTeX（使用提供的导言区）→ PDF
    - 若有 xelatex 或 pdflatex：直接编译 PDF
    - 否则：仅导出 .tex，并提示后续处理方式
    """
    out_dir = os.path.dirname(os.path.abspath(out_pdf)) or "."
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(out_pdf))[0]
    tex_path = os.path.join(out_dir, base + ".tex")

    tex = _assemble_latex(md_text)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    _compile_latex(tex_path, out_pdf)
    if os.path.exists(out_pdf):
        print("[OK] PDF 输出 →", out_pdf)
    else:
        print("[INFO] PDF 未生成（缺少 LaTeX 引擎）。已输出 .tex →", tex_path)
