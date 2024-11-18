
### 功能
在电脑上监测手机屏幕，一旦手机开始刷视频必然会导致像素发生较大变化， \
于是“刷”的动作就可以被检测到，一旦有刷的动作，就开始随机从单词数据集中抽取单词进行播报。 \
实现只要在刷视频就会播单词的机制，帮助我们在夜间避免熬夜刷视频，在白天刷视频能够大量背单词的效果。  


### 安装
```
conda create --name short_video_recite_words python=3.8
conda activate short_video_recite_words
pip install pyautogui
pip install pyttsx3
pip install pandas 
pip install tkinter
# torch 可以用cpu版本，因为没有计算图
pip install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html
```za
### 文件
```
utils为有道翻译的支持文件
dataset_vocab为我自己制作的单词列表，你可以自己淘宝上找一个自己考试的词汇excel表，
处理成只有一列单词的格式（不用像我这样空这么多行），注意在第一行标上English。
mouse_calibration.py是位置标定程序，根据鼠标的位置给到坐标，调节下方的region参数
short_video_recite_words.py是主程序，直接用python指令运行
```

### 可调节的参数（也可以不调）
```
region = (30, 231, 485, 906)  # 左上角 (30, 231)，宽 485，高 906 —— 根据你想要监控的屏幕部分（这个是我投屏直接贴着左上角得到的参数）

interval = 2  # 每 2 秒截一次屏

diff_threshold = 90000  # 可以根据需要调整不同时间图片的差异阈值

# 设置语音速度和音量
engine.setProperty('rate', 200)  # 设置语速
engine.setProperty('volume', 1.0)  # 设置音量

APP_KEY = '6ec5b5e83aa35a2c'
APP_SECRET = '879tB9DrB26joPwu3wvNr0fXZ3NrfIfB'  #有道智能云上可以申请自己的api

if show == 1:  #词汇可以不显示，直接看print，因为需要时间运行

```

录手机频可以用自己选择的录频软件
