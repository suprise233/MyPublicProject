from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
我们使用Gemini的模型
model_client = OpenAIChatCompletionClient(
model="gemini-1.5-pro",
api_key="AIzaSyBhQlfhyXZ4ATj5BIYRl5USmWzfsRCGOyk",  # 替换为你的 Gemini API 密钥
)
定义美食代理
food_agent = AssistantAgent(
name="food_agent",
model_client=model_client,
system_message="你是一个美食专家，可以提供关于城市美食的建议和信息，但请简短回答，不超过100字。",
model_client_stream=True,
)
定义风景代理
scenery_agent = AssistantAgent(
name="scenery_agent",
model_client=model_client,
system_message="你是一个旅行专家，可以提供关于城市风景名胜的建议和信息，但请简短回答，不超过100字。",
model_client_stream=True,
)
定义工具函数，用于调用美食代理
async def get_food_info(city: str) -> str:
"""获取指定城市的美食信息。"""
messages = [UserMessage(content=f"请提供 {city} 的美食信息。")]
response = await food_agent.a_generate_reply(messages)
return response.content
定义工具函数，用于调用风景代理
async def get_scenery_info(city: str) -> str:
"""获取指定城市的风景信息。"""
messages = [UserMessage(content=f"请提供 {city} 的风景信息。")]
response = await scenery_agent.a_generate_reply(messages)
return response.content
定义主代理 (main agent)
main_agent = AssistantAgent(
name="main_agent",
model_client=model_client,
tools=[get_food_info, get_scenery_info],
system_message="""你是一个乐于助人的助手，可以帮助用户查询城市信息。
你可以根据用户的问题选择合适的工具来回答：
- 如果用户询问美食相关信息，请使用 get_food_info 工具。
- 如果用户询问风景名胜相关信息，请使用 get_scenery_info 工具。""",
reflect_on_tool_use=True,
model_client_stream=True,
)
运行代理并将消息流式传输到控制台。
async def main() -> None:
# 获取用户输入
question = input("请输入您要查询的问题（关于城市的美食或风景）：")
await Console(main_agent.run_stream(task=question))  # 直接使用用户输入作为任务
import asyncio
asyncio.run(main())