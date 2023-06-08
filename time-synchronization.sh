#!/bin/bash

# @brief: time synchronization

echo "time synchronization..."
echo "(双系统时间同步设置中...)"

sudo apt install ntpdate
sudo ntpdate time.windows.com
sudo hwclock --localtime --systohc

echo "time synchronization finished!"
