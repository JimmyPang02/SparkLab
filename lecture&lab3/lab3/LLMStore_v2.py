import gradio as gr


# 使用会话状态来存储LLM名称列表, 思考这里为啥不用全局变量?

# 存储所有创建的LLM
llm_store = []


# 创建LLM的功能
def create_llm(name, description, system_prompt, llm_list):
    llm = {
        "name": name,
        "description": description,
        "system_prompt": system_prompt
    }
    llm_store.append(llm)
    llm_list.append(name)
    return f"LLM '{name}' 创建成功！", gr.Dropdown(choices=llm_list, interactive=True)

# 根据选择的LLM获取其详细信息
def get_llm_info(selected_llm_name):
    for llm in llm_store:
        if llm["name"] == selected_llm_name:
            return llm["name"], llm["description"]

# 对话功能
def chat_with_llm(selected_llm_name, user_input):
    for llm in llm_store:
        if llm["name"] == selected_llm_name:
            system_prompt = llm["system_prompt"]
            # 这里可以调用你的LLM模型进行对话，下面只是一个示例响应
            response = f"System Prompt: {system_prompt}\nUser Input: {user_input}\nResponse: 这是一个示例响应。"
            return response

# 创建Gradio界面
with gr.Blocks() as demo:
     
    llm_list = gr.State([]) # 用于存储LLM名称列表
    with gr.Tab("对话"):
        gr.Markdown("## LLM对话")
        llm_dropdown = gr.Dropdown(label="选择LLM", choices=[], interactive=True)
        llm_name_display = gr.Textbox(label="LLM名称", interactive=False)
        llm_description_display = gr.Textbox(label="LLM描述", interactive=False)
        user_input = gr.Textbox(label="你的输入")
        chat_button = gr.Button("发送")
        chat_output = gr.Textbox(label="对话结果")

        llm_dropdown.change(get_llm_info, inputs=llm_dropdown, outputs=[llm_name_display, llm_description_display])
        chat_button.click(chat_with_llm, inputs=[llm_dropdown, user_input], outputs=chat_output)


    with gr.Tab("创建LLM"):
        gr.Markdown("## 创建一个自定义的LLM")
        name_input = gr.Textbox(label="名称")
        description_input = gr.Textbox(label="描述")
        system_prompt_input = gr.Textbox(label="预制提示词/System Prompt")
        create_button = gr.Button("创建")
        create_output = gr.Textbox(label="创建结果")

        create_button.click(create_llm, inputs=[name_input, description_input, system_prompt_input, llm_list], 
                            outputs=[create_output, llm_dropdown])


    # 初始化下拉列表选项
    demo.load(lambda: gr.Dropdown(choices=llm_list.value, interactive=True), inputs=None, outputs=llm_dropdown)

demo.launch()
