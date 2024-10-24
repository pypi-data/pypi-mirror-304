# init_client, LLM_CFG
import os, datetime, traceback, functools
from typing import List, Dict, Optional, Union
from .openai_client import OpenAIClient

LLM_CFG = {}
def add_openai_models():
    global LLM_CFG
    model_list = [
        "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4",
    ]
    for model in model_list:
        assert model not in LLM_CFG, f"{model} already in LLM_CFG"
        LLM_CFG[model] = {
            "model_name": model,
            "base_url": os.getenv("OPENAI_BASE_URL"),
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
add_openai_models()

def init_client(llm_cfg:Dict):
    # global client
    base_url = os.getenv("OPENAI_BASE_URL") if llm_cfg.get("base_url") is None else llm_cfg["base_url"]
    api_key = os.getenv("OPENAI_API_KEY") if llm_cfg.get("api_key") is None else llm_cfg["api_key"]
    model_name = llm_cfg.get("model_name", "gpt-4o")
    client = OpenAIClient(
        model_name=model_name, base_url=base_url, api_key=api_key, is_sn=llm_cfg.get("is_sn", False)
    )
    return client
