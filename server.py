import asyncio
import websockets
import websockets.server
import ASR_ali
import LLM
import TTS
import TTS_test
import VLM
import agent
from concurrent.futures import ThreadPoolExecutor


ip="10.176.34.117"

async def save_pcm(voice):
    with open("voice.pcm","wb") as file:
        file.write(voice)
        print("已保存音频")

async def send_wav(websocket):
    with open("test_tts.wav","rb") as file:
        voice=file.read()
        await websocket.send(voice)

async def save_image(image):
    with open("image.jpg","wb") as f:
        try:
            f.write(image)
            print("已保存图片")
        except IOError as e:
            print('上一张图片正在解析，该图片将被舍弃')
            asyncio.sleep(1)

def is_image(receive):
    if type(receive)==str:
        return "str"
    return "voice"

image_text=''

async def server1(websocket,path):
    global image_text
    #print("接受中")
    print("voice start")
    #image_text=""
    #LLM.get_LLM_response(image_prompt)
    while True:
        receive=await websocket.recv()
        #await save_pcm(receive)
        voice_text=ASR_ali.audio2text(voice=receive)
        #print(voice_text)
        print("你：",voice_text)
        print("VLM: ",image_text)
        if voice_text=="":
            text="听不见，重来！"
        else:
            #text=agent.get_response(f"image: {image_text}\ntext: {voice_text}")
            #text=LLM.get_LLM_response(f"text: {voice_text}")
            text=agent.get_response(user_input=voice_text,vision=image_text)
        print("LLM: ",text)
        TTS_test.text2audio(text)
        print('TTS完成')
        await send_wav(websocket)
        #await websocket.send(LLM_voice)

       
async def server2(websocket,path):
    global image_text
    while True:
        receive=await websocket.recv()
        print('图片已接受')
        await save_image(receive)
        loop=asyncio.get_running_loop()
        image_text=await loop.run_in_executor(ThreadPoolExecutor(),VLM.image_describe)
        #print(image_text)


voice_server=websockets.serve(server1,ip,5678)
image_server=websockets.serve(server2,ip,8765)

asyncio.get_event_loop().run_until_complete(voice_server)
asyncio.get_event_loop().run_until_complete(image_server)
asyncio.get_event_loop().run_forever()

'''
async def main():
    async with websockets.serve(server,ip,8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
'''
