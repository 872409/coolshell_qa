"""
    Description: QA 工具
    Changelog: all notable changes to this file will be documented
"""
import os

import openai

from src.config import Config

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")


def embedding_by_openai(text: str) -> list():
    """
    基于 OpenAI 对文本进行 Embedding
    Args:
        text (str): 输入文本

    Returns:
        _type_: 向量化后的值
    """

    sentence_embeddings = openai.Embedding.create(
        model="text-embedding-ada-002", input=text
    )
    result = None
    try:
        result = sentence_embeddings["data"][0]["embedding"]
    except Exception as e:
        Config.LOGGER.error(f"OpenAI Embedding Failed!: {e}")
    return result


def openai_chat(engine: str, messages: list, temperature: float = 0.6) -> str:
    """
    基于 openai 聊天
    Args:
        engine (str): 模型引擎名称
        messages (list): 消息列表

    Returns:
        str: 返回的消息
    """
    engine = engine or "gpt-3.5-turbo"
    completion = openai.ChatCompletion.create(
        temperature=temperature,
        model=engine,
        messages=messages,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    res = embedding_by_openai("hi")
    print(type(res), len(res))
