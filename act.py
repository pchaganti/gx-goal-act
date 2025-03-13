from LLM import *
from utils import *
from action import Retrive, Code, Write

def run(
    model_name,
    question,
    tools,
    tool_names,
    table_used_prompt,
    memory,
): 
    '''
    核心执行模块，在此进行规划和行动
    '''
    step = 0
    scratchpad = "" # 以 ”思考、行动、观察“ 记录答案
    Max_step = 10
    max_retries = 3
    action_list = [] # 避免 action 重复

    try:
        Court_code = extract_court_code(question)
        if Court_code != None:
            court_name = post_request("get_court_code", {'identifier': Court_code,'columns': ['法院名称']})['法院名称']
            scratchpad += f"题目中有法院代字是{Court_code}，对应的法院名称为{court_name}。\n"
    except:
        pass

    while True:
        step += 1
        print(f"现在的步数：{step}")
        if step > Max_step:
            return scratchpad

        # 生成全局规划 + 行动
        for _ in range(max_retries):
            try:
                prompt = Action_Thought_prompt.format(
                    question=question,
                    table_used_prompt=table_used_prompt,
                    memory=memory,
                    scratchpad=scratchpad,
                    tool_prompt=tools,
                )
                decompose_answer = LLM(prompt, model_name)
                decompose_response = prase_json_from_response(decompose_answer)
                break
            except Exception as e:
                decompose_response = [{"思考": "分解行为错误，请思考表述重新尝试", "行动": "重新分解"}]
        
        print_colored(f"现在的规划：{decompose_response}", color='red')
        try:
            thought = decompose_response[0]["思考"]
            action = decompose_response[0]["行动"]
        except Exception as e:
            thought = "思考错误"
            action = "行为错误"
        
        if action == "结束":
            return scratchpad

        if action not in action_list:
            action_list.append(action)
        else:
            print("去重/纠正行为！")
            try:
                action_prompt = Action_refine_prompt.format(
                    question=question,
                    table_used_prompt=table_used_prompt,
                    wrong_action=action,
                    scratchpad=scratchpad,
                    tool_prompt=tools,
                )
                Action_refine_answer = LLM(action_prompt, model_name)
                Action_decompose_response = prase_json_from_response(Action_refine_answer)
                thought = Action_decompose_response[0]["思考"]
                action = Action_decompose_response[0]["行动"]
                action_list.append(action)
            except:
                pass

        print_colored(f"现在要做的事：{thought}: {action}", color='blue')
        try:
            action_one = action.split("[")[0]
        except:
            action_one = action[:3]
        
        '''
        增加解析行动的鲁棒性
        '''
        if action_one != "查询" and action_one != "编程" and action_one != "写作" and action_one != "结束":
            if action.find("查询") != -1:
                action_one = "查询"
            elif action.find("编程") != -1:
                action_one = "编程"
            elif action.find("写作") != -1:
                action_one = "写作"
            elif action.find("结束") != -1:
                action_one = "结束"
            else:
                action_one = "查询"

        try:
            Court_code = extract_court_code(thought + action)
            if Court_code != None:
                court_name = post_request("get_court_code", {'identifier': Court_code,'columns': ['法院名称']})['法院名称']
                scratchpad += f"发现有法院代字{Court_code}，该法院代字对应的法院名称为{court_name}。\n"
        except:
            pass
        
        if action_one == "查询":
            tc = thought + action
            if (tc).find('统计') != -1:
                print("修改为编程")
                action_one = "编程"

            if (tc).find('筛选') != -1:
                print("修改为编程")
                action_one = "编程"
            
            if (tc).find("求和") != -1 or (tc).find("总和") != -1 or (tc).find("总额") != -1 or (tc).find("总金额") != -1:
                print("修改为编程")
                action_one = "编程"

            if ((tc).find("排序") != -1 or (tc).find("最高") != -1 or (tc).find("最低") != -1 or (tc).find("第二高") != -1):
                print("修改为编程")
                action_one = "编程"

            if (tc).find('list') != -1:
                # 输出结果可能很长，非简单查询
                action_one = "编程"

        print_colored(f"现在的action_one：{action_one}", color='green')

        # 简单查询
        if action_one == "查询":
            result = Retrive(scratchpad, tool_names, tools, table_used_prompt, thought + action, model_name)
            scratchpad += f"思考{step}: {thought}\n行动{step}: {action}\n观察{step}: {result}\n"
        # 编程
        elif action_one == "编程":
            result = Code(scratchpad, tool_names, tools, table_used_prompt, thought + action, model_name)
            scratchpad += f"思考{step}: {thought}\n行动{step}: {action}\n观察{step}: {result}\n"
        elif action_one == "写作":
            result = Write(question, scratchpad, thought + action, model_name)
            scratchpad += f"思考{step}: {thought}\n行动{step}: {action}\n观察{step}: {result}\n"
        elif action_one == "重新分解":
            scratchpad += f"思考{step}: {thought}\n行动{step}: {action}\n观察{step}: 行动分解失败，没有按照正确分解格式，请仔细思考重新分解规划！\n"
        elif action_one == "结束":
            return scratchpad
        else:
            scratchpad += f"思考{step}: {thought}\n行动{step}: {action}\n观察{step}: 行动分解错误，没有按照正确分解格式或行动不在四种规定的行动范围内！行动必须是查询、编程、写作、结束之一。\n"

        print_colored(f"scratchpad now: \n\n{scratchpad}", color='blue')