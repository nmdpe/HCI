import speech_recognition as sr

def form(resu):
    start = resu.index('"', resu.index('"', resu.index('"') + 1) + 1) + 1
    end = resu.index('"', start)
    return resu[start:end]

def audio2text():
    r=sr.Recognizer()

    test=sr.AudioFile('voice.pcm')

    with test as source:
        audio=r.record(source)

    said=r.recognize_vosk(audio,language='zh-CN')
    return form(said)