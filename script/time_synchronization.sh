#!/bin/bash

# @brief: time synchronization

. script/lib/log.sh

log_info "time synchronization..."
log_info "(双系统时间同步设置中...)"

echo %{PWD} | sudo -S apt install -y ntpdate
echo %{PWD} | sudo -S ntpdate time.windows.com
echo %{PWD} | sudo -S hwclock --localtime --systohc

log_info "time synchronization finished!"
