"""
    Description: 推荐文章 Item
        eg: pipenv run python ./src/spider/item_featured.py
    Changelog: all notable changes to this file will be documented
"""
import asyncio
import json
import os

from ruia import AttrField, HtmlField, Item, RegexField, Spider, TextField

from src.config import Config


class ItemFeatured(Item):
    """
    文章 Item
    """

    target_item = TextField(css_select="ul.featured-post li")
    title = TextField(css_select="li a")
    url = AttrField(css_select="li a", attr="href")
    date = TextField(css_select="#date")
    author = TextField(css_select="#author")


async def run():
    """
    运行
    """
    file_path = os.path.join(Config.HTML_DIR, "featured.html")
    content = ""
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        async for item in ItemFeatured.get_items(html=html):
            item = item.results
            content += f"{item['date']} {item['title']} —— {item['author']}\n"
            # content += f"{item['date']} [{item['title']}]({item['url']}) —— {item['author']}\n"
    print(json.dumps({"content": content}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(run())
