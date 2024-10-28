import json
import os
from fastmodels import llmop
from fastmodels.types.easyllm.response_params import AgentCompletionChunk

# 初始化客户端
client = llmop(
    api_key="",
    project_id=""
)
stream = True
# 调用接口
response = client.agent.threads.create_and_run(
    agent_id="",
    messages=[
        {"role": "assistant", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁"},
    ],
    stream=stream
)




