import pyautogui
import time
import torch
import numpy as np
import pyttsx3
import pandas as pd
from datetime import datetime
from random import choice
import os
import tkinter as tk
import requests
from utils.AuthV3Util import addAuthParams

# 填写你的有道 API 凭证
# 以下是我从有道上申请的api（免费，建议自己申请一个）
APP_KEY = '6ec5b5e83aa35a2c'
APP_SECRET = '879tB9DrB26joPwu3wvNr0fXZ3NrfIfB'


def spell_and_speak(engine,word):
    # 播报单词的拼写
    # 拼接字母为连续字符串，用空格分隔
    spelled_word = " ".join(word)

    # 播报完整单词
    engine.say(spelled_word)
    engine.runAndWait()


def show_word_once(word, translation, x=2000, y=1000):
    # 创建主窗口
    root = tk.Tk()
    root.title("单词展示")

    # 设置窗口大小和位置
    width = 400
    height = 200
    root.geometry(f"{width}x{height}+{x}+{y}")  # 例如：400x200+100+100 表示窗口大小400x200，位置(100,100)

    # 添加文本标签
    label_word = tk.Label(root, text=f"English: {word}", font=("Arial", 14))
    label_word.pack(pady=10)

    label_translation = tk.Label(root, text=f"Chinese: {translation}", font=("Arial", 14))
    label_translation.pack(pady=10)

    # 显示窗口
    root.update()  # 更新窗口内容

    # 保持窗口 2 秒
    time.sleep(1)

    # 关闭窗口
    root.destroy()


def translate_text(q, lang_from="en", lang_to="zh-CHS", vocab_id=None):
    """
    使用有道翻译 API 翻译文本
    :param q: 待翻译文本
    :param lang_from: 源语言（如 'en' 表示英文）
    :param lang_to: 目标语言（如 'zh-CHS' 表示中文）
    :param vocab_id: 用户词表ID，可选
    :return: 翻译结果
    """
    url = 'https://openapi.youdao.com/api'
    data = {'q': q, 'from': lang_from, 'to': lang_to}
    if vocab_id:
        data['vocabId'] = vocab_id

    # 添加认证参数
    addAuthParams(APP_KEY, APP_SECRET, data)

    # 发起 POST 请求
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=data)

    # 返回结果解析
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")


# 初始化文本到语音的引擎
engine = pyttsx3.init()
# 设置语音速度和音量
engine.setProperty('rate', 200)  # 设置语速
engine.setProperty('volume', 1.0)  # 设置音量

# 加载词汇表
vocab_file = "dataset_vocab.xlsx"
df_vocab = pd.read_excel(vocab_file)
df_vocab = df_vocab.dropna()
vocab_list = df_vocab["English"].tolist()  # 假设列名为 'words'

# 定义截屏的区域 (x, y, width, height)
region = (30, 231, 485, 906)  # 左上角 (30, 231)，宽 485，高 906

# 定义保存文件夹路径
save_folder = "C:/Users/abcde/Desktop/iphone"
os.makedirs(save_folder, exist_ok=True)  # 如果文件夹不存在，创建它

# 定义截屏频率（以秒为单位）
interval = 2  # 每 20 秒截一次屏

# 设置差异阈值
diff_threshold = 90000  # 可以根据需要调整阈值

# 上一张图片（初始化为空张量）
previous_image = None


# 图像差异计算函数
def calculate_image_difference(image1, image2):
    # 计算两张图像之间的差异
    diff = torch.norm(image1 - image2).item()
    return diff


# 图像采样函数，返回采样的图像张量
def sample_image():
    screenshot = pyautogui.screenshot(region=region)
    image_np = np.array(screenshot)
    # 转换为 Tensor
    image_tensor = torch.tensor(image_np, dtype=torch.float32).permute(2, 0, 1)  # CxHxW
    return image_tensor


# 播放单词读音
def play_word_audio(word):
    engine.say(word)
    engine.runAndWait()


# 开始定时截屏
print("开始定时截屏，按 Ctrl+C 停止。")
count = 0
try:
    while True:
        count = count+1
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 定义文件名
        file_name = f"screenshot_{timestamp}.png"
        # 完整路径
        file_path = os.path.join(save_folder, file_name)

        # 采样当前图像
        current_image = sample_image()

        if previous_image is not None:
            # 计算当前图像与上一张图像的差异
            diff = calculate_image_difference(current_image, previous_image)
            print(f"图像差异: {diff}")
            show = 0
            # 如果差异超过阈值
            if diff > diff_threshold:
                # 随机选择一个词汇并播放语音
                word = choice(vocab_list)
                print(f"差异较大，播放单词: {word}")
                translation = translate_text(word, lang_from="en", lang_to="zh-CHS")['translation'][0]
                print(f"中文: {translation}")
                play_word_audio(word)
                play_word_audio(translation)
                spell_and_speak(engine,word)
                #选择是否图形化显示
                if show == 1:
                    show_word_once(word, translation)


        # 保存当前截图
        screenshot = pyautogui.screenshot(region=region)
        # screenshot.save(file_path)
        # print(f"已保存截图: {file_path}")
        print(f"这是第{count}次采样")
        # 更新上一张图像
        previous_image = current_image

        # 等待下一次截屏
        time.sleep(interval)
except KeyboardInterrupt:
    print("定时截屏已停止。")

