import speech_recognition as sr

def form(resu):
    start = resu.index('"', resu.index('"', resu.index('"') + 1) + 1) + 1
    end = resu.index('"', start)
    return resu[start:end]

r=sr.Recognizer()

test=sr.AudioFile('test.wav')

print("loadfile")

with test as source:
    audio=r.record(source)

print("getaudio")

said=r.recognize_vosk(audio,language='zh-CN')

print(form(said))