import os
from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def get_client() -> OpenAI:
    """
    从环境变量读取 key，避免把 key 写进代码：
    export DEEPSEEK_API_KEY="sk-xxxx"
    """
    #api_key = os.getenv("DEEPSEEK_API_KEY")
    api_key = "sk-fab5178562954049b31b7810cdbdadfe"
    if not api_key:
        raise RuntimeError("请先设置环境变量 DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
