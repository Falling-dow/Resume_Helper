import argparse
from pdf_extract import extract_text_from_pdf
from llm_tailor import tailor_resume_text
#from docx_render import md_to_docx
from md2pdf import md_to_latex_to_pdf


def main():
    parser = argparse.ArgumentParser(description="JD+PDF 简历 → 改写并导出 DOCX")
    parser.add_argument("--jd", default="backend/app/ai/jd.txt", help="JD 文本文件路径")
    parser.add_argument("--pdf", default="backend/app/ai/test_Resume.pdf", help="PDF 简历路径")
    parser.add_argument("--out-md", default="backend/app/ai/resume_tailored.md")
    #parser.add_argument("--out-docx", default="backend/app/ai/resume_tailored.docx")
    parser.add_argument("--out-pdf", default="backend/app/ai/resume_tailored.pdf")
    args = parser.parse_args()

    # 1) PDF → 文本
    pdf_text = extract_text_from_pdf(args.pdf)
    if len(pdf_text) < 30:
        raise RuntimeError("PDF解析失败或文本过短（若为扫描件请安装 poppler + tesseract）。")

    # 2) 读 JD
    with open(args.jd, "r", encoding="utf-8") as f:
        jd_text = f.read().strip()

    # 3) 调 R1 改写为 Markdown
    md_text = tailor_resume_text(jd_text, pdf_text, out_fmt="markdown")
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(md_text)
    print("[OK] Markdown 输出 →", args.out_md)

    # 4) Markdown → latex → PDF
    md_to_latex_to_pdf(md_text, args.out_pdf)
    print("[OK] pdf 输出 →", args.out_pdf)

if __name__ == "__main__":
    main()
