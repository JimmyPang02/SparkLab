from openai import OpenAI
 

def get_LLM_response(user_input,systen_prompt):
    client = OpenAI(
        api_key = "sk-HWm8ZBWVs9DStt3MM1aVWTtelJndUJmoR7rdhaV72Sf9meZG", # key替换成你的API key
        base_url = "https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": systen_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature = 0.3
    )
 
    return completion.choices[0].message.content    
        

