from pathlib import Path

from pypdf import PdfReader


class PDFService:
    """负责从文本型 PDF 中提取每一页的文字。"""

    def extract_pages(
        self,
        pdf_path: str | Path,
    ) -> list[str]:
        """按原页码顺序返回每一页的文本。"""
        path = Path(pdf_path)

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"PDF 文件不存在：{path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("只支持 PDF 文件")

        reader = PdfReader(path)
        pages: list[str] = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text.strip())

        if not any(pages):
            raise ValueError(
                "没有提取到文本，请确认 PDF 包含可复制的文字"
            )

        return pages