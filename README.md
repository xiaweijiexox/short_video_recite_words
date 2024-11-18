### 安装
```
conda create --name short video_recite_words python=3.8
pip install pyautogui
pip install pyttsx3
pip install pandas 
pip install tkinter
# torch 可以用cpu版本，因为没有计算图
pip install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html
```

### 可调节的参数（也可以不调）
```
region = (30, 231, 485, 906)  # 左上角 (30, 231)，宽 485，高 906 —— 根据你想要监控的屏幕部分（这个是投屏直接贴着左上角得到的参数）

interval = 2  # 每 2 秒截一次屏

diff_threshold = 90000  # 可以根据需要调整不同时间图片的差异阈值

# 设置语音速度和音量
engine.setProperty('rate', 200)  # 设置语速
engine.setProperty('volume', 1.0)  # 设置音量

APP_KEY = '6ec5b5e83aa35a2c'
APP_SECRET = '879tB9DrB26joPwu3wvNr0fXZ3NrfIfB'  #有道智能云上可以申请自己的api

if show == 1:  #词汇可以不显示，直接看print，因为需要时间运行

```

录频可以用自己选择的录频软件