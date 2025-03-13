import json
import re
import traceback
import concurrent.futures
from tqdm import tqdm
from prompt import *
from schema import *
from LLM import *
from generated_tools import *


def extract_court_code(text):
    # 案号的正则表达式
    case_number_pattern = re.compile(r"[(（](\d{4})[)）]([^\d]+?\d+)\D+\d+号")

    match = case_number_pattern.search(text)

    if match:
        court_code = match.group(2)
        return court_code
    else:
        return None

def remove_commas_from_numbers(text):
    number_with_commas_pattern = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)")

    def replace_commas(match):
        return match.group(0).replace(",", "")

    cleaned_text = re.sub(number_with_commas_pattern, replace_commas, text)

    return cleaned_text

def get_province_by_sub(sub_province):
    provices = [
        "北京市",
        "天津市",
        "上海市",
        "重庆市",
        "河北省",
        "山西省",
        "辽宁省",
        "吉林省",
        "黑龙江省",
        "江苏省",
        "浙江省",
        "安徽省",
        "福建省",
        "江西省",
        "山东省",
        "河南省",
        "湖北省",
        "湖南省",
        "广东省",
        "海南省",
        "四川省",
        "贵州省",
        "云南省",
        "陕西省",
        "甘肃省",
        "青海省",
        "台湾省",
        "内蒙古自治区",
        "广西壮族自治区",
        "西藏自治区",
        "宁夏回族自治区",
        "新疆维吾尔自治区",
        "香港特别行政区",
        "澳门特别行政区",
    ]
    for p in provices:
        if p.find(sub_province) != -1:
            return p
    return sub_province

def get_city_by_sub(sub_city):
    if sub_city != "" and sub_city[-1] == "市":
        return sub_city
    citys = [
        "北京市",
        "天津市",
        "上海市",
        "重庆市",
        "阿坝藏族羌族自治州",
        "阿克苏地区",
        "阿拉善盟",
        "阿勒泰地区",
        "阿里地区",
        "安康市",
        "安庆市",
        "安顺市",
        "安阳市",
        "鞍山市",
        "巴彦淖尔市",
        "巴音郭楞蒙古自治州",
        "巴中市",
        "白城市",
        "白山市",
        "白银市",
        "百色市",
        "蚌埠市",
        "包头市",
        "宝鸡市",
        "保定市",
        "保山市",
        "北海市",
        "本溪市",
        "毕节地区",
        "滨州市",
        "博尔塔拉蒙古自治州",
        "沧州市",
        "昌都地区",
        "昌吉回族自治州",
        "长春市",
        "长沙市",
        "长治市",
        "常德市",
        "常州市",
        "巢湖市",
        "朝阳市",
        "潮州市",
        "郴州市",
        "成都市",
        "承德市",
        "池州市",
        "赤峰市",
        "崇左市",
        "滁州市",
        "楚雄彝族自治州",
        "达州市",
        "大理白族自治州",
        "大连市",
        "大庆市",
        "大同市",
        "大兴安岭地区",
        "丹东市",
        "德宏傣族景颇族自治州",
        "德阳市",
        "德州市",
        "迪庆藏族自治州",
        "定西市",
        "东莞市",
        "东营市",
        "鄂尔多斯市",
        "鄂州市",
        "恩施土家族苗族自治州",
        "防城港市",
        "佛山市",
        "福州市",
        "抚顺市",
        "抚州市",
        "阜新市",
        "阜阳市",
        "甘南州",
        "甘孜藏族自治州",
        "赣州市",
        "固原市",
        "广安市",
        "广元市",
        "广州市",
        "贵港市",
        "贵阳市",
        "桂林市",
        "果洛藏族自治州",
        "哈尔滨市",
        "哈密地区",
        "海北藏族自治州",
        "海东地区",
        "海口市",
        "海南藏族自治州",
        "海西蒙古族藏族自治州",
        "邯郸市",
        "汉中市",
        "杭州市",
        "毫州市",
        "合肥市",
        "和田地区",
        "河池市",
        "河源市",
        "菏泽市",
        "贺州市",
        "鹤壁市",
        "鹤岗市",
        "黑河市",
        "衡水市",
        "衡阳市",
        "红河哈尼族彝族自治州",
        "呼和浩特市",
        "呼伦贝尔市",
        "湖州市",
        "葫芦岛市",
        "怀化市",
        "淮安市",
        "淮北市",
        "淮南市",
        "黄冈市",
        "黄南藏族自治州",
        "黄山市",
        "黄石市",
        "惠州市",
        "鸡西市",
        "吉安市",
        "吉林市",
        "济南市",
        "济宁市",
        "佳木斯市",
        "嘉兴市",
        "嘉峪关市",
        "江门市",
        "焦作市",
        "揭阳市",
        "金昌市",
        "金华市",
        "锦州市",
        "晋城市",
        "晋中市",
        "荆门市",
        "荆州市",
        "景德镇市",
        "九江市",
        "酒泉市",
        "喀什地区",
        "开封市",
        "克拉玛依市",
        "克孜勒苏柯尔克孜自治州",
        "昆明市",
        "拉萨市",
        "来宾市",
        "莱芜市",
        "兰州市",
        "廊坊市",
        "乐山市",
        "丽江市",
        "丽水市",
        "连云港市",
        "凉山彝族自治州",
        "辽阳市",
        "辽源市",
        "聊城市",
        "林芝地区",
        "临沧市",
        "临汾市",
        "临夏州",
        "临沂市",
        "柳州市",
        "六安市",
        "六盘水市",
        "龙岩市",
        "陇南市",
        "娄底市",
        "泸州市",
        "吕梁市",
        "洛阳市",
        "漯河市",
        "马鞍山市",
        "茂名市",
        "眉山市",
        "梅州市",
        "绵阳市",
        "牡丹江市",
        "内江市",
        "那曲地区",
        "南昌市",
        "南充市",
        "南京市",
        "南宁市",
        "南平市",
        "南通市",
        "南阳市",
        "宁波市",
        "宁德市",
        "怒江傈僳族自治州",
        "攀枝花市",
        "盘锦市",
        "平顶山市",
        "平凉市",
        "萍乡市",
        "莆田市",
        "濮阳市",
        "普洱市",
        "七台河市",
        "齐齐哈尔市",
        "黔东南苗族侗族自治州",
        "黔南布依族苗族自治州",
        "黔西南布依族苗族自治州",
        "钦州市",
        "秦皇岛市",
        "青岛市",
        "清远市",
        "庆阳市",
        "曲靖市",
        "衢州市",
        "泉州市",
        "日喀则地区",
        "日照市",
        "三门峡市",
        "三明市",
        "三亚市",
        "山南地区",
        "汕头市",
        "汕尾市",
        "商洛市",
        "商丘市",
        "上饶市",
        "韶关市",
        "邵阳市",
        "绍兴市",
        "深圳市",
        "沈阳市",
        "十堰市",
        "石家庄市",
        "石嘴山市",
        "双鸭山市",
        "朔州市",
        "四平市",
        "松原市",
        "苏州市",
        "宿迁市",
        "宿州市",
        "绥化市",
        "随州市",
        "遂宁市",
        "塔城地区",
        "台州市",
        "太原市",
        "泰安市",
        "泰州市",
        "唐山市",
        "天水市",
        "铁岭市",
        "通化市",
        "通辽市",
        "铜川市",
        "铜陵市",
        "铜仁市",
        "吐鲁番地区",
        "威海市",
        "潍坊市",
        "渭南市",
        "温州市",
        "文山壮族苗族自治州",
        "乌海市",
        "乌兰察布市",
        "乌鲁木齐市",
        "无锡市",
        "吴忠市",
        "芜湖市",
        "梧州市",
        "武汉市",
        "武威市",
        "西安市",
        "西宁市",
        "西双版纳傣族自治州",
        "锡林郭勒盟",
        "厦门市",
        "咸宁市",
        "咸阳市",
        "湘潭市",
        "湘西土家族苗族自治州",
        "襄樊市",
        "孝感市",
        "忻州市",
        "新乡市",
        "新余市",
        "信阳市",
        "兴安盟",
        "邢台市",
        "徐州市",
        "许昌市",
        "宣城市",
        "雅安市",
        "烟台市",
        "延安市",
        "延边朝鲜族自治州",
        "盐城市",
        "扬州市",
        "阳江市",
        "阳泉市",
        "伊春市",
        "伊犁哈萨克自治州",
        "宜宾市",
        "宜昌市",
        "宜春市",
        "益阳市",
        "银川市",
        "鹰潭市",
        "营口市",
        "永州市",
        "榆林市",
        "玉林市",
        "玉树藏族自治州",
        "玉溪市",
        "岳阳市",
        "云浮市",
        "运城市",
        "枣庄市",
        "湛江市",
        "张家界市",
        "张家口市",
        "张掖市",
        "漳州市",
        "昭通市",
        "肇庆市",
        "镇江市",
        "郑州市",
        "中山市",
        "中卫市",
        "舟山市",
        "周口市",
        "株洲市",
        "珠海市",
        "驻马店市",
        "资阳市",
        "淄博市",
        "自贡市",
        "遵义市",
    ]
    for c in citys:
        if c.find(sub_city) != -1:
            return c
    return sub_city

def check_code(code):
    '''
    对代码进行规则化处理
    '''
    new_code = code
    pattern = r"(\w+)\((.*?)\)"
    # 使用 re.findall 提取所有函数名和参数
    matches = re.findall(pattern, code)

    # 输出所有匹配到的函数名和参数
    for i, (func_name, args) in enumerate(matches):
        if is_tool_name(func_name):
            print(f"函数调用 {i}:")
            print(f"函数名: {func_name}")
            print(f"参数: {args}")
            args_pattern = r"'(.*?)', (\[.*?\])"
            match = re.search(args_pattern, args)
            if match:
                identifier = match.group(1).strip('').replace('(', '（').replace(')', '）')
                columns = eval(match.group(2))
                func_name, new_args = correct_args(func_name, {
                    'identifier': identifier,
                    'columns':  columns
                })
                new_code = new_code.replace(args, f"'{new_args['identifier']}', {new_args['columns']}")
    return new_code

def correct_args(api_name, api_args):
    '''
    对工具调用的参数进行规则矫正
    '''
    #api_args: {'identifier': '北京碧水源科技股份有限公司', 'columns': ['上市公司关系', '上市公司投资金额', '公司名称']}
    print(f"矫正前参数：{api_name}: {api_args}")

    try:
        if api_name == "get_company_register_name":
            # 真正使用这个 统一社会信用代码
            pass
        elif 'identifier' in api_args.keys() and isinstance(api_args['identifier'], str):
            sub_name = api_args['identifier'].strip('公司')
            try: 
                name = post_request("get_company_info", {'identifier': sub_name,'columns': ['公司名称']})['公司名称']
                if name.find('公司') != -1:
                    api_args['identifier'] = name
            except:
                pass
            try:
                name = post_request("get_company_register_name", {'identifier': sub_name,'columns': ['公司名称']})
                if name.find('公司') != -1:
                    api_args['identifier'] = name
            except:
                traceback.print_exc()
                pass

        if isinstance(api_args["columns"], dict):
            api_args["columns"] = list(api_args["columns"].values())[0]
        if isinstance(api_args["columns"], list) == False or (len(api_args['columns']) > 0 and api_args["columns"][0] == "*"):
            api_args["columns"] = []

        if "上市公司投资金额" in api_args["columns"] and "上市公司参股比例" not in api_args["columns"]:
            api_args["columns"].append("上市公司参股比例")

        temp = []
        # 将api_args['columns']所有 '级别' 替换为 ["法院级别", "行政级别", "级别"]，其他保留
        for arg in api_args["columns"]:
            if arg.find("级别") != -1:
                for i in ["法院级别", "行政级别", "级别"]:
                    if i not in temp:
                        temp.append(i)
            else:
                temp.append(arg)
        api_args["columns"] = temp

        temp = api_args["columns"]
        # 若api_args['columns']中有 '律师事务所', 则添加 ['原告', '被告']，其他保留
        if (
            "原告律师事务所" in api_args["columns"]
            or "被告律师事务所" in api_args["columns"]
            or "原告" in api_args["columns"]
            or "被告" in api_args["columns"]
        ):
            api_args["columns"].append("原告")
            api_args["columns"].append("原告律师事务所")
            api_args["columns"].append("被告")
            api_args["columns"].append("被告律师事务所")
            api_args["columns"] = list(set(api_args["columns"]))

        if api_name == "get_legal_document_list":  # 添加案号，方便后续筛选
            api_args["columns"].append("案号")
            api_args["columns"] = list(set(api_args["columns"]))
        if api_name == "get_company_info": # 添加公司名称
            api_args["columns"].append("公司名称")
            api_args["columns"] = list(set(api_args["columns"]))
        if api_name == "get_sub_company_info":
            api_args["columns"].append("关联上市公司全称")
            api_args["columns"] = list(set(api_args["columns"]))
        if api_name == "get_zb_info_list":
            api_args["columns"].append("执行标的（元）")
            api_args["columns"] = list(set(api_args["columns"]))
        if api_name == "get_sub_company_info_list": # 根据母公司查询子公司，但实际输入的公司可能还不是母公司
            try: 
                name = post_request("get_sub_company_info", api_args)['关联上市公司全称'] # 直接查出母公司
                if name.find('公司') != -1:
                    api_args['identifier'] = name
            except:
                pass

        # 矫正一下省份格式
        if 'prov' in api_args.keys():
            api_args["prov"] = get_province_by_sub(api_args["prov"])
        if 'city' in api_args.keys():
            api_args["city"] = get_city_by_sub(api_args["city"])
        if 'county' in api_args.keys():
            if isinstance(api_args["county"], str) and len(api_args["county"]) > 0:
                if not (api_args["county"][-1] == '区' or api_args["county"][-1] == '市' or  api_args["county"][-1] == '旗'):
                    api_args["county"] += '区'

        # 省份在，则城市一定在，如果省份在，城市不在，则试图根据直辖市填充
        if "prov" in api_args.keys() and "city" not in api_args.keys():
            if api_args['prov'] in ["北京市", "天津市", "上海市", "重庆市"]:
                api_args["city"] = api_args["prov"]

        # 城市在，则省份一定在，如果城市在，省份不在，则试图根据直辖市填充
        if "prov" in api_args.keys() and "city" not in api_args.keys():
            if api_args["city"] in ["北京市", "天津市", "上海市", "重庆市"]:
                api_args["prov"] = api_args["city"]

        api_args["columns"] = list(set(api_args["columns"]))

        if len(api_args["columns"]) >= 5:
            api_args["columns"] = []
    except:
        traceback.print_exc()
        pass

    print(f"矫正后参数：{api_name}: {api_args}")
    return api_name, api_args

def multi_thread_excute(all_tasks, parralle_num=20):
    """
    多线程运行任务，注意，返回结果序并不和all_tasks一致，请设计好task的输出，能够通过map的形式找到对应的答案
    """

    def multi_thread_excute_helper(tasks):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            exe_tasks = [executor.submit(*task) for task in tasks]
            results = [future.result() for future in concurrent.futures.as_completed(exe_tasks)]
        return results

    all_results = []
    for i in tqdm(range(0, len(all_tasks), parralle_num)):
        all_results += multi_thread_excute_helper(all_tasks[i : i + parralle_num])
    return all_results

def parse_action(rsp: str):
    '''
    解析 json 形式的 action
    '''
    # json_pattern = r'\[.*?\{.*?\}.*?\]'
    json_pattern = r"```json(.*?)```"
    rsp_json = None
    matches = re.findall(json_pattern, rsp, re.DOTALL)
    if len(matches) != 0:
        for match in matches:
            try:
                # 加载外层的 JSON 列表
                # print(match)
                match = match.replace('\'', '\"').replace('(', '（').replace(')', '）')     
                rsp_json = json.loads(match)    
                if isinstance(rsp_json['action_input'], dict):
                    if rsp_json['action'] == 'get_rank' or rsp_json['action'] == 'get_sum' or rsp_json['action'] == 'get_subtract' or \
                        rsp_json['action'] == 'get_multiply' or rsp_json['action'] == 'get_divide':
                        return rsp_json['action'], rsp_json['action_input']
                    if 'columns' in rsp_json['action_input'].keys():
                        if len(rsp_json['action_input']['columns']) > 5:
                            rsp_json['action_input']['columns'] = []
                    elif 'identifier' in rsp_json['action_input'].keys() or 'prov' in rsp_json['action_input'].keys():
                        rsp_json['action_input']['columns'] = []
                return rsp_json['action'], rsp_json['action_input']
            except Exception as e:
                return "", ""
    else:
        # 尝试匹配 xxx```pythontool_call(identifier='xxx', columns=[])```
        try :
            action, tool_call, tail = rsp.split("```")
            prefix = "pythontool_call("
            suffix = ")"
            if tool_call.startswith(prefix) and tool_call.endswith(suffix):
                tool_call = tool_call[len(prefix):-len(suffix)]
            tool_call_dict = eval(f"dict({tool_call})")  # 使用 eval 将字符串字典化
            return action, tool_call_dict
        except Exception as e:
            return "", ""
        
def post_request(name, input):
    print("调用工具中...", name, input)
    return call_(name, input)

from termcolor import colored

def print_colored(text, color=None):
    """
    打印彩色字符串。

    参数：
    - text: 要打印的文本
    - color: 文本颜色（如 red, green, blue, yellow, cyan, magenta, white）
    - on_color: 背景颜色（如 on_red, on_green, on_blue）
    - attrs: 属性列表（如 ['bold', 'dark', 'underline', 'blink', 'reverse', 'concealed']）
    """
    try:
        print('\n\n\n')
        print(colored(text, color=color))
        print('\n\n\n')
    except Exception as e:
        print(f"错误：{e}")

def filter_table_and_tool(query, model_name):
    '''
    信息过滤
    '''
    for _ in range(3):
        try:
            table_prompt = TABLE_PROMPT.format(question=query, database_schema=database_schema)
            table_answer = LLM(table_prompt, model_name)
            table_response = prase_json_from_response(table_answer)
            table = table_response["名称"]
            break
        except:
            table = [
                "CompanyInfo",
                "CompanyRegister",
                "SubCompanyInfo",
                "LegalDoc",
                "CourtInfo",
                "CourtCode",
                "LawfirmInfo",
                "LawfirmLog",
                "AddrInfo",
                "LegalAbstract",
                "RestrictionCase",
                "FinalizedCase",
                "DishonestyCase",
                "AdministrativeCase"
            ]
    print(f"用到的table: {table}")
    if "CompanyInfo" not in table:
        table.append("CompanyInfo")
    if "AddrInfo" not in table:
        table.append("AddrInfo")
    tool_prompt = ""
    table_used_prompt = ""
    used_tools = []
    for i in table:
        emun = table_map[i]
        one_prompt = f"""
{i}表格有下列字段:
{build_enum_list(emun)}
-------------------------------------
"""
        table_used_prompt += one_prompt + "\n"
        used_tools.extend(Tools_map[i])
        tool_prompt += str(Tools_prompt[i]) + "\n"

    return used_tools, table_used_prompt

def extract_units(question: str):
    """
    提取问题中的所有可能单位
    """
    fixed_units = {"起", "次", "个", "件", "家"}  # 预定义单位列表
    units_found = set()
    
    for char in reversed(question):  # 从后往前找
        if char in fixed_units:
            units_found.add(char)
    
    return units_found if units_found else None  # 返回所有找到的单位

def process_question_answer(question: str, answer: str):
    """
    处理问题和答案，使单位保持一致，并附加所有可能正确的单位
    """
    units = extract_units(question)
    if not units:
        return answer  # 如果未找到单位，则不修改答案
    
    # 查找所有数字+单位的匹配项
    matches = re.findall(r'(\d+)\s*([起次个件家])', answer)
    
    # 替换所有匹配项并附加所有可能的单位
    for number, answer_unit in matches:
        additional_units = units - {answer_unit}  # 过滤掉已经存在的单位
        for unit in additional_units:
            answer += f'（即 {number}{unit}）'  # 附加所有可能的单位表达
    
    return answer

# model = "glm-4"

# datas = open(f'./output_0310/goalact_0310_{model}.json', 'r').readlines()
# ground_truth = json.load(open('./dataset_1202.json', 'r'))
# output_f = open(f'./output_0311/goalact_0311_{model}.json', 'w')

# for data in datas:
#     data = json.loads(data)
#     id = data['id']
#     res = data['res']
#     summary = data['summary']

#     question = ground_truth[int(id) - 1]['new_question']

#     res = process_question_answer(question, res)
#     summary = process_question_answer(question, summary)

#     output_f.write(json.dumps({
#         "id": id,
#         "res": res,
#         "summary": summary
#     }, ensure_ascii=False) + '\n')

