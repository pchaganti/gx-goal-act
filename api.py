# %%
from dotenv import load_dotenv
# load_dotenv()  # 这会加载 .env 文件中的环境变量

# %%
import pandas as pd
from pandas import Timestamp
import pandas as pd
import numpy as np
nan = np.nan
import re
import os

# %%
cache_dir = "./cache/"
os.makedirs(cache_dir, exist_ok=True)

dataset_path = "./law_dataset_1202.xlsx"

def load_data_with_cache():
    cache_file = os.path.join(cache_dir, "data.pkl")
    if os.path.exists(cache_file):
        # print("从缓存加载数据...")
        return pd.read_pickle(cache_file)
    else:
        # print("加载数据中...")
        data = {
            "company_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='company_info'),
            "company_register": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='company_register'),
            "sub_company_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='sub_company_info'),
            "legal_document": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='legal_doc'),
            "court_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='court_info'),
            "court_code": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='court_code'),
            "lawfirm_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='lawfirm_info'),
            "lawfirm_log": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='lawfirm_log'),
            "address_info": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='addr_info'),
            "legal_abstract": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='legal_abstract'),
            "restriction_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='restriction_case'),
            "finalized_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='finalized_case'),
            "dishonesty_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='dishonesty_case'),
            "administrative_case": pd.read_excel(dataset_path, engine='openpyxl', sheet_name='administrative_case')
        }
        pd.to_pickle(data, cache_file)
        print("数据加载完成并已缓存")
        return data

# 加载数据
data = load_data_with_cache()
company_info = data["company_info"]
company_register = data['company_register']
sub_company_info = data['sub_company_info']
legal_document = data['legal_document']
court_info = data['court_info']
court_code = data['court_code']
lawfirm_info = data['lawfirm_info']
lawfirm_log = data['lawfirm_log']
address_info = data['address_info']
legal_abstract = data['legal_abstract']
restriction_case = data['restriction_case']
finalized_case = data['finalized_case']
dishonesty_case = data['dishonesty_case']
administrative_case = data['administrative_case']


# company_info = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='company_info')
# company_register = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='company_register')
# sub_company_info = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='sub_company_info')
# legal_document = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='legal_doc')
# court_info = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='court_info')
# court_code = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='court_code')
# lawfirm_info = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='lawfirm_info')
# lawfirm_log = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='lawfirm_log')
# address_info = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='addr_info')
# # address_code = pd.read_excel('副本B榜数据allnew.xlsx', engine='openpyxl', sheet_name='addr_code')
# # temp_info = pd.read_excel('副本B榜数据allnew.xlsx', engine='openpyxl', sheet_name='temp_info')
# legal_abstract = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='legal_abstract')
# restriction_case = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='restriction_case')
# finalized_case = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='finalized_case')
# dishonesty_case = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='dishonesty_case')
# administrative_case = pd.read_excel('law_dataset_v2.xlsx', engine='openpyxl', sheet_name='administrative_case')

# %%
def get_citizens_sue_citizens(input_data):
    """
    民事起诉状(公民提起民事诉讼用——公民起诉公民模板)\n\n
    民事起诉状
    原告：xxx，性别：男/女，出生日期：xxxx年xx月xx日，民族：x族，工作单位：......(写明工作单位和职务或职业)，地址：......，联系方式：......。
    原告委托诉讼代理人：xxx，联系方式：......。
    被告：xxx，性别：男/女，出生日期：xxxx年xx月xx日，民族：x族，工作单位：......(写明工作单位和职务或职业)，地址：......，联系方式：......。
    被告委托诉讼代理人：xxx，联系方式：......。
    诉讼请求：
    ......
    事实和理由：
    ......
    证据和证据来源，证人姓名和住所：
    ......
    此致
    xxxx人民法院
    附:本起诉状副本x份
    起诉人(签名)
    xxxx年xx月xx日
    """
    document_template = (
        "民事起诉状（公民起诉公民）\n"
        "原告：{plaintiff_name}，性别：{plaintiff_gender}，出生日期：{plaintiff_birthdate}，民族：{plaintiff_ethnicity}，工作单位：{plaintiff_work_unit}，地址：{plaintiff_address}，联系方式：{plaintiff_contact}。\n"
        "原告委托诉讼代理人：{plaintiff_lawyer}，联系方式：{plaintiff_lawyer_contact}。\n"
        "被告：{defendant_name}，性别：{defendant_gender}，出生日期：{defendant_birthdate}，民族：{defendant_ethnicity}，工作单位：{defendant_work_unit}，地址：{defendant_address}，联系方式：{defendant_contact}。\n"
        "被告委托诉讼代理人：{defendant_lawyer}，联系方式：{defendant_lawyer_contact}。\n"
        "诉讼请求：\n{lawsuit_demand}\n"
        "事实和理由：\n{facts_reasons}\n"
        "证据和证据来源，证人姓名和住所：\n{evidence}\n"
        "此致\n{court_name}\n\n"
        "附:本起诉状副本x份\n\n"
        "起诉人(签名)\n"
        "{sue_date}"
    )

    return document_template.format(
        plaintiff_name=input_data['原告'],
        plaintiff_gender=input_data['原告性别'],
        plaintiff_birthdate=input_data['原告生日'],
        plaintiff_ethnicity=input_data['原告民族'],
        plaintiff_work_unit=input_data['原告工作单位'],
        plaintiff_address=input_data['原告地址'],
        plaintiff_contact=input_data['原告联系方式'],
        plaintiff_lawyer=input_data['原告委托诉讼代理人'],
        plaintiff_lawyer_contact=input_data['原告委托诉讼代理人联系方式'],
        defendant_name=input_data['被告'],
        defendant_gender=input_data['被告性别'],
        defendant_birthdate=input_data['被告生日'],
        defendant_ethnicity=input_data['被告民族'],
        defendant_work_unit=input_data['被告工作单位'],
        defendant_address=input_data['被告地址'],
        defendant_contact=input_data['被告联系方式'],
        defendant_lawyer=input_data['被告委托诉讼代理人'],
        defendant_lawyer_contact=input_data['被告委托诉讼代理人联系方式'],
        lawsuit_demand=input_data['诉讼请求'],
        facts_reasons=input_data['事实和理由'],
        evidence=input_data['证据'],
        court_name=input_data['法院名称'],
        sue_date=input_data['起诉日期']
    )

def get_company_sue_citizens(input_data):
    """
    民事起诉状(公民提起民事诉讼用——公民起诉公民模板)\n\n
    民事起诉状
    原告：xxx，地址：......。
    法定代表人（负责人）：xxx，联系方式：......。
    原告委托诉讼代理人：xxx，联系方式：......。
    被告：xxx，性别：男/女，出生日期：xxxx年xx月xx日，民族：x族，工作单位：......(写明工作单位和职务或职业)，地址：......，联系方式：......。
    被告委托诉讼代理人：xxx，联系方式：......。
    诉讼请求：
    ......
    事实和理由：
    ......
    证据和证据来源，证人姓名和住所：
    ......
    此致
    xxxx人民法院
    附:本起诉状副本x份
    起诉人(签名)
    xxxx年xx月xx日
    """
    document_template = (
        "民事起诉状（公司起诉公民）\n"
        "原告：{plaintiff_name}，地址：{plaintiff_address}。"
        "法定代表人（负责人）：{plaintiff_boss}，联系方式：{plaintiff_contact}。\n"
        "原告委托诉讼代理人：{plaintiff_lawyer}，联系方式：{plaintiff_lawyer_contact}。\n"
        "被告：{defendant_name}，性别：{defendant_gender}，出生日期：{defendant_birthdate}，民族：{defendant_ethnicity}，工作单位：{defendant_work_unit}，地址：{defendant_address}，联系方式：{defendant_contact}。\n"
        "被告委托诉讼代理人：{defendant_lawyer}，联系方式：{defendant_lawyer_contact}。\n"
        "诉讼请求：\n{lawsuit_demand}\n"
        "事实和理由：\n{facts_reasons}\n"
        "证据和证据来源，证人姓名和住所：\n{evidence}\n"
        "此致\n{court_name}\n\n"
        "附:本起诉状副本x份\n\n"
        "起诉人(签名)\n"
        "{sue_date}"
    )

    return document_template.format(
        plaintiff_name=input_data['原告'],
        plaintiff_address=input_data['原告地址'],
        plaintiff_boss=input_data['原告法定代表人'],
        plaintiff_contact=input_data['原告联系方式'],
        plaintiff_lawyer=input_data['原告委托诉讼代理人'],
        plaintiff_lawyer_contact=input_data['原告委托诉讼代理人联系方式'],
        defendant_name=input_data['被告'],
        defendant_gender=input_data['被告性别'],
        defendant_birthdate=input_data['被告生日'],
        defendant_ethnicity=input_data['被告民族'],
        defendant_work_unit=input_data['被告工作单位'],
        defendant_address=input_data['被告地址'],
        defendant_contact=input_data['被告联系方式'],
        defendant_lawyer=input_data['被告委托诉讼代理人'],
        defendant_lawyer_contact=input_data['被告委托诉讼代理人联系方式'],
        lawsuit_demand=input_data['诉讼请求'],
        facts_reasons=input_data['事实和理由'],
        evidence=input_data['证据'],
        court_name=input_data['法院名称'],
        sue_date=input_data['起诉日期']
    )

def get_citizens_sue_company(input_data):
    """
    民事起诉状(公民提起民事诉讼用——公民起诉公民模板)\n\n
    民事起诉状
    原告：xxx，性别：男/女，出生日期：xxxx年xx月xx日，民族：x族，工作单位：......(写明工作单位和职务或职业)，地址：......，联系方式：......。
    原告委托诉讼代理人：xxx，联系方式：......。
    被告：xxx，地址：......。
    法定代表人（负责人）：xxx，联系方式：......。
    被告委托诉讼代理人：xxx，联系方式：......。
    诉讼请求：
    ......
    事实和理由：
    ......
    证据和证据来源，证人姓名和住所：
    ......
    此致
    xxxx人民法院
    附:本起诉状副本x份
    起诉人(签名)
    xxxx年xx月xx日
    """
    document_template = (
        "民事起诉状（公民起诉公司）\n"
        "原告：{plaintiff_name}，性别：{plaintiff_gender}，出生日期：{plaintiff_birthdate}，民族：{plaintiff_ethnicity}，工作单位：{plaintiff_work_unit}，地址：{plaintiff_address}，联系方式：{plaintiff_contact}。\n"
        "原告委托诉讼代理人：{plaintiff_lawyer}，联系方式：{plaintiff_lawyer_contact}。\n"
        "被告：{defendant_name}，地址：{defendant_address}。"
        "法定代表人（负责人）：{defendant_boss}，联系方式：{defendant_contact}。\n"
        "被告委托诉讼代理人：{defendant_lawyer}，联系方式：{defendant_lawyer_contact}。\n"
        "诉讼请求：\n{lawsuit_demand}\n"
        "事实和理由：\n{facts_reasons}\n"
        "证据和证据来源，证人姓名和住所：\n{evidence}\n"
        "此致\n{court_name}\n\n"
        "附:本起诉状副本x份\n\n"
        "起诉人(签名)\n"
        "{sue_date}"
    )

    return document_template.format(
        plaintiff_name=input_data['原告'],
        plaintiff_gender=input_data['原告性别'],
        plaintiff_birthdate=input_data['原告生日'],
        plaintiff_ethnicity=input_data['原告民族'],
        plaintiff_work_unit=input_data['原告工作单位'],
        plaintiff_address=input_data['原告地址'],
        plaintiff_contact=input_data['原告联系方式'],
        plaintiff_lawyer=input_data['原告委托诉讼代理人'],
        plaintiff_lawyer_contact=input_data['原告委托诉讼代理人联系方式'],
        defendant_name=input_data['被告'],
        defendant_address=input_data['被告地址'],
        defendant_boss=input_data['被告法定代表人'],
        defendant_contact=input_data['被告联系方式'],
        defendant_lawyer=input_data['被告委托诉讼代理人'],
        defendant_lawyer_contact=input_data['被告委托诉讼代理人联系方式'],
        lawsuit_demand=input_data['诉讼请求'],
        facts_reasons=input_data['事实和理由'],
        evidence=input_data['证据'],
        court_name=input_data['法院名称'],
        sue_date=input_data['起诉日期']
    )

def get_company_sue_company(input_data):
    """
    民事起诉状(公民提起民事诉讼用——公司起诉公司模板)\n\n
    民事起诉状
    原告：xxx，地址：......。
    法定代表人（负责人）：xxx，联系方式：......。
    原告委托诉讼代理人：xxx，联系方式：......。
    被告：xxx，地址：......。
    法定代表人（负责人）：xxx，联系方式：......。
    被告委托诉讼代理人：xxx，联系方式：......。
    诉讼请求：
    ......
    事实和理由：
    ......
    证据和证据来源，证人姓名和住所：
    ......
    此致
    xxxx人民法院
    附:本起诉状副本x份
    起诉人(签名)
    xxxx年xx月xx日
    """
    document_template = (
        "民事起诉状（公司起诉公司）\n"
        "原告：{plaintiff_name}，地址：{plaintiff_address}。"
        "法定代表人（负责人）：{plaintiff_boss}，联系方式：{plaintiff_contact}。\n"
        "原告委托诉讼代理人：{plaintiff_lawyer}，联系方式：{plaintiff_lawyer_contact}。\n"
        "被告：{defendant_name}，地址：{defendant_address}。"
        "法定代表人（负责人）：{defendant_boss}，联系方式：{defendant_contact}。\n"
        "被告委托诉讼代理人：{defendant_lawyer}，联系方式：{defendant_lawyer_contact}。\n"
        "诉讼请求：\n{lawsuit_demand}\n"
        "事实和理由：\n{facts_reasons}\n"
        "证据和证据来源，证人姓名和住所：\n{evidence}\n"
        "此致\n{court_name}\n\n"
        "附:本起诉状副本x份\n\n"
        "起诉人(签名)\n"
        "{sue_date}"
    )

    return document_template.format(
        plaintiff_name=input_data['原告'],
        plaintiff_address=input_data['原告地址'],
        plaintiff_boss=input_data['原告法定代表人'],
        plaintiff_contact=input_data['原告联系方式'],
        plaintiff_lawyer=input_data['原告委托诉讼代理人'],
        plaintiff_lawyer_contact=input_data['原告委托诉讼代理人联系方式'],
        defendant_name=input_data['被告'],
        defendant_address=input_data['被告地址'],
        defendant_boss=input_data['被告法定代表人'],
        defendant_contact=input_data['被告联系方式'],
        defendant_lawyer=input_data['被告委托诉讼代理人'],
        defendant_lawyer_contact=input_data['被告委托诉讼代理人联系方式'],
        lawsuit_demand=input_data['诉讼请求'],
        facts_reasons=input_data['事实和理由'],
        evidence=input_data['证据'],
        court_name=input_data['法院名称'],
        sue_date=input_data['起诉日期']
    )

# %%
def get_rank(identifier, is_desc=False):
    nums = identifier
    if not isinstance(nums, list) or len(nums) == 0:
        return "排序时发生错误，请检查参数格式！"
    
    if any(not isinstance(x, (int, float, str)) for x in nums):
        return "排序时发生错误，请检查参数格式！"
    
    def map_str_to_num(str_num):
        try:
            str_num = str_num.replace("千", "*1e3")
            str_num = str_num.replace("万", "*1e4")
            str_num = str_num.replace("亿", "*1e8")
            str_num = str_num.replace('年', '').replace('月', '').replace('日', '').replace('-', '')
            return eval(str_num)
        except Exception as e:
            pass
    
    # 统一成浮点数类型
    nums = [map_str_to_num(str(i)) for i in nums]

    try:
        return sorted(nums, reverse=is_desc)
    except Exception as e:
        pass
    return "排序时发生错误，请检查参数格式！"

from zhipuai import ZhipuAI
from langchain.vectorstores import FAISS
import faiss
client = ZhipuAI(api_key="2dc8291a45880410ee0796565841fd91.qjjMjdjdKoUK1Czp")
import traceback
import json

law_index = faiss.read_index('./index/law_item.bin')
case_index = faiss.read_index('./index/case.bin')
knowledge_index = faiss.read_index('./index/knowledge.bin')

law_corpus = open('./corpus/law_item.json', 'r').readlines()
case_corpus = open('./corpus/case.json', 'r').readlines()
knowledge_corpus = open('./corpus/knowledge.json', 'r').readlines()

def get_law_case(identifier, k=1):
    try: 
        query_response = client.embeddings.create(
            model="embedding-3", input=[identifier]
        )
        query_vector = np.array(query_response.data[0].embedding)
        distances, indices = case_index.search(np.array([query_vector]), k)

        result = []
        for i in indices[0]:
            result.append(json.loads(case_corpus[i])['contents'])

        return result
    except:
        return "检索时发生错误！"


def get_law_item(identifier, k=5):
    try:
        query_response = client.embeddings.create(
            model="embedding-3", input=[identifier]
        )
        query_vector = np.array(query_response.data[0].embedding)
        distances, indices = law_index.search(np.array([query_vector]), k)

        result = []
        for i in indices[0]:
            result.append(json.loads(law_corpus[i])['contents'])
        
        return result
    except:
        return "检索时发生错误！"

def get_law_knowledge(identifier, k=5):
    try:
        query_response = client.embeddings.create(
            model="embedding-3", input=[identifier]
        )
        query_vector = np.array(query_response.data[0].embedding)
        distances, indices = knowledge_index.search(np.array([query_vector]), k)

        result = []
        for i in indices[0]:
            result.append(json.loads(knowledge_corpus[i])['contents'])

        return result
    except:
        traceback.print_exc()
        return "检索时发生错误！"

def get_sum(identifier):
    nums = identifier
    if not isinstance(nums, list) or len(nums) == 0:
        return "求和时发生错误，请检查参数格式！"
    
    if any(not isinstance(x, (int, float, str)) for x in nums):
        return "求和时发生错误，请检查参数格式！"
    
    def map_str_to_num(str_num):
        try:
            str_num = str_num.replace("千", "*1e3")
            str_num = str_num.replace("万", "*1e4")
            str_num = str_num.replace("亿", "*1e8")
            return eval(str_num)
        except Exception as e:
            pass
        return "求和时发生错误，请检查参数格式！"
    
    # 统一成浮点数类型
    nums = [map_str_to_num(str(i)) for i in nums]
    
    try:
        return sum(nums)
    except Exception as e:
        pass
    return "求和时发生错误，请检查参数格式！"

def get_multiply(identifier):
    nums = identifier
    if not isinstance(nums, list) or len(nums) == 0:
        return "乘法时发生错误，请检查参数格式！"
    
    if any(not isinstance(x, (int, float, str)) for x in nums):
        return "乘法时发生错误，请检查参数格式！"
    
    def map_str_to_num(str_num):
        try:
            str_num = str_num.replace("千", "*1e3")
            str_num = str_num.replace("万", "*1e4")
            str_num = str_num.replace("亿", "*1e8")
            return eval(str_num)
        except Exception as e:
            pass
        return "乘法时发生错误，请检查参数格式！"
    
    # 统一成浮点数类型
    nums = [map_str_to_num(str(i)) for i in nums]
    
    try:
        result = 1
        for num in nums:
            result *= num
        return result
    except Exception as e:
        pass
    return "乘法时发生错误，请检查参数格式！"

def get_subtract(minuend, subtrahend):

    if not isinstance(minuend, (int, float, str)):
        return "减法时发生错误，请检查参数格式！"
    
    if not isinstance(subtrahend, (int, float, str)):
        return "减法时发生错误，请检查参数格式！"

    def map_str_to_num(str_num):
        try:
            str_num = str_num.replace("千", "*1e3")
            str_num = str_num.replace("万", "*1e4")
            str_num = str_num.replace("亿", "*1e8")
            return eval(str_num)
        except Exception as e:
            pass
        return "减法时发生错误，请检查参数格式！"
    
    minuend = map_str_to_num(str(minuend))
    subtrahend = map_str_to_num(str(subtrahend))

    try:
        return minuend - subtrahend
    except Exception as e:
        pass
    return "减法时发生错误，请检查参数格式！"

def get_divide(dividend, divisor):
    
    if not isinstance(dividend, (int, float, str)):
        return "除法时发生错误，请检查参数格式！"
    
    if not isinstance(divisor, (int, float, str)):
        return "除法时发生错误，请检查参数格式！"
    
    def map_str_to_num(str_num):
        try:
            str_num = str_num.replace("千", "*1e3")
            str_num = str_num.replace("万", "*1e4")
            str_num = str_num.replace("亿", "*1e8")
            return eval(str_num)
        except Exception as e:
            pass
        return "除法时发生错误，请检查参数格式！"
    
    dividend = map_str_to_num(str(dividend))
    divisor = map_str_to_num(str(divisor))

    try:
        # 防止除以零的错误
        if divisor == 0:
            return "除法时发生错误，除数不能为零！"
        return dividend / divisor
    except Exception as e:
        pass
    return "除法时发生错误，请检查参数格式！"


def get_company_info(identifier, columns=None):
    '''
    根据【公司名称、公司简称或公司代码】查找【上市公司】信息
    {
    '公司名称': '上海妙可蓝多食品科技股份有限公司',
    '公司简称': '妙可蓝多',
    '英文名称': 'Shanghai Milkground Food Tech Co., Ltd.',
    '关联证券': nan,
    '公司代码': 600882,
    '曾用简称': '大成股份>> *ST大成>> 华联矿业>> 广泽股份',
    '所属市场': '上交所',
    '所属行业': '食品制造业',
    '成立日期': '1988-11-29',
    '上市日期': '1995-12-06',
    '法人代表': '柴琇',
    '总经理': '柴琇',
    '董秘': '谢毅',
    '邮政编码': 200136,
    '注册地址': '上海市奉贤区工业路899号8幢',
    '办公地址': '上海市浦东新区金桥路1398号金台大厦10楼',
    '联系电话': '021-50188700',
    '传真': '021-50188918',
    '官方网址': 'www.milkground.cn',
    '电子邮箱': 'ir@milkland.com.cn',
    '入选指数': '国证Ａ指,巨潮小盘',
    '主营业务': '',
    '经营范围': '',
    '机构简介': '',
    '每股面值': 1.0,
    '首发价格': 1.0,
    '首发募资净额': 4950.0,
    '首发主承销商': nan}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    company_info['公司代码'] = company_info['公司代码'].astype(str)
    row = company_info[(company_info['公司名称'] == identifier) |
                       (company_info['公司简称'] == identifier) |
                       (company_info['公司代码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

# %%

def get_company_register(identifier, columns=None):
    '''
    根据【公司名称】查询【工商】信息
    {
    '公司名称': '天能电池集团股份有限公司',
    '登记状态': '妙可蓝多',
    '统一社会信用代码': '913305007490121183',
    '法定代表人': '',
    '注册资本': 97210.0,
    '成立日期': '2003-03-13',
    '联系地址': '',
    '联系电话': '',
    '联系邮箱': '',
    '注册号': '330500400001780',
    '组织机构代码': '74901211-8',
    '参保人数': 709,
    '行业一级': '',
    '行业二级': '',
    '行业三级': '',
    '曾用名': '天能电池集团有限公司、浙江天能电池有限公司',
    '企业简介': '',
    '经营范围': ''}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = company_register[(company_register['公司名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_company_register_name(identifier, columns=None):
    '''
    根据【统一社会信用代码】查询【公司名称】
    {
    '公司名称': '天能电池集团股份有限公司',
    '登记状态': '妙可蓝多',
    '统一社会信用代码': '913305007490121183',
    '注册资本': 97210.0,
    '成立日期': '2003-03-13',
    '省份': '浙江省',
    '城市': '湖州市',
    '区县': '长兴县',
    '注册号': '330500400001780',
    '组织机构代码': '74901211-8',
    '参保人数': 709,
    '企业类型': '其他股份有限公司（上市）',
    '曾用名': '天能电池集团有限公司、浙江天能电池有限公司'}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = company_register[(company_register['统一社会信用代码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()['公司名称']
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()['公司名称']
    else:
        return "No data found for the specified identifier."

# %%

def get_sub_company_info(identifier, columns=None):
    '''
    根据【被投资的公司名称】查询【母公司及投资】信息
    {
    '关联上市公司全称': '',
    '上市公司关系': '',
    '上市公司参股比例': '',
    '上市公司投资金额': ‘’,
    '公司名称': ‘’}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = sub_company_info[(sub_company_info['公司名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_sub_company_info_list(identifier, columns=None):
    '''
    根据【母公司的名称】查询所有【投资的子公司信息】
    {
    '关联上市公司全称': '',
    '上市公司关系': '',
    '上市公司参股比例': '',
    '上市公司投资金额': ‘’,
    '子公司名称': ‘’}
    :param identifier: 公司名称、公司简称或公司代码
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = sub_company_info[(sub_company_info['关联上市公司全称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

# %%

def get_legal_document(identifier, columns=None):
    '''
    根据【案号】查询【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    # print(identifier)
    row = legal_document[(legal_document['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_legal_document_company_list(identifier, columns=None):
    '''
    根据【关联公司】查询所有【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 关联公司
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = legal_document[(legal_document['关联公司'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_legal_document_law_list(identifier, columns=None):
    '''
    根据【律师事务所】查询所有【裁判文书】结构化相关信息
    {
    '关联公司': '',
    '标题': '',
    '案号': '',
    '文书类型': ‘’,
    '原告': ‘’,
    '被告': ‘’,
    '原告律师事务所': ‘’,
    '被告律师事务所': ‘’,
    '案由': ‘’,
    '涉案金额（元）': ‘’,
    '判决结果': ‘’,
    '日期': ‘’,
    '文件名': ‘’}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = legal_document[(legal_document['原告律师事务所'] == identifier)|(legal_document['被告律师事务所']== identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

# %%

def get_court_info(identifier, columns=None):
    '''
    根据【法院名称】查询【法院名录】相关信息
    {
    '法院名称': '',
    '法院负责人': '',
    '成立日期': '',
    '法院地址': ‘’,
    '联系电话': ‘’,
    '法院网站': ‘’}
    :param identifier: 法院名称
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = court_info[(court_info['法院名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_court_info_list(prov, city, county, columns=None):
    '''
    根据【省市区】查询所有【法院】相关信息
    {
    '法院名称': '',
    '法院负责人': '',
    '成立日期': '',
    '法院地址': ‘’,
    '联系电话': ‘’,
    '法院网站': ‘’,
    '法院省份': ‘’,
    '法院城市': ‘’,
    '法院区县': ‘’}
    :param identifier: 省市区
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = court_info[(court_info['法院省份'] == prov)& (court_info['法院城市'] == city)& (court_info['法院区县'] == county)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_court_code(identifier, columns=None):
    '''
    根据【法院名称或者法院代字】查询【法院代字】等相关数据
    {
    '法院名称': '',
    '行政级别': '',
    '法院级别': '',
    '法院代字': '',
    '区划代码': '',
    '级别': ''}
    :param identifier: 法院名称或者法院代字
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = court_code[(court_code['法院名称'] == identifier) |
                       (court_code['法院代字'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

# %%

def get_lawfirm_info(identifier, columns=None):
    '''
    根据【律师事务所】查询【律师事务所名录】

    {
    '律师事务所名称': '',
    '律师事务所唯一编码': '',
    '律师事务所负责人': '',
    '事务所注册资本': '',
    '事务所成立日期': '',
    '律师事务所地址': '',
    '通讯电话': '',
    '通讯邮箱': '',
    '律所登记机关': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = lawfirm_info[(lawfirm_info['律师事务所名称'] == identifier) |
                       (lawfirm_info['律师事务所唯一编码'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_lawfirm_info_list(prov, city, county, columns=None):
    '''
    根据【省市区】查询所有【律所】相关信息
    {
    '律师事务所名称': '',
    '律师事务所唯一编码': '',
    '律师事务所负责人': '',
    '事务所注册资本': '',
    '事务所成立日期': '',
    '律师事务所地址': '',
    '通讯电话': '',
    '通讯邮箱': '',
    '律所登记机关': '',
    '事务所省份': '',
    '事务所城市': '',
    '事务所区县': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''
    #
    row = lawfirm_info[(lawfirm_info['事务所省份'] == prov)& (lawfirm_info['事务所城市'] == city)& (lawfirm_info['事务所区县'] == county)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_lawfirm_log(identifier, columns=None):
    '''
    根据【律师事务所】查询【律师事务所服务记录】
    {
    '律师事务所名称': '',
    '业务量排名': '',
    '服务已上市公司': '',
    '报告期间所服务上市公司违规事件': '',
    '报告期所服务上市公司接受立案调查': ''}
    :param identifier: 律师事务所
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = lawfirm_log[(lawfirm_log['律师事务所名称'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

# %%

def get_address_info(identifier, columns=None):
    '''
    根据【公司地址】查询地址所在【省市区】
    {
    '地址': '',
    '省份': '',
    '城市': '',
    '区县': ''}
    :param identifier: 地址
    :param columns: 需要返回的列名列表
    :return: 地址信息字典或错误信息
    '''

    row = address_info[address_info['地址'] == identifier]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

# def get_address_code(prov, city, county, columns=None):
#     '''
#     根据省市区查询区划代码
#     {
#     '省份': '',
#     '城市': '',
#     '城市区划代码': '',
#     '县区': '',
#     '县区区划代码': ''}
#     :param identifier: 地址
#     :param columns: 需要返回的列名列表
#     :return: 地址信息字典或错误信息
#     '''

#     row = address_code[(address_code['省份'] == prov)
#                        & (address_code['城市'] == city)
#                        & (address_code['区县'] == county)]
#     if not row.empty:
#         row = row.iloc[0]
#         if columns:
#             if set(columns).issubset(row.index):
#                 return row[columns].to_dict()
#             else:
#                 return "One or more specified columns do not exist."
#         return row.to_dict()
#     else:
#         return "No data found for the specified identifier."
# def get_temp_info(date, prov, city, columns=None):
#     '''
#     根据日期及地区查询天气相关信息
#     {
#     '日期': '',
#     '省份': '',
#     '城市': '',
#     '天气': '',
#     '最高温度': '',
#     '最低温度': '',
#     '湿度': ''}
#     :param identifier: 地区，日期
#     :param columns: 需要返回的列名列表
#     :return: 天气信息字典或错误信息
#     '''
#     temp_info['日期'] = temp_info['日期'].astype(str)
#     row = temp_info[(temp_info['日期'] == date) & (temp_info['省份'] == prov) & (temp_info['城市'] == city)]
#     if not row.empty:
#         row = row.iloc[0]
#         if columns:
#             if set(columns).issubset(row.index):
#                 return row[columns].to_dict()
#             else:
#                 return "One or more specified columns do not exist."
#         return row.to_dict()
#     else:
#         return "No data found for the specified identifier."

# %%

def get_legal_abstract(identifier, columns=None):
    '''
    根据【案号】查询【文本摘要】
    {
    '文件名': '',
    '案号': '',
    '文本摘要': ''}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 地址信息字典或错误信息
    '''

    row = legal_abstract[(legal_abstract['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

# %%

def get_restriction_case(identifier, columns=None):
    '''
    根据【案号】查询【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = restriction_case[(restriction_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_restriction_case_company_list(identifier, columns=None):
    '''
    根据【限制高消费企业名称】查询所有【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 限制高消费企业名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = restriction_case[(restriction_case['限制高消费企业名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_restriction_case_court_list(identifier, columns=None):
    '''
    根据【法院】查询所有【限制高消费】相关信息
    {
    '限制高消费企业名称': '',
    '案号': '',
    '法定代表人': ‘’,
    '申请人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '限高发布日期': ‘’}
    :param identifier: 限制高消费企业名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = restriction_case[(restriction_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

# %%

def get_finalized_case(identifier, columns=None):
    '''
    根据【案号】查询【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = finalized_case[(finalized_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_finalized_case_company_list(identifier, columns=None):
    '''
    根据【企业名称】查询所有【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 终本公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = finalized_case[(finalized_case['终本公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_finalized_case_court_list(identifier, columns=None):
    '''
    根据【法院】查询所有【终本】相关信息
    {
    '终本公司名称': '',
    '案号': '',
    '被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '未履行金额（元）': ‘’,
    '执行标的（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '终本日期': ‘’}
    :param identifier: 法院
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = finalized_case[(finalized_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

# %%

def get_dishonesty_case(identifier, columns=None):
    '''
    根据【案号】查询【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = dishonesty_case[(dishonesty_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_dishonesty_case_company_list(identifier, columns=None):
    '''
    根据【企业名称】查询所有【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 失信被执行公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = dishonesty_case[(dishonesty_case['失信被执行公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

def get_dishonesty_case_court_list(identifier, columns=None):
    '''
    根据【法院】查询所有【失信被执行】相关信息
    {
    '失信被执行公司名称': '',
    '案号': '',
    '失信被执行人': ‘’,
    '疑似申请执行人': ‘’,
    '涉案金额（元）': ‘’,
    '执行法院': ‘’,
    '立案日期': ‘’,
    '发布日期': ‘’}
    :param identifier: 法院
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = dishonesty_case[(dishonesty_case['执行法院'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."

# %%

def get_administrative_case(identifier, columns=None):
    '''
    根据【案号】查询【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 案号
    :param columns: 需要返回的列名列表
    :return: 公司信息字典或错误信息
    '''

    row = administrative_case[(administrative_case['案号'] == identifier)]
    if not row.empty:
        row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.index):
                return row[columns].to_dict()
            else:
                return "One or more specified columns do not exist."
        return row.to_dict()
    else:
        return "No data found for the specified identifier."

def get_administrative_case_company_list(identifier, columns=None):
    '''
    根据【企业名称】查询所有【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 行政处罚公司名称
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = administrative_case[(administrative_case['行政处罚公司名称'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."    

def get_administrative_case_court_list(identifier, columns=None):
    '''
    根据【处罚单位】查询所有【行政处罚】相关信息
    {
    '行政处罚公司名称': '',
    '案号': '',
    '事实': ‘’,
    '处罚结果': ‘’,
    '处罚金额（元）': ‘’,
    '处罚单位': ‘’,
    '处罚日期': ‘’}
    :param identifier: 处罚单位
    :param columns: 需要返回的列名列表
    :return: 字典或错误信息list
    '''
    #
    row = administrative_case[(administrative_case['处罚单位'] == identifier)]
    if not row.empty:
        # row = row.iloc[0]
        if columns:
            if set(columns).issubset(row.columns):
                row = row[columns]
            else:
                return "One or more specified columns do not exist."
        return row.to_dict(orient='records')
    else:
        return "No data found for the specified identifier."    

# %%
def set_column_widths(table, widths):
    """设置表格列宽"""
    for i, width in enumerate(widths):
        for row in table.rows:
            row.cells[i].width = Inches(width)

def calculate_widths(dict_list, headers):
    """根据内容长度计算列宽，这里尝试改善列宽计算方法"""
    # 初始化宽度字典
    max_lengths = {key: len(key) for key in headers}  # 初始宽度设为表头的长度
    for item in dict_list:
        for key, value in item.items():
            if key in max_lengths:  # 确保只处理filtered_keys中的键
                if len(re.findall('[a-z0-9A-Z]{5,}', str(value))):
                    length = len(str(value))-10*len(re.findall('[a-z0-9A-Z]{5,}', str(value)))
                else:
                    length = len(str(value))
                if length > max_lengths[key]:
                    max_lengths[key] = length

    # 将字符长度转换为英寸
    # 考虑每个字符0.15英寸，但需要根据实际效果调整
    # 设定最小宽度为1.0英寸，最大宽度为6英寸
    return [max(0.5, min(10.0, length * 0.15)) for length in max_lengths.values()]

def get_save_dict_list_to_word(company_name, new_dict):
    # 创建一个 Word 文档
    doc = Document()

    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE  # 设置页面为横向
    section.page_width = Inches(15)  # 页面宽度
    section.page_height = Inches(8.5)  # 页面高度
    section.left_margin = Inches(0.5)  # 设置左边距
    section.right_margin = Inches(0.5)  # 设置右边距

    for key, dict_list in new_dict.items():
        dict_list = new_dict[key].copy()
        if dict_list:
            # 添加标题
            title_paragraph = doc.add_paragraph()  # 创建一个新的段落
            title_run = title_paragraph.add_run(key)  # 创建一个运行并添加文本
            title_run.font.size = Pt(24)  # 设置字体大小
            title_run.font.bold = True  # 设置字体为粗体
            title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # 设置段落居中对齐
            # 添加一个表格，行数为字典列表的长度加一（为列名预留一行），列数为第一个字典的键的数量
            skip_columns = []
            if '企业简介' in dict_list[0]:
                skip_columns.append('企业简介')
            if '经营范围' in dict_list[0]:
                skip_columns.append('经营范围')
            filtered_keys = [key for key in dict_list[0].keys() if key not in skip_columns]
            table = doc.add_table(rows=1 + len(dict_list), cols=len(filtered_keys))
            table.style = 'Table Grid'
            # 插入列名
            hdr_cells = table.rows[0].cells
            for i, key in enumerate(filtered_keys):
                hdr_cells[i].text = str(key)
                hdr_cells[i].paragraphs[0].runs[0].font.bold = True
                hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)  # 设置较小的字体大小

            # 插入行数据
            for row_index, row_data in enumerate(dict_list, 1):
                row_cells = table.rows[row_index].cells
                for i, key in enumerate(filtered_keys):
                    value = row_data[key]
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%Y-%m-%d')
                    row_cells[i].text = str(value)
                    row_cells[i].paragraphs[0].runs[0].font.size = Pt(10)  # 设置较小的字体大小
            # '企业简介' and '经营范围'
            for key in skip_columns:
                if key in dict_list[0]:
                    row = table.add_row().cells
                    row[0].merge(row[-1])  # Merge all cells in this row
                    row[0].text = f"{key}: {dict_list[0][key]}"
                    row[0].paragraphs[0].runs[0].font.size = Pt(12)  # Optional: Increase font size for emphasis


            # 计算并设置列宽
            widths = calculate_widths(dict_list, filtered_keys)
            set_column_widths(table, widths)

    # 保存文档
    middle1, middle2, middle3, middle4 = 0, 0, 0, 0
    if len(new_dict['工商信息']) >= 1:
        middle1 = len(new_dict['工商信息'][0].keys())
    if len(new_dict['子公司信息']) >= 1:
        middle2 = len(new_dict['子公司信息'][0].keys())
    if len(new_dict['裁判文书']) >= 1:
        middle3 = len(new_dict['裁判文书'][0].keys())
    if len(new_dict['限制高消费']) >= 1:
        middle4 = len(new_dict['限制高消费'][0].keys())
    check = 'Word_'+ company_name \
            + '_companyregister' + str(len(new_dict['工商信息'])) + '_' + str(middle1)\
            + '_subcompanyinfo' + str(len(new_dict['子公司信息'])) + '_' + str(middle2) \
            + '_legallist' + str(len(new_dict['裁判文书'])) + '_' + str(middle3) \
            + '_xzgxflist' + str(len(new_dict['限制高消费'])) + '_' + str(middle4)
    doc.save(check + '.docx')
    return check


# %%
key1_not_list = [
    '公司简称', '英文名称', '关联证券', '公司代码', '曾用简称', '所属市场', '所属行业', '成立日期', '上市日期',
    '法人代表', '总经理', '董秘', '邮政编码', '注册地址', '办公地址', '联系电话', '传真', '官方网址', '电子邮箱',
    '入选指数', '主营业务', '经营范围', '机构简介', '每股面值', '首发价格', '首发募资净额', '首发主承销商']
key2_not_list = [
    '登记状态', '统一社会信用代码', '法定代表人', '注册资本', '成立日期', '企业地址', '联系电话', '联系邮箱', '注册号', '组织机构代码',
    '参保人数', '行业一级', '行业二级', '行业三级', '曾用名', '企业简介', '经营范围'
]
key3_not_list = ['上市公司关系']
key4_not_list = [
    '关联公司', '标题', '文书类型', '原告', '被告', '原告律师事务所', '被告律师事务所', '案由', '涉案金额（元）', '判决结果', '日期', '文件名'
]
key5_not_list = [
    '法院名称', '法院负责人', '成立日期', '法院地址', '联系电话', '法院官网'
]
key6_not_list = ['法院名称', '行政级别', '法院级别', '法院代字', '区划代码']
key7_not_list = [
    '律师事务所唯一编码', '律师事务所负责人', '事务所注册资本', '事务所成立日期', '律师事务所地址',
    '通讯电话', '通讯邮箱', '律所登记机关'
]
key8_not_list = [
    '律师事务所名称', '业务量排名', '服务已上市公司', '报告期间所服务上市公司违规事件', '报告期所服务上市公司接受立案调查'
]
key9_not_list = ['省份', '城市', '区县']
key10_not_list = ['省份', '城市', '区县', '城市区划代码', '区县区划代码']
key11_not_list = ['日期', '省份', '城市', '天气', '最高温度', '最低温度', '湿度']
key12_not_list = ['案号', '文件名', '文本摘要']

all_list = []

# %%
# 1 get_company_info 根据【公司名称、公司简称或公司代码】查找【上市公司】信息 company_info
# 2 get_company_register 根据【公司名称】查询【工商】信息 company_register
# 3 get_company_register_name 根据【统一社会信用代码】查询【公司名称】 company_register
# 4 get_sub_company_info 根据【被投资的公司名称】查询【母公司及投资】信息 sub_company_info
# 5 get_sub_company_info_list 根据【母公司的名称】查询所有【投资的子公司信息】信息 sub_company_info
# 6 get_legal_document 根据【案号】查询【裁判文书】结构化相关信息 legal_document
# 7 get_legal_document_company_list 根据【关联公司】查询所有【裁判文书】结构化相关信息 legal_document
# 8 get_legal_document_law_list 根据【律师事务所】查询所有【裁判文书】结构化相关信息 legal_document
# 9 get_court_info 根据【法院名称】查询【法院名录】相关信息 court_info
# 10 get_court_info_list 根据【省市区】查询所有【法院】相关信息 court_info
# 11 get_court_code 根据【法院名称或者法院代字】查询【法院代字】等相关数据 court_code
# 12 get_lawfirm_info 根据【律师事务所】查询【律师事务所名录】 lawfirm_info
# 13 get_lawfirm_info_list 根据【省市区】查询所有【律所】相关信息 lawfirm_info
# 14 get_lawfirm_log 根据【律师事务所】查询【律师事务所服务记录】 lawfirm_log
# 15 get_address_info 根据【公司地址】查询地址所在【省市区】 address_info
# 16 get_legal_abstract 根据【案号】查询【文本摘要】 legal_abstract
# 17 get_restriction_case 根据【案号】查询【限制高消费】相关信息 restriction_case
# 18 get_restriction_case_company_list 根据【限制高消费企业名称】查询所有【限制高消费】相关信息 restriction_case
# 19 get_restriction_case_court_list 根据【法院】查询所有【限制高消费】相关信息 restriction_case
# 20 get_finalized_case 根据【案号】查询【终本】相关信息 finalized_case
# 21 get_finalized_case_company_list 根据【企业名称】查询所有【终本】相关信息 finalized_case
# 22 get_finalized_case_court_list 根据【法院】查询所有【终本】相关信息 finalized_case
# 23 get_dishonesty_case 根据【案号】查询【失信被执行】相关信息 dishonesty_case
# 24 get_dishonesty_case_company_list 根据【企业名称】查询所有【失信被执行】相关信息 dishonesty_case
# 25 get_dishonesty_case_court_list 根据【法院】查询所有【失信被执行】相关信息 dishonesty_case
# 26 get_administrative_case 根据【案号】查询【行政处罚】相关信息 administrative_case
# 27 get_administrative_case_company_list 根据【企业名称】查询所有【行政处罚】相关信息 administrative_case
# 28 get_administrative_case_court_list 根据【处罚单位】查询所有【行政处罚】相关信息 administrative_case
# 29 get_save_dict_list_to_word 创建一个 Word 文档