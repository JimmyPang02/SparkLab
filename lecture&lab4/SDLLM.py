from typing import * # 引入Dict,Any等类型，用于类型提示，提高代码可读性
 
import json
import requests
from openai import OpenAI
 
client = OpenAI(
    api_key="sk-HWm8ZBWVs9DStt3MM1aVWTtelJndUJmoR7rdhaV72Sf9meZG", # 替换成你的API key
    base_url="https://api.moonshot.cn/v1",
)
  
def search(arguments: Dict[str, Any]) -> Any:
    """搜索使用的是 Tavily 的API
    API文档: https://docs.tavily.com/docs/tavily-api/rest_api
    申请API KEY: https://app.tavily.com/home
    """
    search_api_key="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" # 替换成你的API key
    query = arguments["query"]
    print('searching...')
    data = {
        'api_key': search_api_key,
        'query': query,
    }
    result = result=requests.post('https://api.tavily.com/search', json=data).text
    print("搜索结果: ",result)
    return {"result": result}

def image_generator(arguments: Dict[str, Any]) -> Any:
    """生成图片
    """
    print('generating image...')

    url = "https://api.siliconflow.cn/v1/stabilityai/stable-diffusion-3-medium/text-to-image"
    prompt = arguments["prompt"] # LLM 抽取出来的prompt
    api_key="sk-ngngivsknytxsckfmbxvgrmufyabzatvdobelwnlhqlebhhi"
    payload = {
        "prompt": prompt,
        "image_size": "1024x1024",
        "batch_size": 1,
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    # 这里的"json=payload"等同于"data=json.dumps(payload)"，因为requests库提供了一个json参数，自动将python字典转换为json字符串
    response = requests.post(url, json=payload, headers=headers)

    print("生成图片工具的响应: ", json.loads(response.text)["images"][0]["url"])

    return {"result": "image"}

 
tool_map = {
    "search": search,
    "image_generator": image_generator,
}
 
tools = [
    {
        "type": "function",
        "function":     
        {
            "name": "search",  # 函数的名称，请使用英文大小写字母、数据加上减号和下划线作为函数名称
            "description": """ 
                通过搜索引擎搜索互联网上的内容。
                当你的知识无法回答用户提出的问题，或用户请求你进行联网搜索时，调用此工具。请从与用户的对话中提取用户想要搜索的内容作为 query 参数的值。
                搜索结果包含网站的标题、网站的地址（URL）以及网站简介。
            """,  # 函数的介绍，在这里写上函数的具体作用以及使用场景，以便 Kimi 大模型能正确地选择使用哪些函数
            "parameters": {  # 使用 parameters 字段来定义函数接收的参数
                "type": "object",  # 固定使用 type: object 来使 Kimi 大模型生成一个 JSON Object 参数
                "required": ["query"],  # 使用 required 字段告诉 Kimi 大模型哪些参数是必填项
                "properties": {  # properties 中是具体的参数定义，你可以定义多个参数
                    "query": {  # 在这里，key 是参数名称，value 是参数的具体定义
                        "type": "string",  # 使用 type 定义参数类型
                        "description": """
                            用户搜索的内容，请从用户的提问或聊天上下文中提取。
                        """  # 使用 description 描述参数以便 Kimi 大模型更好地生成参数
                    }
                }
            }
        },
    },
    {
        "type": "function",
        "function":     
        {
            "name": "image_generator",  # 函数的名称，请使用英文大小写字母、数据加上减号和下划线作为函数名称
            "description": """ 
                生成图片。
                当用户需要生成图片时，调用此工具。请从与用户的对话中提取用户想要生成的图片的描述作为 prompt 参数的值。
                图片生成结果包含图片的地址（URL）。
            """,  # 函数的介绍，在这里写上函数的具体作用以及使用场景，以便 Kimi 大模型能正确地选择使用哪些函数
            "parameters": {  # 使用 parameters 字段来定义函数接收的参数
                "type": "object",  # 固定使用 type: object 来使 Kimi 大模型生成一个 JSON Object 参数
                "required": ["prompt"],  # 使用 required 字段告诉 Kimi 大模型哪些参数是必填项
                "properties": {  # properties 中是具体的参数定义，你可以定义多个参数
                    "prompt": {  # 在这里，key 是参数名称，value 是参数的具体定义
                        "type": "string",  # 使用 type 定义参数类型
                        "description": """
                            用户生成图片的描述，请从用户的提问或聊天上下文中提取。
                        """  # 使用 description 描述参数以便 Kimi 大模型更好地生成参数
                    }
                }
            }
        },
    }
]

 
messages = [
    {"role": "system",
     "content": "你是 Stable Diffusion GPT，由 SparkLab 提供的人工智能画家，你更擅长中文和英文的对话以及图像的生成。你会为用户提供安全，有帮助，准确的回答，帮助其描述想要生成的图像。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。SparkLab 为专有名词，不可翻译成其他语言。"},
    {"role": "user", "content": "我想要生成一张小狗的图片"}  # 在提问中要求 Kimi 大模型联网搜索
]
 
finish_reason = None

while finish_reason is None or finish_reason == "tool_calls":
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.3,
        tools=tools,  # <-- 我们通过 tools 参数，将定义好的 tools 提交给 Kimi 大模型
    )
    choice = completion.choices[0]
    finish_reason = choice.finish_reason
    print("是否调用工具：", finish_reason)
 
    if finish_reason == "tool_calls":  # <-- 判断当前返回内容是否包含 tool_calls
        messages.append(choice.message)  # <-- 我们将 Kimi 大模型返回给我们的 assistant 消息也添加到上下文中，以便于下次请求时 Kimi 大模型能理解我们的诉求
        for tool_call in choice.message.tool_calls:  # <-- tool_calls 可能是多个，因此我们使用循环逐个执行
            tool_call_name = tool_call.function.name
            tool_call_arguments = json.loads(tool_call.function.arguments)  # <-- arguments 是序列化后的 JSON Object，我们需要使用 json.loads 反序列化一下
            tool_function = tool_map[tool_call_name]  # <-- 通过 tool_map 快速找到需要执行哪个函数
            tool_result = tool_function(tool_call_arguments)
 
            # 使用函数执行结果构造一个 role=tool 的 message，以此来向模型展示工具调用的结果；
            # 注意，我们需要在 message 中提供 tool_call_id 和 name 字段，以便 Kimi 大模型
            # 能正确匹配到对应的 tool_call。
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call_name,
                "content": json.dumps(tool_result),  # <-- 我们约定使用字符串格式向 Kimi 大模型提交工具调用结果，因此在这里使用 json.dumps 将执行结果序列化成字符串
            })
 
print("最终回复：", choice.message.content)  # <-- 在这里，我们才将模型生成的回复返回给用户