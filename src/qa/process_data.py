"""
    Description: 文章数据处理
    Changelog: all notable changes to this file will be documented
"""

import json
import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from src.config import Config
from src.qa.utils import embedding_by_openai

json_file_path = os.path.join(Config.DATA_DIR, "json/data.json")
db_path = os.path.join(Config.DB_DIR, "coolshell_qa")

qdrant_client = QdrantClient(path=db_path)
collection_name = "coolshell_qa_v1"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

with open(json_file_path, "r", encoding="utf-8") as fp:
    data = json.load(fp)
    for index, each in enumerate(data):
        date = each["date"]
        description = str(each.get("description", "")).strip()
        content = str(each.get("content", "")).strip()
        title = each["title"]
        url = each["url"]
        final_content = description or content
        text = f"文章标题：{title}\n 发表时间: {date}\n 文章链接: {url}\n 文章内容: {final_content}"
        qdrant_client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[
                PointStruct(
                    id=index,
                    vector=embedding_by_openai(text),
                    payload=each,
                ),
            ],
        )
