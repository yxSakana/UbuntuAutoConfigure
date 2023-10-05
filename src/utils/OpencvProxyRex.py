#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Project name: OpencvProxyRex
# @Filename: OpencvProxyRex.py
# @Author: sxy
# @Date: 2023-05-27 22:11

from typing import List
from os import sep
import re
import sys

opencv_path = ""
opencv_contrib_path = ""
proxy_url = "\"https://ghproxy.com/"  # 代理网址
url_rex = re.compile('"https://raw.githubusercontent.com/.*?"')

rex_opencv_paths = [
    sep.join(["3rdparty", "ippicv", "ippicv.cmake"])
]  # 标准包
rex_opencv_contrib_paths = [
    # os.sep.join(["modules", "wechat_qrcode", "CMakeLists.txt"])
    sep.join(["modules", "face", "CMakeLists.txt"]),
    sep.join(["modules", "xfeatures2d", "cmake", "download_boostdesc.cmake"]),
    sep.join(["modules", "xfeatures2d", "cmake", "download_vgg.cmake"]),
]  # 拓展包

# Ensure parameter is 3(确保参数为 3 个)
if len(sys.argv) == 3:
    # obtain OpenCV package path(获取 OpenCV 包路径)
    opencv_path = sys.argv[1]
    opencv_contrib_path = sys.argv[2]
    if not opencv_path[-1] == sep:
        opencv_path += sep
    if not opencv_contrib_path[-1] == sep:
        opencv_contrib_path += sep

    # improve the path(完善路径)
    for i in range(len(rex_opencv_paths)):
        rex_opencv_paths[i] = opencv_path + rex_opencv_paths[i]
    for i in range(len(rex_opencv_contrib_paths)):
        rex_opencv_contrib_paths[i] = opencv_contrib_path + rex_opencv_contrib_paths[i]
else:
    print("\033[31m argv != 3")
    print("(Usage): \t./OpencvProxyRex.py <opencv path> <opencv contrib path>")
    print("(example): \t./OpencvProxyRex.py /home/sss/opencv-4.5.0 /home/sss/opencv_contrib-4.5.0")
    print("(Warring): \tOnly absolute paths are supported(仅支持绝对路径) \033[0m")
    exit(-1)


def rexProxy(rex_paths: List[str]) -> None:
    for rex_path in rex_paths:
        with open(rex_path, "r") as file:
            content = file.read()
        try:
            url = re.findall(url_rex, content)[0][1:]
        except IndexError as e:
            print("\033[36m Right! \033[0m")
            continue

        result = re.sub(url_rex, proxy_url + url, content)
        with open(rex_path, "w") as file:
            file.write(result)
            print(f"\033[36m {rex_path} => Right! \033[0m")


if __name__ == '__main__':
    rexProxy(rex_opencv_paths)
    rexProxy(rex_opencv_contrib_paths)
