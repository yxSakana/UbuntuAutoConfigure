#!/bin/bash
# @brief: install python depend
# @time: 2023-6-7 13:00

. script/lib/log.sh

log_info "python depend installing..."

echo %{PWD} | sudo -S apt update
echo %{PWD} | sudo -S apt install -y python3-pip
echo %{PWD} | sudo -S apt install -y python3-dev python3-pip python3-venv

log_info "python depend finished!"
