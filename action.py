from LLM import *
from utils import *
import subprocess
from api import *

def parse_code(code):
    # ```python\n(.*?)```
    '''
    解析代码
    '''
    json_pattern = r"```python(.*?)```"
    matches = re.findall(json_pattern, code, re.DOTALL)
    if len(matches) != 0:
        for match in matches:
            return match
    else:
        return ""

import time
import random

def Code(history, tool_names, tools, table_used_prompt, action, model_name):
    messages = []
    action_prompt = CODE_CLASS.format(history=history, tool_names=tool_names, tools=tools, 
                                                        table_used_prompt=table_used_prompt, example=CODE_EXAMPLE, action=action)
    messages.append({"role": "user", "content": action_prompt})
    for _ in range(5):
        append_error = ""
        try: 
            code_action = parse_code(LLM(messages, model_name))
            code_action = check_code(code_action)
            print_colored(f"代码在这里：{code_action}", color="green")
            timestamp = time.strftime("%Y%m%d%H%M%S")  # 秒级时间戳
            random_part = str(random.randint(1000, 9999))  # 随机数
            unique_id = timestamp + random_part
            temp_filename = f'./temp_{unique_id}.py'
            temp_file = open(temp_filename, 'w')
            temp_file.write("from api import *\nimport sys\n")
            temp_file.write(code_action)
            messages.append({"role": "assistant", "content": code_action})
            temp_file.write("sys.stdout.flush()\n")
            with open(temp_filename, 'r', encoding='utf-8') as temp_file:
                result = subprocess.run(['python',temp_filename], capture_output=True, text=True)
            os.remove(temp_filename)
            if result.stderr != "" or result.stdout == "":
                print_colored(f"代码执行出错 STDERR：{result.stderr}", color="red")
                append_error = f"代码执行出错！原因可能是：一、调用的工具不合适，尝试使用其他工具；二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。\n运行代码的具体错误信息：{result.stderr}\n请你反思并尝试重新编程。"
            if result.stdout.find("No data found for the specified identifier.") != -1:
                append_error = f"代码执行出错！原因可能是：一、调用的工具不合适，尝试使用其他工具；二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。\n运行代码的具体错误信息：{result.stderr}\n请你反思并尝试重新编程。"
            print_colored(f"代码执行结果：{result.stdout}", color="green")
        except Exception as e:
            print_colored(f"代码执行出错 EXCE：{e}", color="red")
            append_error = f"代码执行出错！原因可能是：一、调用的工具不合适，尝试使用其他工具；二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。\n运行代码的具体错误信息：{e}\n请你反思并尝试重新编程。"
        if append_error == "":
            return result.stdout
        else:
            messages.append({"role": "user", "content": append_error})
    return "编程失败，请重新规划！"


def Write(query, history, action, model_name):
    '''
    搜集资料
    进行创作
    '''
    law_item = post_request("get_law_item", {'identifier': query})
    print_colored(law_item, color="green")
    law_case = post_request("get_law_case", {'identifier': query})
    law_knowledge = post_request("get_law_knowledge", {'identifier': query})

    action_prompt = WRITE_CLASS.format(item=law_item, case=law_case, knowledge=law_knowledge, history=history, action=action)
    res = LLM(action_prompt, model_name)
    return res

def Retrive(history, tool_names, tools, table_used_prompt, action, model_name):
    '''
    简单查询
    text + json
    '''
    input_action = action
    for _ in range(5):
        action_prompt = ACTION_CLASS.format(history=history, tool_names=tool_names, tools=tools, 
                                                    table_used_prompt=table_used_prompt, example=ACTION_EXAMPLE, action=input_action)
        action_s = LLM(action_prompt, model_name)
        action_type, action_input = parse_action(action_s)
        action_type, action_input = correct_args(action_type, action_input)
        if action_type == "":
            input_action += f"""查询一次只能调用一次工具，查询必须按照以下json格式输出，可以被Python json.loads函数解析：```json{{"action": $TOOL_NAME,"action_input": $INPUT}}```"""
        else:
            break
    print_colored(f"查询在这里：{action_type}：{action_input}", color="green")

    result = ""
    if action_type == "":
        result = f"查询失败，请重新规划！"

    else:
        try:
            result = post_request(action_type, action_input)
            if result == "No data found for the specified identifier.":
                result += '原因可能是：一、调用的工具不合适，尝试使用其他工具；二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。请你反思并尝试纠正。'
            elif result == "One or more specified columns do not exist.":
                result += '原因可能是：一、调用的工具不合适，尝试使用其他工具；二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。请你反思并尝试纠正。'
        except Exception as e:
            result = str(result) + '原因可能是：一、调用的工具不合适，尝试使用其他工具； 二、调用工具时传入的参数可能存在非法值，例如identifier的值非法（与工具的输入要求不符），或者columns列表中包含了要查询的表格中未出现的字段。请你反思并尝试纠正。'

    print_colored(result, color="yellow")
    return result
