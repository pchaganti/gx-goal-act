from zhipuai import ZhipuAI
from prompt import *
import json
import re
from openai import OpenAI

qianwen_client = OpenAI(
    api_key="your_key",
    base_url="base_url"
)

openai_client = OpenAI(
            base_url="base_url", 
            api_key="your_key"
            )

def LLM(query, model_name):
    if isinstance(query, list):
        messages = query
    else:
        messages = [{"role": "user","content": query}]
    if model_name.find("gpt") != -1:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature = 0,
        )

    elif model_name.find('claude') != -1:
        response = claude_client.chat.completions.create(
                model=model_name, 
                messages=messages,
                temperature = 0,
            )
    
    elif model_name.find('qwen') != -1:
        response = qianwen_client.chat.completions.create(
            temperature = 0,
            model=model_name, # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages
        )
    
    elif model_name.find('glm') != -1:
        client = ZhipuAI(api_key='your_api')
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            temperature=0,
            do_sample=False,
        )

    ## 在这里记录 token 消耗数
    # 输入 token
    input_token = response.usage.prompt_tokens
    # 输出 token
    output_token = response.usage.completion_tokens
    # 总 token
    used_token = response.usage.total_tokens

    return response.choices[0].message.content.strip()

def prase_json_from_response(rsp: str):
    pattern = r"```json(.*?)```"
    rsp_json = None
    try:
        match = re.search(pattern, rsp, re.DOTALL)
        if match is not None:
            try:
                rsp_json = json.loads(match.group(1).strip())
            except:
                pass
        else:
            rsp_json = json.loads(rsp)
        return rsp_json
    except json.JSONDecodeError as e:  # 因为太长解析不了
        try:
            match = re.search(r"\{(.*?)\}", rsp, re.DOTALL)
            if match:
                content = "[{" + match.group(1) + "}]"
                return json.loads(content)
        except:
            pass
        print(rsp)
        raise ("Json Decode Error: {error}".format(error=e))
