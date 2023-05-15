"""
    Description: 配置类
    Changelog: all notable changes to this file will be documented
"""

import logging
import os

import openai


def get_logger(name="CoolShell QA"):
    """
    初始化内部日志
    Args:
        name (str, optional): _description_. Defaults to "Flask API".

    Returns:
        _type_: 日志实例
    """
    logging_format = f"[%(asctime)s] %(levelname)-5s %(name)-{len(name)}s "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    )
    return logging.getLogger(name)


class Config:
    """
    Basic config
    """

    TIMEZONE = "Asia/Shanghai"
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    HTML_DIR = os.path.join(DATA_DIR, "html")
    DB_DIR = os.path.join(DATA_DIR, "db")
    DB_PATH = os.path.join(DB_DIR, "coolshell_qa")
    DB_COLL_NAME = "coolshell_qa_v1"
    LOGGER = get_logger()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

if __name__ == "__main__":
    print(Config.HTML_DIR)
