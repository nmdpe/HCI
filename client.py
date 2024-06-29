import pyaudio
import speech_recognition as sr
import websockets
import asyncio
import time
import requests
import wave
import cv2
from typing import Union
from concurrent.futures import ThreadPoolExecutor


async def get_sentence():
    rate=16000
    rcg=sr.Recognizer()
    rcg.pause_threshold=0.8
    rcg.energy_threshold=600
    with sr.Microphone(sample_rate=rate) as src:
        print("录音中......")
        voice=rcg.listen(src,phrase_time_limit=8)

    '''
    with open("voice.pcm","wb") as f:
        f.write(voice.get_wav_data())
    '''
    print("录音结束")
    return voice.get_wav_data()

voice_ip="换自己的服务器，5678端口"
image_ip="换自己的服务器，8765端口"

async def send_pcm(websocket):
    with open("voice.pcm","rb") as file:
        voice=file.read()
        #await websocket.send("voice")
        await websocket.send(voice)

async def save_wav(voice):
    with open("output.wav","wb") as file:
        file.write(voice)
        print("保存回复")

def play_audio():
    chunk = 1024  
    wf = wave.open(r"output.wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)  # 读取数据
    #print(data)
    while data != b'':  # 播放
        stream.write(data)
        data = wf.readframes(chunk)
        #print('while循环中！')
        #print(data)
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio

    return "播放完毕"

def get_image():
    cap=cv2.VideoCapture(0)
    if cap.isOpened():
        ret,frame=cap.read()
        if ret:
            cv2.imwrite('./image.jpg',frame)
        cap.release() 
    cv2.destroyAllWindows()

async def send_image(ws):
    while True:
        loop=asyncio.get_running_loop()
        executor=ThreadPoolExecutor()
        await loop.run_in_executor(executor,get_image)
        with open("image.jpg","rb") as f:
            image=f.read()
            print("正在上传图片")
            await ws.send(image)
            print("上传图片成功")
        await asyncio.sleep(10)

async def send_voice(ws):
    while True:
        user_voice=await get_sentence()
        #asyncio.get_event_loop().run_until_complete(voice_client())
        print("上传语音中")
        #await send_pcm(ws)
        await ws.send(user_voice)
        print("上传语音成功")
        voice=await ws.recv()
        #print(text)
        #download()
        await save_wav(voice)
        print('下载语音成功')
        loop=asyncio.get_running_loop()
        executor=ThreadPoolExecutor()
        future=await loop.run_in_executor(executor,play_audio)
        print(future)

async def image_client():
    while True:
        try:
            async with websockets.connect(image_ip) as ws:
                try:
                    await send_image(ws)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    print('即将重连')
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            print('连接失败，再次重连')


async def voice_client():
    print("连接中")
    while True:
        try:
            async with websockets.connect(voice_ip) as ws:
                try:
                    await send_voice(ws)
                    #await send_voice(ws)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    print("即将重连")
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            print("连接失败，再次重连")

async def main():
    await asyncio.gather(voice_client(),image_client())

asyncio.run(main())

    
