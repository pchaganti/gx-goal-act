import json
import argparse
import os
from act import *
import traceback
from utils import *
from prompt import *
from memory import *
import concurrent.futures as cf

def run_single(data, model_name):
    try:
        query = data['new_question']
        print(query)
        print("改写问题...")
        '''
        对问题进行预处理
        '''
        ### 改写问题
        for _ in range(3):
            try:
                query_rewrite_prompt = QUESATION_REWRITE.format(question=query)
                query_rewrite_answer = LLM(query_rewrite_prompt, model_name)
                query_rewrite_response = prase_json_from_response(query_rewrite_answer)
                new_question = query_rewrite_response["重写问题"]
                break
            except:
                new_question = query
        new_question = f"用户原始查询：{query}\n以下是为了辅助你理解的改写问题（当改写内容与原内容冲突时，请依照原内容）：\n{new_question}"
        print(new_question)
        ### 信息过滤
        used_tools, table_used_prompt = filter_table_and_tool(new_question, model_name)
        tools = "\n\n".join([f"{tool.name} {tool.description}" for tool in used_tools])
        tool_names = " ".join([f"{tool.name}" for tool in used_tools])

        ### memory
        print("加载记忆...")
        for _ in range(3):
            try:
                Memory_prompt = MEMORY_PROMPT.format(question=new_question, query_list=query_list)
                Memory_answer = LLM(Memory_prompt, model_name)
                Memory_response = prase_json_from_response(Memory_answer)
                Memory_list = Memory_response["相关问题"]
                memory = get_memory(Memory_list)
                break
            except:
                Memory_list = [1, 2, 3]
                memory = get_memory(Memory_list) # 只用来辅助生成全局规划
        print(Memory_list)
        
        scratchpad = run(model_name=model_name, 
                        question=new_question, 
                        tools=tools, 
                        tool_names=tool_names, 
                        table_used_prompt=table_used_prompt, 
                        memory=memory)

        '''
        对答案进行后处理
        '''
        f_answer = LLM(FILTER_PROMPT.format(query=query, info=scratchpad), model_name)
        summary_answer = LLM(SUMMARY_PROMPT.format(query=query, info=scratchpad), model_name)
        
        f_answer = re.sub(r'(?<=\d),(?=\d)', '', f_answer)
        summary_answer = re.sub(r'(?<=\d),(?=\d)', '', summary_answer)

        f_answer = f_answer.replace("《", "").replace("》", "")
        summary_answer = summary_answer.replace("《", "").replace("》", "")

        f_answer = process_question_answer(query, f_answer)
        summary_answer = process_question_answer(query, summary_answer)

        print(f"final_anwer is {f_answer}")
        print(f"summary_answer is {summary_answer}")

        return {
            "id": data['id'],
            "res": f_answer,
            "summary": summary_answer,
            "scratchpad": scratchpad
        }
    except Exception as e:
        traceback.print_exc()
        output.write(json.dumps({
            "id": data['id'],
            "res": "silence",
            "summary": "silence"
        }, ensure_ascii=False) + '\n')
        output.flush()
        return {
            "id": data['id'],
            "res": "silence",
            "summary": "silence",
            "scratchpad": ""
        }

def run_with_cache(data, model_name, date):
    """ 运行任务，先检查缓存是否已存在，避免重复计算 """
    cache_dir = f"./temp_{date}/{model_name}"
    os.makedirs(f'./temp_{date}/{model_name}', exist_ok=True)
    file_path = os.path.join(cache_dir, f"{data['id']}.json")
    print(file_path)
    # 检查缓存是否存在
    if os.path.exists(file_path):
        print("已存在")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # 运行计算任务
    result = run_single(data, model_name)
    
    # 存储结果到缓存
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    return result

if __name__ == "__main__":
    datas = json.load(open('./dataset_1202.json', 'r'))[:10]
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--model', type=str, required=True, help='实验基座模型')
    parser.add_argument('--date', type=str, required=True, help='实验日期，用于区别输出路径，如output_date')
    parser.add_argument('--multi', action='store_true', help='是否开启并行')
    args = parser.parse_args()
    model_name = args.model
    date = args.date
    multi = args.multi
    os.makedirs(f"./output_{date}", exist_ok=True)
    output = open(f'./output_{date}/goalact_{date}_{model_name}.json', 'a') 
    log_txt = open(f'./output_{date}/log_goalact_{date}_{model_name}.txt', 'a')
    os.makedirs(f"./token_{date}", exist_ok=True)

    if multi:
        result_json_list = []
        with cf.ProcessPoolExecutor(max_workers=5) as executor:
            future_list = [executor.submit(run_with_cache, data, model_name, date) for data in datas]
            for future in tqdm(cf.as_completed(future_list), total=len(future_list), desc="Processing", ncols=100):
                result_json_list.append(future.result())
        result_json_list.sort(key=lambda x: x["id"])
        for result in result_json_list:
            output.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    if not multi:
        for idx, data in enumerate(datas):
            try:
                query = data['new_question']
                print(query)
                print("改写问题...")
                '''
                对问题进行预处理
                '''
                ### 改写问题
                for _ in range(3):
                    try:
                        query_rewrite_prompt = QUESATION_REWRITE.format(question=query)
                        query_rewrite_answer = LLM(query_rewrite_prompt, model_name)
                        query_rewrite_response = prase_json_from_response(query_rewrite_answer)
                        new_question = query_rewrite_response["重写问题"]
                        break
                    except:
                        new_question = query
                new_question = f"用户原始查询：{query}\n以下是为了辅助你理解的改写问题（当改写内容与原内容冲突时，请依照原内容）：\n{new_question}"
                print(new_question)
                ### 信息过滤
                used_tools, table_used_prompt = filter_table_and_tool(new_question, model_name)
                tools = "\n\n".join([f"{tool.name} {tool.description}" for tool in used_tools])
                tool_names = " ".join([f"{tool.name}" for tool in used_tools])

                ### memory
                print("加载记忆...")
                for _ in range(3):
                    try:
                        Memory_prompt = MEMORY_PROMPT.format(question=new_question, query_list=query_list)
                        Memory_answer = LLM(Memory_prompt, model_name)
                        Memory_response = prase_json_from_response(Memory_answer)
                        Memory_list = Memory_response["相关问题"]
                        memory = get_memory(Memory_list)
                        break
                    except:
                        Memory_list = [1, 2, 3]
                        memory = get_memory(Memory_list) # 只用来辅助生成全局规划
                print(Memory_list)
                
                scratchpad = run(model_name=model_name, 
                                question=new_question, 
                                tools=tools, 
                                tool_names=tool_names, 
                                table_used_prompt=table_used_prompt, 
                                memory=memory)

                '''
                对答案进行后处理
                '''
                f_answer = LLM(FILTER_PROMPT.format(query=query, info=scratchpad), model_name)
                summary_answer = LLM(SUMMARY_PROMPT.format(query=query, info=scratchpad), model_name)
                
                f_answer = re.sub(r'(?<=\d),(?=\d)', '', f_answer)
                summary_answer = re.sub(r'(?<=\d),(?=\d)', '', summary_answer)

                f_answer = f_answer.replace("《", "").replace("》", "")
                summary_answer = summary_answer.replace("《", "").replace("》", "")

                f_answer = process_question_answer(query, f_answer)
                summary_answer = process_question_answer(query, summary_answer)

                print(f"final_anwer is {f_answer}")
                print(f"summary_answer is {summary_answer}")

                log_txt.write(scratchpad)
                log_txt.write('\n')
                log_txt.write(f"final_anwer is {f_answer}")
                log_txt.write('\n')
                log_txt.write(f"summary_answer is {summary_answer}")
                log_txt.write('\n\n\n')
                log_txt.flush()

                output.write(json.dumps({
                    "id": data['id'],
                    "res": f_answer,
                    "summary": summary_answer
                }, ensure_ascii=False) + '\n')
                output.flush()
            except Exception as e:
                traceback.print_exc()
                output.write(json.dumps({
                    "id": data['id'],
                    "res": "silence",
                    "summary": "silence"
                }, ensure_ascii=False) + '\n')
                output.flush()
