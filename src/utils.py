"""
    Description: 常用工具类
    Changelog: all notable changes to this file will be documented
"""
import html2text

from markdownify import markdownify as md
from readability import Document


def html_to_text_h2t(html: str) -> str:
    """
    从 html 提取核心内容 text
    Args:
        html (str): html

    Returns:
        _type_: text
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = False
    h.unicode_snob = False
    text = h.handle(html)
    return text.strip()


def extra_meta_from_article(html: str) -> dict:
    """
    提取文章类元信息，如：标题 内容等
    Args:
        html (str): html

    Returns:
        dict: {"content": "", "title": ""}
    """
    doc = Document(html)
    core_html = doc.summary()
    return {
        "title": doc.title(),
        "core_html": core_html,
        "core_text": html_to_text_h2t(core_html),
    }


if __name__ == "__main__":
    import os

    from src.config import Config

    file_path = os.path.join(Config.HTML_DIR, "featured.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        print(extra_meta_from_article(html=html))
