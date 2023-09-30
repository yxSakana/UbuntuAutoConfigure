# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file label.py
  @brief 标签
 
  @author yx 
  @date 2023-09-25 02:01
"""

from typing import Union
import tkinter as tk


class Label(object):
    def __init__(self, parent: Union[tk.Tk, tk.Frame], text: str):
        self.label = tk.Label(parent, text=text)
