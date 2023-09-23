#!/bin/bash

# @brief: time synchronization

. ../utils/auto_configure.sh

green "time synchronization..."
green "(双系统时间同步设置中...)"

sudo apt install -y ntpdate
sudo ntpdate time.windows.com
sudo hwclock --localtime --systohc

green "time synchronization finished!"
