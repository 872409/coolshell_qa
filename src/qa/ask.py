"""
    Description: 问答入口
    Changelog: all notable changes to this file will be documented
"""

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from src.config import Config
from src.qa.utils import embedding_by_openai, openai_chat

PROMPT_SYSTEM = "你是 CoolShell 问答机器人，由[陈皓](https://github.com/haoel)（左耳朵耗子）创办，博客内容涉及编程、技术、管理等方面。你可以基于上下文中的博客文章信息对用户的提问进行回答"
PROMPT_CONTEXT = """
We have provided context information below:
------------------------
{0}
------------------------
Instructions: Respond to user query using context results. The answer uses the Markdown syntax.
If the question is unrelated to the context, kindly inform that you can only answer questions relevant to the given context.
Please answer my question in the same language that I used to ask you.
My question is: 
{1}
"""

qdrant_client = QdrantClient(path=Config.DB_PATH)
collection_name = Config.DB_COLL_NAME


def ask(text: str, limit: int = 1) -> str:
    """
    提问
    Args:
        text (str):     问题
        limit (int):    搜索数量

    Returns:
        str: 答案
    """
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=embedding_by_openai(text),
        limit=limit,
        search_params={"exact": False, "hnsw_ef": 128},
    )
    data = []
    for each in search_result:
        data.append(each.payload)

    context = ""
    for _, each in enumerate(data):
        date = each["date"]
        description = str(each.get("description", "")).strip()
        content = str(each.get("content", "")).strip()
        title = each["title"]
        url = each["url"]
        final_content = description or content
        context += f"Title: {title}\npublish date: {date}\nurl: {url}\ncontent: {final_content}"

    content = PROMPT_CONTEXT.format(context.strip(), text)
    messages = [
        {
            "role": "system",
            "content": PROMPT_SYSTEM,
        },
        # {"role": "user", "content": "你是谁？做个自我介绍吧"},
        # {"role": "assistant", "content": "好的，我是 CoolShell 问答机器人，由陈皓（左耳朵耗子）创办。"},
        {"role": "user", "content": content},
    ]
    return openai_chat(engine="gpt-3.5-turbo", messages=messages)


if __name__ == "__main__":
    print(ask(text="简单说下 XY problem"))
