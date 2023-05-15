"""
    Description: 文章列表抓取，持久化成json文件
        eg: pipenv run python ./src/spider/req_html.py
    Changelog: all notable changes to this file will be documented
"""
import os
import subprocess
import time

from src.config import Config

for page in range(55, 75):
    file_path = os.path.join(Config.HTML_DIR, f"pages/page_{page}.html")
    result = subprocess.run(
        ["curl", f"https://coolshell.cn/page/{page}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.decode("utf-8")
    with open(file_path, "w", encoding="utf-8") as fp:
        fp.write(output)
    # time.sleep(1)
