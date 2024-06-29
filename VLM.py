from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path
from llava.eval.run_llava import eval_model

model_path="/home/u22307140061/LLaVA/llava-v1.5-7b"

tokenizer, model, image_processor, context_len = load_pretrained_model(
    model_path=model_path,
    model_base=None,
    model_name=get_model_name_from_path(model_path),
    load_4bit=True
)

#prompt = "What are the things I should be cautious about when I visit here?"
prompt = 'You are able to understand the visual content that the user provides, and assist the user with a variety of tasks using natural language. You only need to describe the human in the image. You need to explicitly describe the facial expression, movement and sentiment of the human in the image. Follow the instructions carefully and explain your answers in detail. ###Human: Hi! ###Assistant: Hi there! How can I help you today?###Human: Describe the scene in brief.###Assistant:The image shows'
image_file = "image.jpg"

args = type('Args', (), {
    "model_path": model_path,
    "model_base": None,
    "model_name": get_model_name_from_path(model_path),
    "query": prompt,
    "conv_mode": None,
    "image_file": image_file,
    "sep": ",",
    "temperature": 0,
    "top_p": None,
    "num_beams": 1,
    "max_new_tokens": 512,
    "stop": '###'
})()

def image_describe():
    print("开始使用vlm")
    return eval_model(args)