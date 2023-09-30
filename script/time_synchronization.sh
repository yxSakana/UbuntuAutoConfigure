#!/bin/bash

# @brief: time synchronization

. script/color_config.sh

green "time synchronization..."
green "(双系统时间同步设置中...)"

echo %{PWD} | sudo -S apt install -y ntpdate
echo %{PWD} | sudo -S ntpdate time.windows.com
echo %{PWD} | sudo -S hwclock --localtime --systohc

green "time synchronization finished!"
