#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""  
  @projectName pythonProject
  @file app.py.py
  @brief Ubuntu 环境自动化配置, 添加了 GUI
 
  @author yx 
  @date 2023-09-24 15:29
"""

from ui.auto_config_ui import AutoConfigUi
import subprocess


if __name__ == "__main__":
    ui = AutoConfigUi()
    ui.root.mainloop()

    try:
        subprocess.run("rm -rf run")
    except FileNotFoundError:
        pass
