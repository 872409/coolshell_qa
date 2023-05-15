"""
    Description: 文章 Item
        eg: pipenv run python ./src/spider/item_article.py
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import json
import os

from ruia import AttrField, HtmlField, Item, RegexField, Spider, TextField

from src.config import Config


class ItemArticle(Item):
    """
    文章 Item
    """

    target_item = TextField(css_select="#main .post-content")
    title = TextField(css_select="h2.entry-title a")
    url = AttrField(css_select="h2.entry-title a", attr="href")
    date = AttrField(css_select="time.entry-date", attr="datetime")
    description = TextField(css_select="div.entry-content")


async def run():
    """
    运行
    """
    page_path = os.path.join(Config.HTML_DIR, "pages")
    target_data = []
    for page in range(1, 75):
        each_file = f"page_{page}.html"
        Config.LOGGER.info(f"解析页面: {each_file}")
        if str(each_file).startswith("page"):
            each_file = os.path.join(page_path, each_file)
            with open(each_file, "r", encoding="utf-8") as f:
                html = f.read()
                async for item in ItemArticle.get_items(html=html):
                    item_data = {"content": ""}
                    item_data.update(item.results)
                    target_data.append(item_data)
    # 持久化到 json
    json_file_path = os.path.join(Config.DATA_DIR, "json/articles.json")
    with open(json_file_path, "w", encoding="utf-8") as fp:
        json.dump(target_data, fp, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(run())
