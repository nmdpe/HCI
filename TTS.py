# coding=utf-8
import os
import dashscope
from dashscope.audio.tts import SpeechSynthesizer

dashscope.api_key=os.getenv('DASHSCOPE_API_KEY')


def text2audio(text):
    print('TEXT2AUDIO:',text)

    result = SpeechSynthesizer.call(model='sambert-zhida-v1',
                                    text='text',
                                    sample_rate=48000)

    #return result.get_audio_data()
    
    if result.get_audio_data() is not None:
        with open('test_tts.wav', 'wb') as f:
            f.write(result.get_audio_data())  
    

#text2audio("好好好好好好")