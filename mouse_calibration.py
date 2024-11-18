import pyautogui
import tkinter as tk

# 创建窗口
root = tk.Tk()
root.title("鼠标位置追踪器")

# 标签显示坐标
label = tk.Label(root, text="鼠标位置: X=0, Y=0", font=("Arial", 16))
label.pack(padx=20, pady=20)

def update_mouse_position():
    # 获取鼠标当前位置
    x, y = pyautogui.position()
    # 更新标签内容
    label.config(text=f"鼠标位置: X={x}, Y={y}")
    # 每隔 100ms 更新一次
    root.after(100, update_mouse_position)

# 启动鼠标位置更新
update_mouse_position()

# 启动 Tkinter 主循环
root.mainloop()