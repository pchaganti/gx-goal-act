from api import *

class Tool():
    def __init__(self, func, name, description):
        self.func = func
        self.name = name
        self.description = description
    
    def is_name(self, name):
        return name == self.name

get_company_info_tool = Tool(
    func=get_company_info,
    name="get_company_info",
    description=(
        "根据[公司名称, 公司简称或者公司代码]在[CompanyInfo]表格中查询对应的上市公司信息. \n"
        "[输入参数]:\n"
        "identifier(str): 公司名称, 公司简称或者公司代码\n"
        "columns(list): 需要返回的列名列表\n"
        "[返回值]:\n"
        "返回公司信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_rank_tool = Tool(
    func=get_rank,
    name="get_rank",
    description=(
        "根据[输入列表]进行[排序]得到结果, 通常在需要知道最大值或者最小值时可以使用. \n"
        "[输入参数]:\n"
        "identifier(list[int, float, str]): 输入列表\n"
        "is_desc(str): 'True'代表降序排列, 'False'代表升序排列\n"
        "[返回值]:\n"
        "返回列表排序后的结果(list), 或者在排序过程中发生错误时返回相应的错误信息. "
    )
)

get_multiply_tool = Tool(
    func=get_multiply,
    name="get_multiply",
    description=(
        "根据[输入列表]进行[乘法]得到结果. \n"
        "[输入参数]:\n"
        "identifier(list[int, float, str]): 输入列表\n"
        "[返回值]:\n"
        "返回列表求乘法后的结果([int, float]), 或者在求乘法过程中发生错误时返回相应的错误信息. "
    )
)

get_subtract_tool = Tool(
    func=get_subtract,
    name="get_subtract",
    description=(
        "根据[被减数, 减数]进行[减法]得到结果. \n"
        "[输入参数]:\n"
        "minuend([int, float, str]): 被减数\n"
        "subtrahend([int, float, str]): 减数\n"
        "[返回值]:\n"
        "返回列表求减法后的结果([int, float]), 或者在求减法过程中发生错误时返回相应的错误信息. "
    )
)

get_divide_tool = Tool(
    func=get_divide,
    name="get_divide",
    description=(
        "根据[被除数, 除数]进行[除法]得到结果. \n"
        "[输入参数]:\n"
        "dividend([int, float, str]): 被除数\n"
        "divisor([int, float, str]): 除数\n"
        "[返回值]:\n"
        "返回列表求除法后的结果([int, float]), 或者在求除法过程中发生错误时返回相应的错误信息. "
    )
)

get_sum_tool = Tool(
    func=get_sum,
    name="get_sum",
    description=(
        "根据[输入列表]进行[求和]得到结果, 通常是对金额进行求和时可以使用. \n"
        "[输入参数]:\n"
        "identifier(list[int, float, str]): 输入列表\n"
        "[返回值]:\n"
        "返回列表求和后的结果([int, float]), 或者在求和过程中发生错误时返回相应的错误信息. "
    )
)

get_law_item_tool = Tool(
    func=get_law_item,
    name="get_law_item",
    description=(
        "根据[输入内容]检索相关法律条文. 通常在生成法律文书时可以使用. \n"
        "[输入参数]:\n"
        "identifier(str): 输入内容\n"
        "k(int): 返回最相似的前k个结果"
        "[返回值]:\n"
        "返回检索得到的法律条文的列表([str]), 长度为k, 或者在检索过程中发生错误时返回相应的错误信息. "
    )
)

get_law_case_tool = Tool(
    func=get_law_case,
    name="get_law_case",
    description=(
        "根据[输入内容]检索相关法律案件. 通常在生成法律文书时可以使用. \n"
        "[输入参数]:\n"
        "identifier(str): 输入内容\n"
        "k(int): 返回最相似的前k个结果"
        "[返回值]:\n"
        "返回检索得到的法律案件的列表([str]), 长度为k, 或者在检索过程中发生错误时返回相应的错误信息. "
    )
)

get_law_knowledge_tool = Tool(
    func=get_law_knowledge,
    name="get_law_knowledge",
    description=(
        "根据[输入内容]检索相关法律知识. 通常在生成法律文书时可以使用. \n"
        "[输入参数]:\n"
        "identifier(str): 输入内容\n"
        "k(int): 返回最相似的前k个结果"
        "[返回值]:\n"
        "返回检索得到的法律知识的列表([str]), 长度为k, 或者在检索过程中发生错误时返回相应的错误信息. "
    )
)

get_company_register_tool = Tool(
    func=get_company_register,
    name="get_company_register",
    description=(
        "根据[公司名称]在[CompanyRegister]表格中查询对应的公司工商信息. \n"
        "[输入参数]:\n"
        "identifier(str): 公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回公司信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_company_register_name_tool = Tool(
    func=get_company_register_name,
    name="get_company_register_name",
    description=(
        "根据[统一社会信用代码]在[CompanyRegister]表格中查询对应的公司名称. \n"
        "[输入参数]:\n"
        "identifier(str): 统一社会信用代码\n"
        "[返回值]:\n"
        "返回公司名称(str), 或者在查询过程中发生错误时返回相应的错误信息. . "
    )
)

get_sub_company_info_tool = Tool(
    func=get_sub_company_info,
    name="get_sub_company_info",
    description=(
        "根据[被投资的公司名称]在[SubCompanyInfo]表格中查询对应的母公司及投资信息. \n"
        "[输入参数]:\n"
        "identifier(str): 公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回母公司及投资信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_sub_company_info_list_tool = Tool(
    func=get_sub_company_info_list,
    name="get_sub_company_info_list",
    description=(
        "根据[关联上市公司全称]在[SubCompanyInfo]表格中查询该母公司投资的所有子公司信息. \n"
        "[输入参数]:\n"
        "identifier(str): 关联上市公司全称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回子公司信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_legal_document_tool = Tool(
    func=get_legal_document,
    name="get_legal_document",
    description=(
        "根据[案号]在[LegalDoc]表格中查询对应的裁判文书信息. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回裁判文书信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_legal_document_company_list_tool = Tool(
    func=get_legal_document_company_list,
    name="get_legal_document_company_list",
    description=(
        "根据[关联公司名称]在[LegalDoc]表格中查询对应的裁判文书信息. \n"
        "[输入参数]:\n"
        "identifier(str): 关联公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回裁判文书信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_legal_document_law_list_tool = Tool(
    func=get_legal_document_law_list,
    name="get_legal_document_law_list",
    description=(
        "根据[律师事务所名称]在[LegalDoc]表格中查询对应的裁判文书信息. \n"
        "[输入参数]:\n"
        "identifier(str): 律师事务所名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回裁判文书信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_court_info_tool = Tool(
    func=get_court_info,
    name="get_court_info",
    description=(
        "根据[法院名称]在[CourtInfo]表格中查询对应的法院相关信息\n"
        "[输入参数]:\n"
        "identifier(str): 法院名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回法院信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_court_info_list_tool = Tool(
    func=get_court_info_list,
    name="get_court_info_list",
    description=(
        "根据[省市区]在[CourtInfo]表格中查询对应的法院相关信息. \n"
        "[输入参数(3个输入参数都必须输入，不能缺失)]:\n"
        "prov(str): 省份(要求完整,带'省'/'市'等)\n"
        "city(str): 城市(要求完整,带'市'等)\n"
        "county(str): 区县(要求完整,带'区'等)\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回法院信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_court_code_tool = Tool(
    func=get_court_code,
    name="get_court_code",
    description=(
        "根据[法院名称或者法院代字]在[CourtCode]表格中查询对应的法院相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 法院名称或者法院代字\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回法院信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_lawfirm_info_tool = Tool(
    func=get_lawfirm_info,
    name="get_lawfirm_info",
    description=(
        "根据[律师事务所名称]在[LawfirmInfo]表格中查询对应的律师事务所相关信息. \n" 
        "[输入参数]:\n"
        "identifier(str): 律师事务所名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回律师事务所信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_lawfirm_info_list_tool = Tool(
    func=get_lawfirm_info_list,
    name="get_lawfirm_info_list",
    description=(
        "根据[省市区]在[LawfirmInfo]表格中查询对应的律师事务所相关信息. \n"
        "[输入参数(3个输入参数都必须输入，不能缺失)]:\n"
        "prov(str): 省份(要求完整,带'省'/'市'等)\n"
        "city(str): 城市(要求完整,带'市'等)\n"
        "county(str): 区县(要求完整,带'区'等)\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回律师事务所信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_lawfirm_log_tool = Tool(
    func=get_lawfirm_log,
    name="get_lawfirm_log",
    description=(
        "根据[律师事务所名称]在[LawfirmLog]表格中查询对应的律师事务所服务记录. \n"
        "[输入参数]:\n"
        "identifier(str): 律师事务所名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回律师事务所服务记录的信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_address_info_tool = Tool(
    func=get_address_info,
    name="get_address_info",
    description=(
        "根据[地址]在[AddrInfo]表格中查询对应的地址所在省市区. \n"
        "[输入参数]:\n"
        "identifier(str): 地址\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回公司地址所在省市区的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_legal_abstract_tool = Tool(
    func=get_legal_abstract,
    name="get_legal_abstract",
    description=(
        "根据[案号]在[LegalAbstract]表格中查询对应的案件的文本摘要. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回案件文本摘要的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_restriction_case_tool = Tool(
    func=get_restriction_case,
    name="get_restriction_case",
    description=(
        "根据[案号]在[RestrictionCase]表格中查询对应的限制高消费案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回限制高消费案件信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_restriction_case_company_list_tool = Tool(
    func=get_restriction_case_company_list,
    name="get_restriction_case_company_list",
    description=(
        "根据[限制高消费企业名称]在[RestrictionCase]表格中查询对应的限制高消费案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 限制高消费企业名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回限制高消费案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_restriction_case_court_list_tool = Tool(
    func=get_restriction_case_court_list,
    name="get_restriction_case_court_list",
    description=(
        "根据[执行法院名称]在[RestrictionCase]表格中查询对应的限制高消费案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 执行法院名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回限制高消费案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_finalized_case_tool = Tool(
    func=get_finalized_case,
    name="get_finalized_case",
    description=(
        "根据[案号]在[FinalizedCase]表格中查询对应的终本案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回终本案件信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_finalized_case_company_list_tool = Tool(
    func=get_finalized_case_company_list,
    name="get_finalized_case_company_list",
    description=(
        "根据[终本公司名称]在[FinalizedCase]表格中查询对应的终本案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 终本公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回终本案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_finalized_case_court_list_tool = Tool(
    func=get_finalized_case_court_list,
    name="get_finalized_case_court_list",
    description=(
        "根据[执行法院名称]在[FinalizedCase]表格中查询对应的终本案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 执行法院名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回终本案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_dishonesty_case_tool = Tool(
    func=get_dishonesty_case,
    name="get_dishonesty_case",
    description=(
        "根据[案号]在[DishonestyCase]表格中查询对应的失信被执行案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回失信被执行案件信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_dishonesty_case_company_list_tool = Tool(
    func=get_dishonesty_case_company_list,
    name="get_dishonesty_case_company_list",
    description=(
        "根据[失信被执行公司名称]在[DishonestyCase]表格中查询对应的失信被执行案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 失信被执行公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回失信被执行案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_dishonesty_case_court_list_tool = Tool(
    func=get_dishonesty_case_court_list,
    name="get_dishonesty_case_court_list",
    description=(
        "根据[执行法院名称]在[DishonestyCase]表格中查询对应的失信被执行案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 执行法院名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回失信被执行案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_administrative_case_tool = Tool(
    func=get_administrative_case,
    name="get_administrative_case",
    description=(
        "根据[案号]在[AdministrativeCase]表格中查询对应的行政处罚案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 案号\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回行政处罚案件信息的字典, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_administrative_case_company_list_tool = Tool(
    func=get_administrative_case_company_list,
    name="get_administrative_case_company_list",
    description=(
        "根据[行政处罚公司名称]在[AdministrativeCase]表格中查询对应的行政处罚案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 行政处罚公司名称\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回行政处罚案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)

get_administrative_case_court_list_tool = Tool(
    func=get_administrative_case_court_list,
    name="get_administrative_case_court_list",
    description=(
        "根据[处罚单位]在[AdministrativeCase]表格中查询对应的行政处罚案件相关信息. \n"
        "[输入参数]:\n"
        "identifier(str): 处罚单位\n"
        "columns(list): 需要返回的列名列表\n" 
        "[返回值]:\n"
        "返回行政处罚案件信息的列表, 或者在查询过程中发生错误时返回相应的错误信息. "
    )
)


CompanyInfo_tools = []
CompanyInfo_tools.append(get_company_info_tool)
CompanyRegister_tools = []
CompanyRegister_tools.append(get_company_register_tool)
CompanyRegister_tools.append(get_company_register_name_tool)
SubCompanyInfo_tools = []
SubCompanyInfo_tools.append(get_sub_company_info_tool)
SubCompanyInfo_tools.append(get_sub_company_info_list_tool)
LegalDocInfo_tools = []
LegalDocInfo_tools.append(get_legal_document_tool)
LegalDocInfo_tools.append(get_legal_document_company_list_tool)
LegalDocInfo_tools.append(get_legal_document_law_list_tool)
Court_tools = []
Court_tools.append(get_court_info_tool)
Court_tools.append(get_court_info_list_tool)
Court_tools.append(get_court_code_tool)
Law_tools = []
Law_tools.append(get_lawfirm_info_tool)
Law_tools.append(get_lawfirm_info_list_tool)
Law_tools.append(get_lawfirm_log_tool)
Address_tools = []
Address_tools.append(get_address_info_tool)
Abstract_tools = []
Abstract_tools.append(get_legal_abstract_tool)
RestrictionCase_tools = []
RestrictionCase_tools.append(get_restriction_case_tool)
RestrictionCase_tools.append(get_restriction_case_company_list_tool)
RestrictionCase_tools.append(get_restriction_case_court_list_tool)
FinalizedCase_tools = []
FinalizedCase_tools.append(get_finalized_case_tool)
FinalizedCase_tools.append(get_finalized_case_company_list_tool)
FinalizedCase_tools.append(get_finalized_case_court_list_tool)
DishonestyCase_tools = []
DishonestyCase_tools.append(get_dishonesty_case_tool)
DishonestyCase_tools.append(get_dishonesty_case_company_list_tool)
DishonestyCase_tools.append(get_dishonesty_case_court_list_tool)
AdministrativeCase_tools = []
AdministrativeCase_tools.append(get_administrative_case_tool)
AdministrativeCase_tools.append(get_administrative_case_company_list_tool)
AdministrativeCase_tools.append(get_administrative_case_court_list_tool)

Tools_map = {
    "CompanyInfo": CompanyInfo_tools,
    "CompanyRegister": CompanyRegister_tools,
    "SubCompanyInfo": SubCompanyInfo_tools,
    "LegalDoc": LegalDocInfo_tools,
    "CourtInfo": Court_tools,
    "CourtCode": Court_tools,
    "LawfirmInfo": Law_tools,
    "LawfirmLog": Law_tools,
    "AddrInfo": Address_tools,
    "LegalAbstract": Abstract_tools,
    "RestrictionCase": RestrictionCase_tools,
    "FinalizedCase": FinalizedCase_tools,
    "DishonestyCase": DishonestyCase_tools,
    "AdministrativeCase": AdministrativeCase_tools
}

# 待维护和和使用
Tools_prompt = {
    "CompanyInfo": "CompanyInfo表格可以使用的API_tool包括 1.get_company_info: 根据[公司名称], [公司简称]或[公司代码]查找上市公司信息, 遇到公司简称只使用这个表格. ",
    "CompanyRegister": "CompanyRegister表格可以使用的API_tool包括 1.get_company_register: 根据[公司名称]查询工商信息 2.get_company_register_name: 根据[统一社会信用代码]查询[公司名称]",
    "SubCompanyInfo": "SubCompanyInfo表格可以使用的API_tool包括 1.get_sub_company_info: 根据被投资的子[公司名称]获得表格内其他字段信息 2.get_sub_comp any_info_list: 根据[关联上市公司全称]称查询该公司投资的所有子公司信息list",
    "LegalDoc": "LegalDoc表格可以使用的API_tool包括 1.get_legal_document: 根据[案号]查询裁判文书相关信息 2.get_legal_document_company_list: 根据[关联公司]查询所有裁判文书相关信息list",
    "CourtInfo": "CourtInfo表格可以使用的API_tool包括 1.get_court_info: 根据[法院名称]查询表格相关信息",
    "CourtCode": "CourtCode表格可以使用的API_tool包括 1.get_court_code: 根据[法院名称]或者[法院代字]查询表格等相关数据, 遇到法院代字只使用这个表格. ",
    "LawfirmInfo": "LawfirmInfo可以使用的API_tool包括 1.get_lawfirm_info: 根据[律师事务所名称]查询表格相关信息",
    "LawfirmLog": "LawfirmLog表格可以使用的API_tool包括 1.get_lawfirm_log: 根据[律师事务所名称]查询表格相关信息",
    "AddrInfo": "AddrInfo表格可以使用的API_tool包括 1.get_address_info: 根据[地址]查该地址对应的省份城市区县",
    "LegalAbstract": "LegalAbstract表格可以使用的API_tool包括 1.get_legal_abstract: 根据[案号]查询文本摘要",
    "RestrictionCase": "RestrictionCase表格可以使用的API_tool包括 1.get_restriction_case: 根据[案号]查询限制高消费相关信息 2.get_restriction_case_company_list: 根据[限制高消费企业名称]查询所有限制高消费相关信息list",
    "FinalizedCase": "FinalizedCase表格可以使用的API_tool包括 1.get_restriction_case: 根据[案号]查询限制高消费相关信息 2.get_restriction_case_company_list: 根据[限制高消费企业名称]查询所有限制高消费相关信息list",
    "DishonestyCase": "DishonestyCase表格可以使用的API_tool包括 1.get_restriction_case: 根据[案号]查询限制高消费相关信息 2.get_restriction_case_company_list: 根据[限制高消费企业名称]查询所有限制高消费相关信息list",
    "AdministrativeCase": "AdministrativeCase表格可以使用的API_tool包括 1.get_restriction_case: 根据[案号]查询限制高消费相关信息 2.get_restriction_case_company_list: 根据[限制高消费企业名称]查询所有限制高消费相关信息list",
}

tools = [
    get_company_info_tool,
    get_company_register_tool,
    get_company_register_name_tool,
    get_sub_company_info_tool,
    get_sub_company_info_list_tool,
    get_legal_document_tool,
    get_legal_document_company_list_tool,
    get_legal_document_law_list_tool,
    get_court_info_tool,
    get_court_info_list_tool,
    get_court_code_tool,
    get_lawfirm_info_tool,
    get_lawfirm_info_list_tool,
    get_lawfirm_log_tool,
    get_address_info_tool,
    get_legal_abstract_tool,
    get_restriction_case_tool,
    get_restriction_case_company_list_tool,
    get_restriction_case_court_list_tool,
    get_finalized_case_tool,
    get_finalized_case_company_list_tool,
    get_finalized_case_court_list_tool,
    get_dishonesty_case_tool,
    get_dishonesty_case_company_list_tool,
    get_dishonesty_case_court_list_tool,
    get_administrative_case_tool,
    get_administrative_case_company_list_tool,
    get_administrative_case_court_list_tool,
    get_sum_tool,
    get_rank_tool,
    get_divide_tool,
    get_multiply_tool,
    get_subtract_tool,
    get_law_case_tool,
    get_law_item_tool,
    get_law_knowledge_tool
]

import traceback

def is_tool_name(name):
    for tool in tools:
        if tool.is_name(name):
            return True
    return False

def call_(name, input):
    try:
        for tool in tools:
            if tool.is_name(name):
                if tool.name == "get_law_case" or tool.name == "get_law_item" or tool.name == "get_law_knowledge":
                    if isinstance(input, dict):
                        if 'k' not in input.keys():
                            return tool.func(input['identifier'])
                        return tool.func(input['identifier'], int(input['k']))
                    if isinstance(input, str):
                        return tool.func(input)
                elif tool.name == "get_sum" or tool.name == "get_multiply":
                    if isinstance(input, list):
                        return tool.func(input)
                    return tool.func(input['identifier'])
                elif tool.name == "get_subtract":
                    return tool.func(input['minuend'], input['subtrahend'])
                elif tool.name == "get_divide":
                    return tool.func(input['dividend'], input['divisor'])
                elif tool.name == "get_rank":
                    if isinstance(input, list):
                        return tool.func(input, False)
                    else:
                        return tool.func(input['identifier'], input['is_desc'] == 'True')
                elif tool.name == "get_court_info_list" or tool.name == "get_lawfirm_info_list":
                    return tool.func(input['prov'], input['city'], input['county'], input['columns'])
                return tool.func(input['identifier'], input['columns'])
    except:
        traceback.print_exc()
    return "工具调用发生错误, 请检查传入工具的参数是否正确!"