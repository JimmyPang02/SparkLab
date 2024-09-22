import gradio as gr

# 存储AI工具的列表
ai_tools = []

# 定义创建AI工具的函数
def create_ai_tool(name, prompt, description):
    ai_tool = {
        'name': name,
        'prompt': prompt,
        'description': description,
    }
    ai_tools.append(ai_tool)
    ai_tool_names = [tool['name'] for tool in ai_tools]
    return f"AI工具 '{name}' 创建成功！", [[tool['name'], tool['prompt'], tool['description']] for tool in ai_tools], gr.update(choices=ai_tool_names)

# 定义对话函数
def chat_with_ai_tool(selected_tool_name, user_input):
    selected_tool = next((tool for tool in ai_tools if tool['name'] == selected_tool_name), None)
    if selected_tool:
        # 模拟对话，这里可以接入你的GPT模型
        response = f"这是AI工具 '{selected_tool['name']}' 的回复： {user_input}"
        return response
    return "请选择一个有效的AI工具"

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# GPT Store")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 创建AI工具")
            name_input = gr.Textbox(label="名称")
            prompt_input = gr.Textbox(label="System Prompt")
            description_input = gr.Textbox(label="概述")
            create_button = gr.Button("创建")
            
            create_button.click(
                create_ai_tool,
                inputs=[name_input, prompt_input, description_input],
                outputs=[gr.Textbox(label="创建结果"), gr.Dataframe(headers=["名称", "System Prompt", "概述"], label="AI工具列表")]
            )

            gr.Markdown("## 选择AI工具并对话")
            ai_tool_dropdown = gr.Dropdown(choices=[], label="选择AI工具")
            chat_input = gr.Textbox(label="输入对话内容")
            chat_output = gr.Textbox(label="对话回复")
            chat_button = gr.Button("对话")
            
            chat_button.click(
                chat_with_ai_tool,
                inputs=[ai_tool_dropdown, chat_input],
                outputs=[chat_output]
            )

    # 更新下拉菜单选项
    def update_dropdown():
        print(55555555555555)
        ai_tool_names = [tool['name'] for tool in ai_tools]
        print(ai_tool_names)
        print(ai_tool_dropdown)
        return gr.update(choices=ai_tool_names)

    demo.load(update_dropdown, outputs=[ai_tool_dropdown])

# 启动Gradio界面
demo.launch()