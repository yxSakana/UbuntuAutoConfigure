# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file checkbutton.py
  @brief 多选框
    支持设置当前状态、是否可选
  @author yx 
  @date 2023-09-24 17:06
"""

from typing import Union, Callable
import tkinter as tk


class CheckbuttonWidget(object):
    def __init__(self, parent: Union[tk.Tk, tk.Frame], text: str,
                 command: Callable = None, status: bool = False, name: str = "", optional: bool = True):
        """

        :param parent: 父对象
        :param text: 多选框显示的文字
        :param command: 回调函数
        :param status: 开始状态为 选中/未选中
        :param name: 该对象的名称
        :param optional: 是否是可选中的
        """
        self._status: tk.BooleanVar = tk.BooleanVar()
        self._status.set(status)

        self.checkbutton: tk.Checkbutton = tk.Checkbutton(parent, text=text, command=command, variable=self._status)

        self._optional = optional  # 是否可选
        self.optional = self._optional

        self.__obj_name: str = name if name else text

    def objName(self) -> str:
        """
        获取对象名称
        :return:
        """
        return self.__obj_name

    @property
    def status(self) -> bool:
        """
        当前是否选中
        :return:
        """
        return self._status.get()

    @status.setter
    def status(self, status: bool):
        """
        设置当前是否选中
        :param status:
        :return:
        """
        self._status = status

    @property
    def optional(self):
        """
        当前是否可选择
        :return:
        """
        return self._optional

    @optional.setter
    def optional(self, status: bool):
        """
        设置当前是否可选择
        :param status:
        :return:
        """
        if status:
            self.checkbutton["state"] = "normal"
        else:
            self.checkbutton["state"] = "disabled"
        self._optional = status


