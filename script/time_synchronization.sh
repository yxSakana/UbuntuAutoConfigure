#!/bin/bash

# @brief: time synchronization

set -e

. script/lib/log.sh

sudo -v

log_info "time synchronization(双系统时间同步设置中)..."

sudo apt install -y ntpdate
sudo ntpdate time.windows.com
sudo hwclock --localtime --systohc

log_info "time synchronization finished!"
