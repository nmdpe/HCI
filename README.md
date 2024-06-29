HCI course project: CS2 Esport Coach based on LLM

一个简单的语音对话系统，帮助你成为CS2高手，同时还提供心理辅导。

# 警告：该项目会用电脑摄像头给你拍照，如果你有隐私要求，请遮住摄像头，或者修改代码去掉相应部分。

没法直接跑，服务器地址被挖掉了需要你换自己的; 各种API-key要自己买，自己写到环境变量里面; VLM等模型需要自己部署，然后把路径换成自己的部署路径。这些做完后，先在服务器上运行server.py，此时不要直接运行client.py，等server.py中llava和langchain初始化完后再在自己电脑上运行client.py，直接说话即可，程序会自动识别一句话并及时停止录音，等待回应后程序会播放音频，播放完后可以再说下一句话。

download_test.py, client.py, image_test.py放自己电脑上，剩下的放服务器上。注意，不要随便删除*_test.py代码，有些纯属乱命名的。
