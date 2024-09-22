import gradio as gr


def count_characters(text):
    #"最核心的逻辑"
    return len(text)

iface = gr.Interface(
    fn=count_characters,
    inputs=[gr.Textbox(lines=2, label="Enter some text here:")],
    outputs=[gr.Number(label="Number of characters")],
    # title="Character Counter",
    # description="Enter a text to count its characters."
)



iface.launch()

# iface.launch(share=True) # share=True to make the app accessible to others
