""" 
https://github.com/openai/openai-python
"""

import sys, os, json, re, time, requests, yaml, traceback
from typing import List, Dict, Optional, Tuple, Union
import openai
from openai.types.chat import ChatCompletion
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .formater import Formater

def stream_generator(response, is_openai=True):
    if is_openai:
        for chunk in response:
            yield chunk.choices[0].delta.content or ""
    else:
        ret = ""
        for chunk in response.iter_lines():
            chunk_ret = json.loads(chunk)['response'].strip() 
            # yield json.loads(chunk)['response'].strip() or ""
            yield chunk_ret[len(ret):]
            ret = chunk_ret

class OpenAIClient:
    base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4o"
    client: openai.OpenAI = None
    temperature: float = 0.5
    max_tokens: int = 4096

    retries: int = 3
    backoff_factor: float = 0.5
    n_thread:int = 5
    
    is_sn: bool = False             # SN model

    def __init__(
        self, model_name:str=None, temperature:float=None, max_tokens:int=None,
        base_url=f"https://api.openai.com/v1", api_key=None, print_url=False, 
        is_sn:bool=None
    ):
        if not api_key:
            print(f"[WARNING] api_key is None, please set it in the environment variable (OPENAI_API_KEY) or pass it as a parameter.")
        if print_url:
            print(f"[INFO] base_url: {base_url}")
        self.base_url = base_url
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        if model_name: self.model_name = model_name
        if temperature: self.temperature = temperature
        if max_tokens: self.max_tokens = max_tokens

        if is_sn is not None: self.is_sn = is_sn

    @staticmethod
    def _process_text_or_conv(query: str = None, messages: List[Dict] = None):
        if query is not None:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        elif messages is not None: pass
        else: raise ValueError("query or messages should be specified")
        return messages
    
    def _process_openai_args(self, args: Dict):
        if "model" not in args: args["model"] = self.model_name
        if "max_tokens" not in args: args["max_tokens"] = self.max_tokens
        if "temperature" not in args: args["temperature"] = self.temperature
        return args

    def query_one_raw(self, query: str = None, messages: List[Dict] = None, **args) -> ChatCompletion:
        messages = self._process_text_or_conv(query, messages)
        args = self._process_openai_args(args)
        chat_completion: ChatCompletion = self.client.chat.completions.create(messages=messages, **args)
        return chat_completion

    def query_one(
        self, 
        query: str = None, messages: List[Dict] = None, 
        return_model=False, return_usage=False, 
        **args
    ) -> Union[str, Tuple[str, ...]]:
        """ Get one response from OpenAI-fashion API
        Args:
            query or messages: input
            return_model, return_usage: control the output
        """
        messages = self._process_text_or_conv(query, messages)
        args = self._process_openai_args(args)
        # make query with retries
        for attempt in range(self.retries):
            try:
                chat_completion: ChatCompletion = self.client.chat.completions.create(messages=messages, **args)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                time.sleep(self.backoff_factor * (2 ** attempt))
        else:
            raise Exception(f"Failed to get response after {self.retries} attempts.")
        # prepare the output
        if not return_model and not return_usage:
            return chat_completion.choices[0].message.content
        res = (chat_completion.choices[0].message.content, )
        if return_usage: return_model = True
        if return_model:
            res = res + (chat_completion.model, )
            if return_usage: res = res + (chat_completion.usage.to_dict(), )
        return res
    
    def query_one_stream_generator(self, text, stop=None) -> None:
        if not self.is_sn:
            response = self.client.chat.completions.create(
                messages=[{ "role": "user", "content": text,}],
                model=self.model_name,
                temperature=self.temperature,
                stream=True,
                stop=stop
            )
            stream = stream_generator(response, is_openai=True)
        else:
            pload = {
                'question': [{"role": "user", "content": text}],
                'messages_format': True,
            }
            response = requests.post(
                self.base_url + "/forward_stream",
                json=pload,
                stream=True,
            )
            stream = stream_generator(response, is_openai=False)
        return stream
    
    def query_one_stream(self, text, stop=None, print_stream=True) -> None:
        res = ""
        stream = self.query_one_stream_generator(text, stop)
        for text in stream:
            res += text
            if print_stream:
                print(f"\033[90m{text}\033[0m", end="")
        if print_stream: print("\n")
        return res


    def query_many(self, texts, stop=None, temperature=None, model_id=None) -> list:
        # == 这样发送请求，会导致结果顺序错乱 ==
        # results = []
        # with ThreadPoolExecutor(max_workers=self.n_thread) as executor:
            # futures = {executor.submit(self.query_one, text, stop, temperature, model_id): text for text in texts}
            # for future in tqdm(as_completed(futures), total=len(texts), desc="Querying"):
            # futures = [executor.submit(self.query_one, text, stop, temperature, model_id) for text in texts]
            # for future in tqdm(futures, total=len(texts), desc="Querying"):
        # == 这样发送请求，保证了结果的顺序 ==
        # -- v1
        # results = [None] * len(texts)
        # with ThreadPoolExecutor(max_workers=self.n_thread) as executor:
        #     futures = {executor.submit(self.query_one, text, stop, temperature, model_id): i for i, text in enumerate(texts)}
        #     for future in tqdm(as_completed(futures), total=len(texts), desc="Querying"):
        #         i = futures[future]
        #         results[i] = future.result()
        # -- v2
        with ThreadPoolExecutor(max_workers=self.n_thread) as executor:
            results = list(tqdm(executor.map(lambda x: self.query_one(x, stop, temperature, model_id), texts), total=len(texts), desc="Querying"))
        return results

