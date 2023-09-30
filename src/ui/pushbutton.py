# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file pushbutton.py
  @brief 按钮
  @author yx 
  @date 2023-09-25 02:12
"""

from typing import Union
import tkinter as tk


class PushButton(object):
    def __init__(self, parent: Union[tk.Tk, tk.Frame], text: str):
        self.pb = tk.Button(parent, text=text)
