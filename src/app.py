"""
    Created by howie.hu at 2023-05-15.
    Description: 接口入口
    Changelog: all notable changes to this file will be documented
"""

from flask import Flask, request

from src.qa.ask import ask

app = Flask(__name__)


@app.route("/qa", methods=["POST"])
def qa():
    """
    问答接口
    """
    post_data: dict = request.json
    text = str(post_data.get("text", "")).strip()
    result = {"data": ask(text), "status": 1}
    return result


if __name__ == "__main__":
    app.run()
