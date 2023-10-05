# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file auto_config_ui.py.py
  @brief GUI 界面
    选项有  必要依赖(必须)、
           双系统时间同步、
           Google Chrome、
           python依赖、
           Qt && OpenCV依赖、
           Clion、
           PyCharm、
           编译Realsense、spdlog、kdrobotcpplibs、
           reboot
  @author yx
  @date 2023-09-24 15:34
"""
import os
import re
import sys
import platform
import subprocess
import tkinter as tk
import tkinter.messagebox
from typing import Sequence, List

from data.data import *
from ui.pwd_entry import PasswordEntry
from ui.checkbutton import CheckbuttonWidget
from ui.select_path_widget import SelectPathWidget


class AutoConfigUi(object):
    def __init__(self):
        AutoConfigUi.mkdir("run", "package")  # 创建必须目录
        self.architecture = platform.machine()

        try:
            self.support_options: Sequence[str] = list(OPTION_MAP_CMD[self.architecture].keys())  # 所有支持的选项
        except KeyError:
            print("不支持的架构: ", self.architecture)
            sys.exit(1)

        self.selected_options: List[str] = []  # 已选择的选项
        self.all_checkbutton: List[CheckbuttonWidget] = []  # 所有多选框对象
        self.need_file_path_widgets: List[SelectPathWidget] = []  # 所有需要路径的组建

        self.root: tk.Tk = tk.Tk()
        self.root.title("Linux Auto Config(Vision)")
        self.root.geometry("450x400")
        self.root.resizable(True, False)

        self.vbox_layout = tk.Frame(self.root)
        self.vbox_layout.pack()
        self.grid_layout = tk.Frame(self.root)
        self.grid_layout.pack()
        self.pb_layout = tk.Frame(self.root)
        self.pb_layout.pack()

        self.button = None
        self.is_in_script = CheckbuttonWidget(self.root, "是否在 python 脚本中执行", status=False, name="is_in_script")
        self.is_in_script.checkbutton.pack()

        self.initUi()

    def initUi(self) -> None:

        row: int = 0

        # 所有选项
        for option in self.support_options:
            # 需要给出路径的 package
            if option in NEED_FILE_PATH:
                optional = False if option in MUST_NEED_FILE_PATH else True  # 是否必须给出路径
                select_widget = SelectPathWidget(self.grid_layout, name=option, text=option, optional=optional)
                select_widget.checkbutton.checkbutton.grid(row=row, column=0)
                select_widget.label.grid(row=row, column=1)
                select_widget.pb.grid(row=row, column=2)

                widget = select_widget.checkbutton
                row += 1
                self.need_file_path_widgets.append(select_widget)
            else:  # 无需给出路径的 package
                widget = CheckbuttonWidget(self.vbox_layout, text=option, status=True)
                widget.checkbutton.pack()

            self.all_checkbutton.append(widget)  # 加入选项队列

        self.button = tk.Button(self.pb_layout, text="Run", command=self.getPwd)
        self.button.pack()

    def getPwd(self):
        """
        获取 root 密码
        :return:
        """
        PasswordEntry(self.root, "输入 root 密码", self.runCmds)

    def runCmds(self, pwd: str) -> None:
        cmds: List = []

        # 判断是否给出路径
        for widget in self.need_file_path_widgets:
            package_path = widget.label.cget("text")
            if not package_path == "None":
                OPTION_MAP_CMD[self.architecture][widget.name] += " " + package_path

        # 判断所有已经选择的选项
        for checkbutton in self.all_checkbutton:
            if checkbutton.status:
                cmds.append(OPTION_MAP_CMD[self.architecture][checkbutton.objName()].format(pwd=pwd))

        # 为所有文件添加密码


        script_files = os.listdir("script/")
        for script_file in script_files:
            if os.path.isfile("script/" + script_file):
                with open("script/" + script_file, "r") as file:
                    content = file.read()
                content = re.sub("echo %\\{PWD}", f"echo {pwd}", content)
                with open("run/" + script_file, "w") as file:
                    file.write(content)

        subprocess.run("chmod +x run/*", shell=True)

        # 执行命令 / 将命令写入文件
        if self.is_in_script.status:
            # run cmd
            for cmd in cmds:
                subprocess.run(cmd, shell=True)
            try:
                subprocess.run("rm -rf run", shell=True)
            except FileNotFoundError:
                pass
        else:
            subprocess.run("echo '#!/bin/bash' > auto_config.sh", shell=True)
            for cmd in cmds:
                with open("auto_config.sh", "a") as file:
                    if ".sh" in cmd:
                        file.write(". " + cmd + "\n")
                    else:
                        file.write(cmd + "\n")
            subprocess.run("chmod +x auto_config.sh", shell=True)
            tkinter.messagebox.showinfo("完成!")

    @staticmethod
    def mkdir(*dirs):
        for d in dirs:
            try:
                os.mkdir(d)
            except FileExistsError:
                pass


if __name__ == "__main__":
    ui = AutoConfigUi()
