# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file select_path_widget.py
  @brief 选择目录的组建
    包含了 多选框、标签、按钮
  @author yx 
  @date 2023-09-25 02:22
"""
import os.path
import tkinter as tk
from typing import Union
from tkinter import filedialog

from ui.checkbutton import CheckbuttonWidget


class SelectPathWidget(object):
    def __init__(self, parent: Union[tk.Tk, tk.Frame], name: str, text: str, optional: bool = True):
        """

        :param parent:
        :param name: 对象名称
        :param text: 多选框显示的文本
        :param optional: 是否可选中
        """
        self._name = name

        self.initial_optional = optional
        self.checkbutton = CheckbuttonWidget(parent, text=text, status=optional, optional=optional)
        self.label = tk.Label(parent, text="None")
        self.pb = tk.Button(parent, text="select", command=self.chooseDirectory)

    def chooseDirectory(self):
        selected_directory = filedialog.askdirectory()

        if selected_directory:
            if os.path.exists(selected_directory):
                self.label.config(text=selected_directory)
                self.checkbutton.optional = True
            else:
                selected_directory = self.label.cget("text") if self.label.cget("text") != "None" else "None"
                self.label.config(text=selected_directory)
        else:
            pass

    @property
    def name(self):
        return self._name
