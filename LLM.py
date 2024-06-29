from dashscope import Generation
import asyncio

def get_response(messages):
    response = Generation.call("qwen-turbo",
                               #max_tokens=100,
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message')
    return response.output.choices[0]['message']['content']

messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

messages=[]
# 您可以自定义设置对话轮数，当前为3
def get_LLM_response(user_input):
    messages.append({'role': 'user', 'content': user_input})
    assistant_output = get_response(messages)
    messages.append({'role': 'assistant', 'content': assistant_output})
    #print(f'用户输入：{user_input}')
    #print(f'LLM：{assistant_output}')
    #print(messages)
    #print('\n')
    return assistant_output

