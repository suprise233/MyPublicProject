from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from fuzzywuzzy import process

# 加载配置文件，其中包含 OpenAI API 密钥等信息 (根据您的实际情况修改)
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


# 定义关键词匹配 Agent
keyword_matching_agent = AssistantAgent(
    name="KeywordMatchingAgent",
    llm_config={"config_list": config_list},  # 使用配置列表中的第一个配置
    system_message="""
        你是一个关键词匹配专家。
        用户会输入一个可能包含拼写错误的关键词。
        你需要从给定的关键词列表中找出最匹配的正确关键词。
        使用 fuzzywuzzy 库进行相似度计算。
        只返回最匹配的关键词，不要包含其他解释。
    """,
)

# 定义用户代理 (模拟用户输入)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",  # 不需人工输入
    code_execution_config=False,  # 不需要代码执行能力
)


# 定义关键词列表
keyword_list = [
    "apple",
    "banana",
    "orange",
    "grapefruit",
    "pineapple",
    "strawberry",
    "watermelon",
]

# 定义纠错和匹配函数 (核心逻辑)
def correct_and_match_keyword(misspelled_keyword, keyword_list):
    """
    使用 fuzzywuzzy 纠正拼写错误并匹配关键词。

    Args:
        misspelled_keyword: 拼写错误的关键词。
        keyword_list: 正确关键词列表。

    Returns:
        最匹配的关键词。
    """
    best_match, score = process.extractOne(misspelled_keyword, keyword_list)
    # 可以根据需要设置一个阈值，例如 score > 80 才认为匹配成功
    if score > 80:
        return best_match
    else:
        return "No matching keyword found."


# 注册纠错函数给 KeywordMatchingAgent
keyword_matching_agent.register_reply(
    [UserProxyAgent, str],  # 接受来自 UserProxyAgent 的字符串消息
    reply_func=lambda recipient, messages, sender, config: (
        True,  # 表示已处理
        correct_and_match_keyword(messages[-1].content, keyword_list),
    ),
)


# 启动对话 (示例)
misspelled_keyword = "appel"  # 模拟用户输入错误关键词
user_proxy.initiate_chat(keyword_matching_agent, message=misspelled_keyword)

misspelled_keyword = "bannana"  # 模拟用户输入错误关键词
user_proxy.initiate_chat(keyword_matching_agent, message=misspelled_keyword)

misspelled_keyword = "straberry"  # 模拟用户输入错误关键词
user_proxy.initiate_chat(keyword_matching_agent, message=misspelled_keyword)