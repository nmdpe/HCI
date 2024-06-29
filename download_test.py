import requests

response=requests.get("http://10.176.34.117:8080/home/u22307140061/dld")
with open('output.wav',"wb") as file:
    file.write(response.content)