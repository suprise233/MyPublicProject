from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 定义一个模型客户端。你可以使用其他实现了 `ChatCompletionClient` 接口的模型客户端。
# model_client = OpenAIChatCompletionClient(
#     model="gpt-4o",
#     # api_key="YOUR_API_KEY",
# )

#我们使用Gemini的模型
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-pro",
    api_key="AIzaSyBhQlfhyXZ4ATj5BIYRl5USmWzfsRCGOyk",
)


# 定义一个简单的函数工具，代理可以使用。
# 在这个例子中，我们使用一个假的天气工具进行演示。
async def get_weather(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city} 的天气是 73 度，晴天。"

# 定义一个 AssistantAgent，包含模型、工具、系统消息，并启用反思。
# 系统消息通过自然语言指示代理。
agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    tools=[get_weather],
    system_message="你是一个乐于助人的助手。",
    reflect_on_tool_use=True,
    model_client_stream=True,  # 启用从模型客户端流式传输标记。
)

# 运行代理并将消息流式传输到控制台。
async def main() -> None:
    await Console(agent.run_stream(task="纽约的天气怎么样？"))

# 注意：如果在 Python 脚本中运行此代码，你需要使用 asyncio.run(main())。
#await main()
import asyncio
asyncio.run(main())