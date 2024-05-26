"""
* 用于创建初始的gui界面，已通过 TEST
"""

import tkinter as tk
from tkinter import messagebox

def get_pages():
    response = messagebox.askyesno("Bye~", "好的，马上开始爬虫")
    if response:
        pages = entry.get() # & pages: str --> int
        window.destroy()
        return pages

def init_gui():
    global window, label, entry, button, pages
    window = tk.Tk()
    window.title("获取爬取相关参数 ^V^")
    window.geometry("500x300")

    label = tk.Label(window, text="告诉我你想要爬取多少数据(n*25)? 请在下方输入n", bg='yellow', fg='red', font=('consolas',12), width=50, height=5)
    label.pack(pady=15)

    entry = tk.Entry(window, show=None, width=5, justify='center')
    entry.pack(pady=5)

    button = tk.Button(window, text="OK", width=10, height=1, command=get_pages)
    button.pack()

    window.mainloop()
    return pages

 