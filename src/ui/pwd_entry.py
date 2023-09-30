# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file pwd_entry.py
  @brief 获取用户 root 密码窗口
 
  @author yx 
  @date 2023-09-24 19:17
"""

import tkinter as tk
from typing import Callable


class PasswordEntry(object):
    def __init__(self, parent: tk.Tk, title: str, fuc: Callable[[str], None]):
        """

        :param parent:
        :param title: 标题
        :param fuc: 在点击 OK 后执行的方法
        """
        self.fuc = fuc

        self.window = tk.Toplevel(parent)
        self.window.title(title)

        self.pwd_entry = tk.Entry(self.window, show="*")
        self.pwd_entry.pack()

        self.ok_button = tk.Button(self.window, text="OK", command=self.getPassword)
        self.ok_button.pack()

    def getPassword(self) -> None:
        self.window.withdraw()
        self.fuc(self.pwd_entry.get())
        return
