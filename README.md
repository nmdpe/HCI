# 2024 Srping FDU HCI Course Project: CS2 Esport Coach based on LLM

想成为CS2高手玩家吗？一个简单的带有知识库的语音对话系统，帮助你成为CS2高手，同时还提供心理辅导。

# 隐私警告，必看

<big> **警告：该项目会用电脑摄像头给用户拍照，如果你有隐私要求，请遮住摄像头，或者修改代码去掉相应部分。** </big>
  
<big> **Warning: This program will take pictures of you with your computer's camera, so if you have privacy requirements, please cover the camera or modify the code to remove the appropriate parts!** </big>

# 如何运行
## 使用前准备
1. 准备好你自己的服务器。

在```client.py```和```server.py```中，服务器地址被挖掉了，需要你换自己的。另外，保证你的服务器有足够的显存。

2. 使用你自己的API，或者自行本地部署模型。
   
本项目使用阿里云的ASR和TTS以及qwen-turbo大语言模型。VLM方面，在服务器本地部署开源的LLaVA1.5-7b。另外，还本地部署了all-MiniLM-L6-v2文本嵌入模型。你需要自己购买API或者本地部署模型。

注意：本项目ASR调用代码在```ASR_ali.py```中，TTS调用代码在```TTS_test.py```中（命名混乱是这样的，当时直接使用```TTS_test.py```调试，搞了半天好不容易跑通了就直接在```server.py```中用了，没再去改命名，没办法当一个系统能正常运行时最好不要乱动。因此，不要删除任何```*_test.py```文件，毕竟当一个系统能正常运行时最好不要乱动），VLM调用代码在```VLM.py```中，请在这些文件中修改你自己的API调用代码。或者，你可以自己写好相应的API调用代码，并修改```server.py```，从而使用你自己写的API调用代码。

3. 将正确的文件放到正确的位置

```download_test.py```, ```client.py```, ```image_test.py```放自己电脑上，剩下的放服务器上。再次警告：不要删除任何```*_test.py```文件，当一个系统能正常运行时最好不要乱动。

4. 开始运行！

这些做完后，先在服务器上运行```server.py```，此时不要直接运行```client.py```，等```server.py```中LLaVA和langchain初始化完后再在自己电脑上运行```client.py```，直接说话即可，程序会自动识别一句话并及时停止录音，等待回应后程序会播放音频，播放完后可以再说下一句话。

